import tornado.ioloop
import tornado.web
import tornado.escape

import os

class BaseHandler(tornado.web.RequestHandler):
	def get_login_url(this):
		return r'/login'

	def get_current_user(this):
		user_json = this.get_secure_cookie('user')
		if user_json:
			return tornado.escape.json_decode(user_json)
		else:
			return None

class LoginHandler(BaseHandler):
	def get(this):
		this.render('login.html', next='index.html')
	def post(this):
		username = this.get_argument('username', '')
		password = this.get_argument('password', '')
		# ad hoc
		auth = (username == 'yako' and password == 'yakoyako')
		if auth:
			this.set_secure_cookie('user', tornado.escape.json_encode(username))
			this.redirect(this.get_argument('next', r'/'))
		else:
			this.write('login failed')

class LogoutHandler(BaseHandler):
	def get(this):
		this.clear_cookie('user')
		this.redirect(r'/login')

class TopPageHandler(BaseHandler):
	@tornado.web.authenticated
	def get(this):
		this.write('you are now logged in! congrats!')


def testapp():
	return tornado.web.Application([
		(r'/login', LoginHandler),
		(r'/logout', LogoutHandler),
		(r'/', TopPageHandler),
	], template_path='template/', cookie_secret='TEST')


if __name__ == '__main__':
	app = testapp()
	app.listen(8585)
	tornado.ioloop.IOLoop.current().start()






