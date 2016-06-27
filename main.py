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
class Post(db.Model):
  fecha=db.DateTimeProperty(auto_now_add = True)
  text=db.TextProperty(required=True)
  user2=db.StringProperty(required = False)
  urll=db.StringProperty(required = False)
  num=db.StringProperty(required = False)
  categoria=db.IntegerProperty(int)

class Comment(db.Model):
  fecha=db.DateTimeProperty(auto_now_add = True)
  text=db.TextProperty(required = True)
  user=db.TextProperty(required = False)
  num=db.TextProperty(required = False)

class Logins(db.Model):
      fecha=db.DateTimeProperty(auto_now_add = True)
      name=db.StringProperty(required = False)
      user=db.StringProperty(required = True)
      pword=db.StringProperty(required = True)

class Privatepost(db.Model):
  user=db.StringProperty(required = False)
  keysid=db.StringProperty(required = False)

class MainHandler(Handler):
  #body de html
    def logindb(self):
      return db.GqlQuery("SELECT * FROM Logins "
                          "ORDER BY fecha DESC")
    def postdb(self):
      return db.GqlQuery("SELECT * FROM Post "
                          "ORDER BY fecha DESC")
    def commentdb(self):
      return db.GqlQuery("SELECT * FROM Comment "
                          "ORDER BY fecha DESC")
    def get(self):
        postdb=db.GqlQuery("SELECT * FROM Post "
                          "ORDER BY fecha DESC LIMIT 4")
        commentdb=self.commentdb()
        user=self.validar()
        self.render("content.html", data=postdb, comment=commentdb, user=user, f=0)
        #db.delete(Post.all(keys_only=True))
        #db.delete(Privatepost.all(keys_only=True))

    def validar(self):
      a=self.get_cookies("user_id")
      if a:
        a=self.check_secure_val(a)
        for d in self.logindb():
          s=str(d.key().id())
          if s==a:
            return d.user.title()
            break

    def reg(self, pword, name, user):
        validar=Logins.all().filter("user = ", user).get()
        if validar:
          self.render("error2.html")
        else:
          add=self.add_cookies("user_id", self.make_secure_val(Session().create_session(pword, name, user)))
          self.redirect("/token=reg?username="+user+"&name="+name+"&n=1")

    def log(self, user, pword):
      pword=self.start_secret(pword)
      login=Logins.all().filter('user = ', user).get()
      if login:
        p=str(login.pword)
        if pword==p:
          p=self.make_secure_val(str(login.key().id()))
          self.add_cookies("user_id", p)
          self.redirect("/")
        else:
          self.render("error.html")
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
      return hashear.make_salt(15)

    def get_cookies(self, c):
      return self.request.cookies.get(c)

    def getP(self, post):
      return self.request.get(post)


    def post(self):
      user=self.getP("userreg")
      pword=self.getP("passreg")
      name=self.getP("nombre")
      pub=self.getP("text")
      num=self.getP("comentar")
      if user and pword and name:
        self.reg(pword, name, user)
      elif pub:
        self.postt(pub)
      elif num:
        self.commentar(num)
      else:
        user=self.getP("user")
        pword=self.getP("pass")
        self.log(user, pword)

    def commentar(self, text):
      num=self.getP("id")
      user=self.validar()
      r=Comment(text=text, num=num, user=user)
      r.put()
      self.redirect("pub")

    #def count(self, n):
     # num=Post.all().filter("")

    def postt(self, text):
      user=self.getP("user")
      tag=1
      salt=self.salts()
      r=Post(text = text, user2=user, urll="/000", num=salt, categoria=tag)
      r.put()
      self.redirect("pub")

    def start_secret(self, pword):
      pword=self.hash_keys(pword)
      pword=self.secret(pword)
      return pword

class Posteados(MainHandler):
  def get(self):
    postdb=db.GqlQuery("SELECT * FROM Post "
                          "ORDER BY fecha DESC")
    private=db.GqlQuery("SELECT * FROM Privatepost "
                          "ORDER BY user DESC")
    dic={}
    i=0
    for post in postdb:
      dic[post.num]=[]
      for p in private:
        i=1
        if post.num==p.keysid:
           dic[post.num].append("1,"+post.user2)
      if i==0:
        dic[post.num].append("0,"+post.user2)
    
    self.write(str(dic).replace("u'", '"').replace("'", '"'))

