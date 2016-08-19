from werkzeug import OrderedMultiDict
from flask import render_template
from .helper import (query, get_field_type, creat_query,
                     model_form, make_dict, query_get, set_relation_model, slugify)
from datetime import datetime
from ..users.model import User

class DashTemplateHelper(object):
    pass


class DashModel(object):
    model = None
    columns = None
    db_session = None
    list_fields = []
    Item_Per_Page = 10

    def __init__(self, model, db_session,blueprint_name, *args, **kwargs):
        self.model = model
        if not self.model:
            raise Exception('DashModel must have a model!')
        self.db_session = db_session
        if not self.db_session:
            raise Exception('DashModel must have a db_session!')
        if not self.columns:
            self.columns = self.get_columns()
        if not self.list_fields:
            self.list_fields = self.columns
        self.__modelclass__ = 'dashmodel'
        self.blueprint = blueprint_name

    def model_name(self):
        return self.model.__name__

    def get_columns(self):
        columns = OrderedMultiDict()
        for column in self.model.__table__.columns:
            columns[column.name] = getattr(self.model, column.name)
        self.column_names = columns.keys()
        return columns

    def get_model_form(self, obj):
        return model_form(self.model, self.db_session)(obj=obj)

    def get_paginate(self, model,search_params, page=1):
        paginate = creat_query(query, self.db_session, model, search_params).paginate(
            page, self.Item_Per_Page)
        # paginate :: page pages items
        return paginate

    def get_model_details(self, model, search_params,page):
        details_dict = {}
        details_dict = make_dict(self.get_paginate(model,search_params,page))
        for item in details_dict['items']:
            set_relation_model(item, User, self.db_session, 'user_id', 'user')
        return details_dict


class DashModelView(DashModel):
    """docstring for DashModel"""

    def get_url_name(self, name):
        return '%s.%s_%s' % (self.blueprint, self.model_name().lower(), name)

    def get_urls(self):
        return (
            ('/', self.index),
            ('/lists', self.lists),
            ('/lists/<int:page>', self.lists),
        )


    def lists(self, page=1):

        search_params = {
            'filters': [{'and':
                         [{'or':
                           [{'fieldname': 'id', 'op': '>=', 'val': 2},
                            {'fieldname': 'id', 'op': '<=', 'val': 13},
                            ]
                           },
                          {'fieldname': 'date', 'op': '>', 'val': datetime(2015, 11, 24)}, ]
                         }],
            'order_by': [{'fieldname': 'id', 'direction': 'asc'}, ],
            'group_by': [{'fieldname': 'id'}, ],
        }
        s = {
            'filters': [],
            'order_by': [],
            'group_by': [],
        }
        form = self.get_model_form(self.model)
        result = self.get_model_details(self.model, s,page)


        return render_template('dash/model/lists.html', model=self,form=form, **result)

    def index(self):
        return "%s" % self.model.__name__
