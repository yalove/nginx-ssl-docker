# coding: utf-8

from flask_wtf import Form

class CustomForm(Form):

    def has_been_submitted(self, request):
        return request.method == "POST" and request.form['btn'] == "{}btn".format(getattr(self, "_prefix"))
