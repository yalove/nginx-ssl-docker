from wechat_sdk import WechatConf, WechatBasic
from functools import wraps
from flask import request
from redis import Redis

redis = Redis()

conf = WechatConf(
    token='yalove',
    appid='wx0ec87cb1a849be97',
    appsecret='a4c6c140f7345bb169074a4e86581212',
    encrypt_mode='safe',
    encoding_aes_key='L6ITjVvks1X4Y0TUeQ2mcotZY0L1mFYW5lqxF2ZzYDp',
	)



def check_signature(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		signature = request.args.get('signature','')
		timestamp =request.args.get('timestamp','')
		nonce =request.args.get('nonce', '')

		wechat = init_wechat()
		if not wechat.check_signature(signature=signature,timestamp=timestamp,nonce=nonce):
			if request.method == 'POST':
				return 'signature failed'
			else:
				return 'success'

		return func(*args, **kwargs)
	return decorated_function


def init_wechat():
	access_token = redis.get("wechat:access_token")
	jsapi_ticket = redis.get("wechat:jsapi_ticket")
	token_expires = redis.get("wechat:token_expires")
	ticket_expires = redis.get("wechat:ticket_expires")

	if access_token and jsapi_ticket and token_expires and ticket_expires:
		conf.access_token = access_token
		conf.jsapi_ticket = jsapi_ticket
		conf.access_token_expires_at = token_expires
		conf.jsapi_ticket_expires_at = ticket_expires
		wechat = WechatBasic(conf=conf)
	else:
		wechat = WechatBasic(conf=conf)
		access_token = wechat.get_access_token()
		redis.set("wechat:access_token", access_token['access_token'], 7000)
		redis.set("wechat:token_expires", access_token['access_token_expires_at'], 7000)
		jsapi_ticket = wechat.get_jsapi_ticket()
		redis.set("wechat:jsapi_ticket", jsapi_ticket['jsapi_ticket'], 7000)
		redis.set("wechat:ticket_expires", jsapi_ticket['jsapi_ticket_expires_at'], 7000)
	return wechat
