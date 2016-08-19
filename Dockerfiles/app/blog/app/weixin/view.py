from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect, g,jsonify
from .utils import check_signature


weixin = Blueprint("weixin", __name__)

@weixin.route('/weixin', methods=['GET', 'POST'])
@check_signature
def handle_wechat_request():
	if request.method == 'POST':
		return wechat_response(request.data)
	else:
		return request.args.get('echostr', '')