class Posteos(MainHandler):
  def post(self):
    postdb=db.GqlQuery("SELECT * FROM Post "
                          "ORDER BY fecha DESC LIMIT 4")
    private=db.GqlQuery("SELECT * FROM Privatepost "
                          "ORDER BY user DESC")
    user=self.getP("user")
      
    for post in postdb: 
      i=0
      for p in private:
        if p.keysid==post.num and post.user2==user:
          i=1
          image="/images/hide.png"
          function="publicpost(user, id)"
          self.render("post.php", user=post.user2, keysid=post.num, text=post.text, fecha=str(post.fecha), url=post.urll, image=image, function=function)
        elif p.keysid==post.num and post.user2!=user:
          i=3
        elif p.keysid!=post.num and post.user2!=user:  
          i=2
          

      if i==0:
        image="/images/show.png"
        function="privatepost(user, id)"
        self.render("post.php", user=post.user2, keysid=post.num, text=post.text, fecha=str(post.fecha), url=post.urll, image=image, function=function)
      if i==2:
        image="/images/public.png"
        function=""
        self.render("post.php", user=post.user2, keysid=post.num, text=post.text, fecha=str(post.fecha), url=post.urll, image=image, function=function)

      
      

class Session(MainHandler):
  def create_session(self, pword, name, user):
      pword=self.start_secret(pword)
      a=Logins(name = name, user = user, pword = pword)
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

class Pub(Handler):
  def get(self):
    self.render("loading.html")

class Url(MainHandler):
 def get(self, url):
    val=Post.all().filter("urll = ", url).get()
    if val:
      data=self.postdb()
      user=self.validar()
      self.render("url.html", data=data, user=user, url=url)
    else:
      data=self.postdb()
      user=self.validar()
      self.render("url.html", data=data, user=user, url=url)

 def post(self, url):
  a=self.getP("text")
  user=self.getP("user")
  d=Post(text=a, user2=user, urll=url)
  d.put()
  self.render("loading2.html")

url = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

class Json(MainHandler):
  def get(self):
    post=self.postdb()
    comment=self.commentdb()
    json={}
    for p in post:
      json[p.num]=[]
      for c in comment:
        if p.num == c.num:
          json[""+p.num+""].append(""+c.text+""+"*/"+""+c.user+""+"*/"+""+c.num+""+"*/"+""+str(c.fecha))
    json=str(json).replace("u'", '"').replace("'", '"')
    self.write(json)


class Privatespost(MainHandler):
  def post(self):
    keysid=self.getP("id")
    user=self.getP("user")
    r=Privatepost(user=user, keysid=keysid)
    r.put()

class Publicpost(MainHandler):
  def post(self):
    keysid=self.getP("id")
    filtrar=Privatepost.all().filter("keysid = ", keysid)
    db.delete(filtrar)
    

class Deletepost(MainHandler):
  def post(self):
    post=self.getP("post")
    comentarios=self.commentdb()
    for c in comentarios:
      if post==c.num:
        db.delete(c)
    db.delete(Post.all().filter("num = ", post).get())

class Deletecomment(MainHandler):
  def post(self):
    texto=str(self.getP("texto"))
    fecha=str(self.getP("fecha"))
    comentarios=self.commentdb()
    for c in comentarios:
      if fecha==str(c.fecha) and texto==str(c.text):
        db.delete(c)

class Bestcomment(MainHandler):
  def get(self):
    dic=self.count()
    self.render("bestcomment.php", dic=dic)

  def count(self):
    comentarios=self.commentdb()
    post=self.postdb()
    dic={}
    for p in post:
      i=0
      dic[p.num]=[]
      for c in comentarios:
         if p.num==c.num:
          i=i+1
      dic[p.num].append(i)
    return str(dic).replace("u'", '"').replace("'", '"')

#esto me lee la url y permite los caracteres qe le mande
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/token=reg', Reg),
    ('/token=login', Login),
    ('/logout', Logout),
    ('/pub', Pub),
    ("/content/.json", Json),
    ("/posteados/post", Posteados),
    ("/posteos", Posteos),
    ("/eliminar/deletepost", Deletepost),
    ("/eliminar/deletecomment", Deletecomment),
    ("/private/post", Privatespost),
    ("/public/post", Publicpost),
    ("/best/comments", Bestcomment),
    (url, Url)
], debug=True)