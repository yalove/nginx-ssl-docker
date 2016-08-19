# coding: utf-8
from flask import send_from_directory
def configure_static(app):
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(app.static_folder, 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    @app.route('/robots.txt')
    def robotstxt():
        return send_from_directory(app.static_folder, 'robots.txt')
