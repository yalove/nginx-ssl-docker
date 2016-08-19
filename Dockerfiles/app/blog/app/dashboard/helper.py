from sqlalchemy.exc import (NoInspectionAvailable, OperationalError)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (ColumnProperty, RelationshipProperty)
from sqlalchemy.orm.attributes import (
    InstrumentedAttribute, QueryableAttribute)
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import RelationshipProperty as RelProperty
from wtforms.ext.sqlalchemy.orm import model_form as mf
from flask.ext.wtf import Form
from sqlalchemy import (and_, or_, )
import inspect
from ..ext import db
import re
def query(model, db_session):
    if hasattr(model, 'query'):
        if callable(model.query):
            query = model.query()
        else:
            query = model.query
        if hasattr(query, 'filter'):
            return query
    return db_session.query(model)


def query_get(model, db_session, id):
    return query(model, db_session).get(id)


def get_field_type(model, filedname):
    field = getattr(model, filedname)
    if isinstance(field, ColumnElement):
        fieldtype = field.type
    else:
        if isinstance(field, AssociationProxy):
            field = field.remote_attr
        if hasattr(field, 'property'):
            prop = field.property
            if isinstance(prop, RelProperty):
                return None
            fieldtype = prop.columns[0].type
        else:
            return None
    return fieldtype


def primary_key_names(model):
    return [key for key, field in inspect.getmembers(model)
            if isinstance(field, QueryableAttribute)
            and isinstance(field.property, ColumnProperty)
            and field.property.columns[0].primary_key]

OPERATORS = {
    'is_null': lambda f: f == None,
    'is_not_null': lambda f: f != None,
    'desc': lambda f: f.desc,
    'asc': lambda f: f.asc,
    '==': lambda f, a: f == a,
    'eq': lambda f, a: f == a,
    'equal_to': lambda f, a: f == a,
    '!=': lambda f, a: f != a,
    'ne': lambda f, a: f != a,
    'not_equal_to': lambda f, a: f != a,
    '>': lambda f, a: f > a,
    'gt': lambda f, a: f > a,
    '>=': lambda f, a: f >= a,
    'ge': lambda f, a: f >= a,
    '<=': lambda f, a: f <= a,
    'le': lambda f, a: f <= a,
    'ilike': lambda f, a: f.ilike(a),
    'like': lambda f, a: f.like(a),
    'in': lambda f, a: f.in_(a),
    'not_in': lambda f, a: ~f.in_(a),
    'has': lambda f, a, fn: f.has(_sub_operator(f, a, fn)),
    'any': lambda f, a, fn: f.any(_sub_operator(f, a, fn)),
}


class Order_By(object):

    def __init__(self, fieldname, direction='asc'):
        self.field = fieldname
        self.direction = direction


class Group_By(object):

    def __init__(self, fieldname):
        self.field = fieldname


class Filter(object):
    '''
        {'or':
            ['and':
                [dict(name= 'name',op = 'like', val='%y%'),
                 dict(name= 'age',op = 'like', val='%y%')],
                 [dict(name= 'name',op = 'eq', val='zz')],
            ]

        }
    '''

    def __init__(self, fieldname, operator, argument=None, otherfield=None):
        self.fieldname = fieldname
        self.operator = operator
        self.argument = argument
        self.otherfield = otherfield

    @staticmethod
    def from_dict(dictionary):
        if 'or' not in dictionary and 'and' not in dictionary:
            fieldname = dictionary.get('fieldname')
            operator = dictionary.get('op')
            argument = dictionary.get('val')
            otherfield = dictionary.get('otherfield')
            return Filter(fieldname, operator, argument, otherfield)
        from_dict = Filter.from_dict
        if 'or' in dictionary:
            subfilters = dictionary.get('or')
            return DisjuncionFilter(*(from_dict(f) for f in subfilters))
        if 'and' in dictionary:
            subfilters = dictionary.get('and')
            return ConjunctionFilter(*(from_dict(f) for f in subfilters))


class JunctionFilter(Filter):
    """docstring for JunctionFilter"""

    def __init__(self, *subfilters):
        self.subfilters = subfilters

    def __iter__(self):
        return iter(self.subfilters)


class ConjunctionFilter(JunctionFilter):
    """docstring for ConjunctionFilter"""
    pass


