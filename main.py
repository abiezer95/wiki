import os
import jinja2
import webapp2
import re
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
class Db(db.Model):
      #texto=db.StringProperty(required = True)
      fecha=db.DateTimeProperty(auto_now_add = True)
      nombre=db.StringProperty(required = False)
      reguser=db.StringProperty(required = True)
      regpass=db.StringProperty(required = True) 
   	  
class MainHandler(Handler):
	#body de html
    def validar(self, user, pword):
      datos= db.GqlQuery("SELECT * FROM Db " "ORDER BY fecha DESC") 

      ps=self.get_cookies("ps")
      us=self.get_cookies("us")
    #       #
      secret=self.start_secret(user)
      ps=self.check_secure_val(ps)

      if secret==us and ps==pword:
        return self.render("content.html", datos=datos, user=user.title(), n=1)
      else:
        return self.render("errorlog.html")
      
    def get(self):
        datos= db.GqlQuery("SELECT * FROM Db " "ORDER BY fecha DESC") 
        pword=self.get_cookies("pw")
        user=self.get_cookies("user")
        if pword and user:
          self.validar(user, pword)
        else:
          self.render("content.html", datos=datos, n=0)

    def add_cookies(self, name, clave):
        self.response.headers.add_header("Set-Cookie", "%s=%s; Path=/" %(name, clave))

    def hash_keys(self, user):
      return hashear.hash(user)
    
    def check_secure_val(self, user):
      return hashear.make_secure_val(user)
    
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
    ##              ##
      if user and pword and name:
        #self.write(check_user(user))
        ##
        #self.write(pword)
        self.redirect("/token=reg?username="+user+"&pword="+self.salts()+"&name="+name+"&n=1")

      else:
        self.redirect("/token=login")

    def start_secret(self, pword):
      pword=self.hash_keys(pword)
      pword=self.secret(pword)
      return pword 


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def check_user(user):
  return user 

PASS_RE = re.compile(r"^.{3,20}$")
def check_pass(pword):
  return pword and PASS_RE.match(pword)

      #aqui le agregamos el objeto con la informacion
    	#datos= db.GqlQuery("SELECT * FROM Db " "ORDER BY fecha DESC")
    	#reg={}
       #	for data in datos:
    		#reg[data.reguser]=[data.regpass]
    	#self.write(reg)
    	#user=self.request.get("user")
    	#password=self.request.get("pass")
    	#if user and password:
    	#	for r in reg:
    	#		if user==r:
    	#			if password==reg[r][0]:
    	#				self.render("content.html", login=1)
    	#else: 				
    	#	self.render("content.html", login=0)
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
    self.add_cookies("ps", " ")
    self.add_cookies("user", " ")
    self.add_cookies("us", " ")
    self.add_cookies("pw", " ")
    self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/token=reg', Reg),
    ('/token=login', Login), 
    ('/logout', Logout)
], debug=True)
