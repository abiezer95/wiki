import os
import jinja2
import webapp2
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
    def get(self):
        data=self.datos()
        user=self.validar()
        self.render("content.html", data=data, user=user)
        #db.delete(Db2.all(keys_only=True))

    def validar(self):
      a=self.get_cookies("user_id")
      a=self.check_secure_val(a)
      for d in self.datos():
        s=str(d.key().id())
        if s==a:
          return d.user
          break

    def reg(self, pword, name, user):
        add=self.add_cookies("user_id", self.make_secure_val(Session().create_session(pword, name, user)))
        self.redirect("/token=reg?username="+user+"&name="+name+"&n=1")
      
    def log(self):
      pass

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
      if user and pword and name:
        self.reg(pword, name, user)
      else:
        pass

    def start_secret(self, pword):
      pword=self.hash_keys(pword)
      pword=self.secret(pword)
      return pword 

class Session(MainHandler):
  def create_session(self, pword, name, user):
      pword=self.hash_keys(pword)
      a=Db2(name = name, user = user, pword = pword)
      a.put()
      pword=str(a.key().id())
      return pword

  def validar(self, c):
    pass

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

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/token=reg', Reg),
    ('/token=login', Login), 
    ('/logout', Logout)
], debug=True)

 #aqui le agregamos el objeto con la informacion
      #datos= db.GqlQuery("SELECT * FROM Db " "ORDER BY fecha DESC")
      #reg={}
       #  for data in datos:
        #reg[data.reguser]=[data.regpass]
      #self.write(reg)
      #user=self.request.get("user")
      #password=self.request.get("pass")
      #if user and password:
      # for r in reg:
      #   if user==r:
      #     if password==reg[r][0]:
      #       self.render("content.html", login=1)
      #else:        
      # self.render("content.html", login=0)