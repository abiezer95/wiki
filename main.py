import os
import jinja2
import webapp2
import re
import htmllib

from urllib import quote
#conectando a la base de datos
from google.appengine.ext import db
from imports import hashear

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
##
class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

#clase database
class Db2(db.Model):
      #texto=db.StringProperty(required = True)
      fecha=db.DateTimeProperty(auto_now_add = True)
      name=db.StringProperty(required = False)
      user=db.StringProperty(required = True)
      pword=db.StringProperty(required = True)

class MainHandler(Handler):
  #body de html
    def datos(self):
      return db.GqlQuery("SELECT * FROM Db2 "
                          "ORDER BY fecha DESC")
    def datos2(self):
      return db.GqlQuery("SELECT * FROM Db1 "
                          "ORDER BY fecha DESC")
    def get(self):
        data2=self.datos2()
        user=self.validar()
        self.render("content.html", data=data2, user=user)
        #db.delete(d1.all(keys_only=True))

    def validar(self):
      a=self.get_cookies("user_id")
      if a:
        a=self.check_secure_val(a)
        for d in self.datos():
          s=str(d.key().id())
          if s==a:
            return d.user.title()
            break

    def reg(self, pword, name, user):
        validar=Db2.all().filter('user = ', user).get()
        if validar:
          self.render("error2.html")
        else:
          add=self.add_cookies("user_id", self.make_secure_val(Session().create_session(pword, name, user)))
          self.redirect("/token=reg?username="+user+"&name="+name+"&n=1")

    def log(self, user, pword):
      ps=self.start_secret(pword)
      f=Db2.all().filter('user = ', user).get()
      if f:
        p=str(f.pword)
        if ps==p:
          p=self.make_secure_val(str(f.key().id()))
          self.add_cookies("user_id", p)
          self.redirect("/")
      else:
        self.render("error.html")

    def add_cookies(self, name, clave):
        self.response.headers.add_header("Set-Cookie", "%s=%s; Path=/" %(name, clave))

    def hash_keys(self, user):
      return hashear.hash(user)

    def make_secure_val(self, user):
      return hashear.make_secure_val(user)

    def check_secure_val(self, user):
      return hashear.check_secure_val(user)

    def secret(self, user):
      return hashear.hmacc(user)
        ##
    def salts(self):
      return hashear.make_salt(10)

    def get_cookies(self, c):
      return self.request.cookies.get(c)

    def getP(self, post):
      return self.request.get(post)


    def post(self):
      user=self.getP("userreg")
      pword=self.getP("passreg")
      name=self.getP("nombre")
      pub=self.getP("text")
      if user and pword and name:
        self.reg(pword, name, user)
      elif pub:
        self.postt(pub)
      else:
        user=self.getP("user")
        pword=self.getP("pass")
        self.log(user, pword)

    def postt(self, pub):
      user=self.request.get("user")
      #self.write(pub)
      r=Db1(text = pub, user2=user, urll="/000")
      r.put()
      self.redirect("pub")

    def start_secret(self, pword):
      pword=self.hash_keys(pword)
      pword=self.secret(pword)
      return pword

class Session(MainHandler):
  def create_session(self, pword, name, user):
      pword=self.start_secret(pword)
      a=Db2(name = name, user = user, pword = pword)
      a.put()
      pword=str(a.key().id())
      return pword

class Reg(Handler):
  def get(self):
    user = self.request.get("username")
    pword = self.request.get("pword")
    name=self.request.get("name").title()
    self.render("login.html", name=name)

class Login(Handler):
  def get(self):
    self.write(self.user)

class Logout(MainHandler):
  def get(self):
    self.add_cookies("user_id", " ")
    self.redirect("/")

class Db1(db.Model):
  fecha=db.DateTimeProperty(auto_now_add = True)
  text=db.TextProperty(required=True)
  user2=db.StringProperty(required = False)
  urll=db.StringProperty(required = False)

class Pub(Handler):
  def get(self):
    self.render("loading.html")

class Url(MainHandler):
 def get(self, url):
    val=Db1.all().filter("urll = ", url).get()
    if val:
      data2=self.datos2()
      user=self.validar()
      self.render("url.html", data=data2, user=user, url=url)
    else:
      data2=self.datos2()
      user=self.validar()
      self.render("url.html", data=data2, user=user, url=url)

 def post(self, url):
  a=self.getP("text")
  user=self.getP("user")
  d=Db1(text=a, user2=user, urll=url)
  d.put()
  self.render("loading2.html")

url = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
#esto me lee la url y permite los caracteres qe le mande
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/token=reg', Reg),
    ('/token=login', Login),
    ('/logout', Logout),
    ('/pub', Pub),
    (url, Url)
], debug=True)