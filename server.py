import tornado.ioloop
import tornado.web
import tornado.escape

import os
import _const

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.db.models import *


class BaseHandler(tornado.web.RequestHandler):
	def get_login_url(this):
		return r'/login'

	def get_current_user(this):
		user = this.get_secure_cookie('user')
		if user:
			return tornado.escape.json_decode(user)
		else:
			return None

class LoginHandler(BaseHandler):
	def get(this):
		this.render('login.html', next='index.html')
	def post(this):
		try:
			username = this.get_argument('username')
			password = this.get_argument('password')

			usr = sql.query(Account).filter(Account.user_id == username).all()
			if len(usr) <= 0:
				raise Exception('no such user')
			usr = usr[0]
			auth = usr.check_password(password)

			if auth:
				#this.set_secure_cookie('user', tornado.escape.json_encode(username))
				this.set_secure_cookie('user', tornado.escape.json_encode( {'username': username, 'display_name': usr.display_name} ))
				this.redirect(this.get_argument('next', r'/'))
			else:
				raise Exception('password did not match')

		except Exception as e:
			this.write(str(e))

class LogoutHandler(BaseHandler):
	def get(this):
		this.clear_cookie('user')
		this.redirect(r'/login')


class RegisterHandler(BaseHandler):
	def get(this):
		this.render('register.html', next='login.html')
	def post(this):
		try:
			username = this.get_argument('username')
			display_name = this.get_argument('display_name', '')
			if len(display_name) <= 0:
				display_name = username
			password = this.get_argument('password')
			password_doublecheck = this.get_argument('password_doublecheck')

			if password != password_doublecheck:
				raise Exception('password did not match')
			else:
				sql.add(Account(username, display_name, password))
				sql.commit()
				this.write('successfully registered')

		except Exception as e:
			this.write(str(e))
			sql.rollback()
		


class TopPageHandler(BaseHandler):
	@tornado.web.authenticated
	def get(this):
		this.write('you are now logged in! congrats!<br>')
		this.write('your userid is: %s' % this.get_current_user()['display_name'])




def testapp():
	return tornado.web.Application([
		(r'/login', LoginHandler),
		(r'/logout', LogoutHandler),
		(r'/register', RegisterHandler),
		(r'/', TopPageHandler),
	], template_path='template/', cookie_secret=_const.secure_cookie_secret)


sql = None

if __name__ == '__main__':
	sql_engine = create_engine(_const.db_address, encoding='utf_8')
	Sql_Session = sessionmaker(bind=sql_engine)
	sql = Sql_Session()

	app = testapp()
	app.listen(8585)
	tornado.ioloop.IOLoop.current().start()






