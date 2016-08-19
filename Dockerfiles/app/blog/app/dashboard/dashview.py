from flask import (Blueprint, url_for, request, abort, render_template)
from werkzeug import OrderedMultiDict
from .dashmodel import DashModelView
from .helper import (get_field_attr,)

class DashPanel(object):
    template_name = 'dash/panels/default.html'

    def __init__(self, dash, title):
        self.dash = dash
        self.title = title

    def dashboard_url(self):
        return url_for('%s.index' % (self.dash.blueprint.name))

    def get_template_name(self):
        return self.template_name

    def get_urls(self):
        return ()

    def get_context(self):
        return {}

    def render(self):
        return render_template(self.get_template_name(), panel=self, **self.get_context())


class Dash(object):
    """docstring for Dash"""

    def __init__(self, app, url_prefix='/dashboard', title='dashboard', endpoint='dash'):
        self.app = app
        self.blueprint = Blueprint(endpoint,
                                   __name__,
                                   static_folder='static',
                                   template_folder='templates',)
        self.url_prefix = url_prefix
        self.title = title
        self._register_model = OrderedMultiDict()
        self._panels = OrderedMultiDict()

    def register_model(self, model, db_session, list_fields=None, model_class=DashModelView,):
        if not hasattr(model, '__modelclass__'):
            model = model_class(model, db_session,self.blueprint.name)

        if list_fields:
            model.list_fields = list_fields
        self._register_model[model] = model

    def register_panel(self, title, panel):
        panel = panel(self, title)
        self._panels[title] = panel



    def get_panels(self):
        return sorted(self._panels.values(), key=lambda x: x.title)




    def get_url_name(self,model,name):
        if self._register_model.has_key(model):
            model = self._register_model[model]
        return '%s.%s_%s' % (self.blueprint.name,model.model_name, name,)

    def index(self):
        return 'ss'

    def get_urls(self):
        return (
            ('/', self.index),
        )

    def register_jinja_filter(self):
        self.app.jinja_env.filters['get_field_attr'] = get_field_attr

    def register_blueprint(self, **kwargs):
        self.app.register_blueprint(
            self.blueprint, url_prefix=self.url_prefix, **kwargs)

    def configure_routes(self):
        for url, func in self.get_urls():
            self.blueprint.route(url, methods=['GET', 'POST'])(func)

        for model in self._register_model.values():
            model_name = model.model_name()
            for url, func in model.get_urls():
                full_url = '/%s%s' % (model_name.lower(), url)
                self.blueprint.add_url_rule(
                    full_url,
                    "%s_%s" % (model_name.lower(), func.__name__),
                    func,
                    methods=['GET', 'POST'],
                )

        for panel in self._panels.values():
            for url, func in panel.get_urls():
                full_url = '/%s%s' % (panel.title, url)
                self.blueprint.add_url_rule(
                    full_url,
                    "panel_%s_%s" % (panel.title, func.__name__),
                    func,
                )

    def setup(self):
        self.configure_routes()
        self.register_blueprint()
        self.register_jinja_filter()