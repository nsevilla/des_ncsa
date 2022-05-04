""" Main application for public release"""
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.log
import Settings
import jira_ticket
from tornado.options import define, options
from db import DbInterface
from jira_ticket import send_confirmation_email
import os
from global_vars import log

define("port", default=8080, help="run on the given port", type=int)

DB = DbInterface()
BASE_URL = os.environ['BASE_URL']

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(tornado.web.RequestHandler):
    """
    Class that handle most of the request, all the rest of the handling is done
    by page.js
    """
    @tornado.web.asynchronous
    def get(self, path = ''):
        self.render('index.html', rootPath = r'{}/'.format(Settings.APP_ROOT))

        #passwords = read_passwd_file()
        #if verify_password(passwords, basicauth_user, basicauth_pass):
            #self.render('index.html')

class EasywebBypassHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, path = ''):
        self.render('easyweb_bypass.html')

class HelpConfirmHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, token=None):
        if not token:
            self.set_status(400)
            self.write('A token is required.')
            self.flush()
            self.finish()
            return
        request_data = DB.get_request_data(token)
        if not request_data:
            log.info(f'''Invalid token: {token}''')
            self.render('invalid_token.html', rootPath = r'{}/'.format(Settings.APP_ROOT))
        else:
            token = request_data[0][0]
            email = request_data[0][1]
            last_name = request_data[0][2]
            first_name = request_data[0][3]
            subject = request_data[0][4]
            message = request_data[0][5]
            topics = request_data[0][6]
            received = request_data[0][7]
            if received == 1:
                self.render('already_received.html', rootPath = r'{}/'.format(Settings.APP_ROOT))
                return
            if subject.lower() == 'testing':
                log.info('TESTING. Skipping Jira ticket creation and DESDM team email.')
                DB.mark_received(token)
                self.set_status(200)
                self.render('submission_confirmed.html', rootPath = r'{}/'.format(Settings.APP_ROOT))
                return
            try:
                jira_ticket.create_ticket(
                    first_name,
                    last_name,
                    email,
                    topics,
                    subject,
                    message,
                )
            except Exception as e:
                log.error(f'''Error creating Jira ticket: {e}''')
                self.write('<p>There was an error confirming your form. Please try again.</p><pre>{e}</pre>')
                self.set_status(500)
                self.flush()
                self.finish()
                return
            try:
                assert DB.mark_received(token)
            except Exception as e:
                log.error(f'''Error deleting request record: {e}''')
                self.set_status(200)
                self.flush()
                self.finish()
                return
            self.set_status(200)
            self.render('submission_confirmed.html', rootPath = r'{}/'.format(Settings.APP_ROOT))

class HelpHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        # arguments = { k.lower(): self.get_argument(k) for k in self.request.arguments }
        first_name = self.get_argument("name", "")
        last_name = self.get_argument("lastname", "")
        email = self.get_argument("email", "")
        subject = self.get_argument("subject", "")
        message = self.get_argument("question", "")
        topic = self.get_argument("topic", "")
        topics = topic.replace(',', '\n')
        log.debug(f'''{first_name}, {last_name}, {email}, {topics}, {message}''')
        try:
            token = DB.add_new_request({
                'email': email,
                'last_name': last_name,
                'first_name': first_name,
                'subject': subject,
                'message': message,
                'topics': topics,
            })
        except Exception as e:
            log.error(f'''Error adding form record: {e}''')
            self.write('There was an error submitting your form. Please try again.')
            self.set_status(500)
            self.flush()
            self.finish()
            return
        try:
            if token:
                send_confirmation_email(
                    base_url=BASE_URL,
                    token=token,
                    email=email,
                    last_name=last_name,
                    first_name=first_name,
                    subject=subject,
                    message=message,
                    topics=topics,
                )
                self.set_status(200)
                self.flush()
                self.finish()
                return
            else:
                self.write('There was an error submitting your form. Please try again.')
                self.set_status(500)
                self.flush()
                self.finish()
                return
        except Exception as e:
            log.error(f'''Error sending confirmation email to "{email}"''')
            self.write('There was an error submitting your form. Please try again.')
            self.set_status(500)
            self.flush()
            self.finish()
            return
        # self.set_status(200)
        # self.flush()
        # self.finish()


class My404Handler(tornado.web.RequestHandler):
    """
    Handles 404 requests, basically bust just changin the status to 404
    """
    def get(self):
        self.set_status(404)
        self.render('index.html', chichi=False)
    def post(self):
        self.set_status(404)
        self.render('index.html', chichi=False)

class Application(tornado.web.Application):
    """
    The tornado application  class
    """
    def __init__(self):
        # The order of the route handlers matters!
        handlers = [
            (r"{}".format(Settings.APP_ROOT), MainHandler),
            (r"{}/static/(.*)".format(Settings.APP_ROOT), tornado.web.StaticFileHandler, {'path':Settings.STATIC_PATH}),
            (r"{}/help/".format(Settings.APP_ROOT), HelpHandler),
            (r"{}/help/confirm/(.*)".format(Settings.APP_ROOT), HelpConfirmHandler),
            (r"{}/releases/sva1/content/(.*)".format(Settings.APP_ROOT), tornado.web.StaticFileHandler, {'path':Settings.SVA1_PATH}),
            (r"{}/easyweb(.*)".format(Settings.APP_ROOT), EasywebBypassHandler),
            (r"{}/(.*)".format(Settings.APP_ROOT), MainHandler),
            ]
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "debug":Settings.DEBUG,
            "default_handler_class": My404Handler,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    """
    The main function
    """
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    #http_server = tornado.httpserver.HTTPServer(Application(), ssl_options={"certfile": "/etc/httpd/ssl/des.crt", "keyfile": "/etc/httpd/ssl/des.key",})
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
