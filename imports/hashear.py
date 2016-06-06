import hashlib
import random
import string
import hmac

def hmacc(e):
  secret="abiezer"
  return hmac.new(secret, e).hexdigest()

def hash(s):
  return hashlib.md5(s).hexdigest()

def make_secure_val(s):
  return "%s|%s" % (s, hash(s))

def check_secure_val(h):
  val=h.split('|')[0]
  if h==make_secure_val(val):
    return val

def make_salt(f):
	return ''.join(random.choice(string.letters) for x in xrange(f))


