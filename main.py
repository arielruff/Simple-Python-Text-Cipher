
# encoding: utf-8
import os
import jinja2
import webapp2
import string

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    
    def write_block(self, crypt="", nocrypt=""):  #Define text submission args
        self.render("index.html", crypted=crypt, noncrypted=nocrypt) #Take input text and inject into output html
        
        
    def get(self):
        self.write_block() 
       
    def post(self):
        user_text = self.request.get('text')  #Grab text which was entered into form
        crypt = self.rot13(user_text)  #Performs Rot13 on given texts
        self.write_block(crypt,user_text)
    
    def rot13(self,rottext):
        rot13 = string.maketrans( 
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
        crypt_text = string.translate(str(rottext), rot13)
        return crypt_text
        
app = webapp2.WSGIApplication([('/', MainPage),
], debug=True)
