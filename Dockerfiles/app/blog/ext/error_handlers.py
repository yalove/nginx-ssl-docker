# coding: utf-8
from flask import render_template


def configure(app):
    @app.errorhandler(403)
    def forbidden_page(*args, **kwargs):
        return render_template("errors/access_forbidden.html"), 403

    @app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        return render_template('errors/page_not_found.html'), 404

    @app.errorhandler(405)
    def method_not_allowed_page(*args, **kwargs):
        return render_template("errors/method_not_allowed.html"), 405

    @app.errorhandler(500)
    def server_error_page(*args, **kwargs):
        return render_template("errors/server_error.html"), 500