class DisjuncionFilter(JunctionFilter):
    """docstring for DisjuncionFilter"""
    pass


class SearchPara(object):

    def __init__(self, filters=None, order_by=None, group_by=None):
        self.filters = filters or []
        self.order_by = order_by or []
        self.group_by = group_by or []

    @staticmethod
    def from_dictionary(dictionary):
        '''
            {
                'filters' : [{'fieldname':'id', 'op':'>', 'val':20 },{},...],
                'order_by' : [{'fieldname':'id', 'direction':'desc' },{},...],
                'group_by': [{'fieldname':id },{},...],
            }
        '''
        filters = [Filter.from_dict(f) for f in dictionary.get('filters', [])]
        order_by = [Order_By(**o) for o in dictionary.get('order_by', [])]
        group_by = [Group_By(**o) for o in dictionary.get('group_by', [])]
        return SearchPara(filters=filters, order_by=order_by, group_by=group_by)


class QueryBuilder(object):
    """docstring for QueryBuilder"""

    @staticmethod
    def _create_operation(model, fieldname, operator, argument, relation=None):
        operatorFunc = OPERATORS[operator]
        numargs = len(inspect.getargspec(operatorFunc).args)
        field = getattr(model, relation or fieldname)
        if numargs == 1:
            return operatorFunc(field)
        if argument is None:
            raise TypeError(
                'to compare a value to Null ,use is_null or is_not_null')
        if numargs == 2:
            return operatorFunc(field, argument)
        return operatorFunc(field, argument, fieldname)

    @staticmethod
    def _create_filter(model, filt):
        if not isinstance(filt, JunctionFilter):
            fname = filt.fieldname
            val = filt.argument
            relation = None
            if '__' in fname:
                relation, fname = fname.split('__')
            if filt.otherfield:
                val = getattr(model, filt.otherfield)
            create_op = QueryBuilder._create_operation
            return create_op(model, fname, filt.operator, val, relation)
        create_filt = QueryBuilder._create_filter
        if isinstance(filt, ConjunctionFilter):
            return and_(create_filt(model, f) for f in filt)
        return or_(create_filt(model, f) for f in filt)

    @staticmethod
    def creat_query(query, session, model, search_params, _ignore_order_by=False):
        query = query(model, session)
        create_filter = QueryBuilder._create_filter
        filters = [create_filter(model, f) for f in search_params.filters]
        query = query.filter(*filters)

        if not _ignore_order_by:
            if search_params.order_by:
                for order_object in search_params.order_by:
                    field_name = order_object.field
                    if '__' in field_name:
                        field_name, field_name_in_relation = field_name.split(
                            '__')
                        relation = getattr(model, field_name)
                        relation_model = relation.mapper.class_
                        field = getattr(relation_model, field_name_in_relation)
                        direction = getattr(field, order_object.direction)
                        query = query.join(relation_model)
                        query = query.order_by(direction())
                    else:
                        field = getattr(model, order_object.field)
                        direction = getattr(field, order_object.direction)
                        query = query.order_by(direction())
            else:
                pks = primary_key_names(model)
                pk_order = (getattr(model, field).asc() for field in pks)
                query = query.order_by(*pk_order)

        if search_params.group_by:
            for group in search_params.group_by:
                field = getattr(model, group.field)
                query = query.group_by(field)

        return query


def creat_query(query, session, model, search_params, _ignore_order_by=False):
    if isinstance(search_params, dict):
        search_params = SearchPara.from_dictionary(search_params)
    return QueryBuilder.creat_query(query, session, model, search_params, _ignore_order_by)


def set_relation_model(instance,relate_model,db_session,attr,attr1):
    if hasattr(instance,attr):
        user = query_get(relate_model,db_session,getattr(instance,attr))
        setattr(instance,attr1, user)


def model_form(*args, **kwargs):
    # model db.session  bound obj instance
    if not 'base_class' in kwargs:
        kwargs['base_class'] = Form
    return mf(*args, **kwargs)


def make_dict(paginate):
    p_dict = dict()
    for i in dir(paginate):
        if not i.startswith('__'):
            p_dict[i] = getattr(paginate, i)
    return p_dict

def get_field_attr(field, attr):
    if hasattr(field, attr):
        return getattr(field,attr)
    return None

def slugify(s):
    return re.sub('[^a-z0-9_\-]+','-',s.lower())