import os
import jinja2
import webapp2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

class MainPage(Handler):
    def get(self):
        self.render("home.html")

    def post(self):
        username = self.request.get("name")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""
        if not valid_username(username):
            username_error = "That's not a valid username."
        if not valid_password(password):
            password_error = "Invalid password"
        if password != verify:
            verify_error = "Passwords do not match"
        if not valid_email(email):
            email_error = "That's not a valid email"
        if not username_error and not password_error and not verify_error and not email_error:
            self.redirect("/welcome?username=" + username)
        else:
            self.render("home.html", name = username, username_error = username_error, password_error = password_error, verify_error = verify_error, email = email, email_error = email_error)

class WelcomePage(Handler):
    def get(self):
        username = self.request.get("username")
        self.render("welcome.html", username = username)

app = webapp2.WSGIApplication([('/', MainPage), ('/welcome', WelcomePage)], debug = True)