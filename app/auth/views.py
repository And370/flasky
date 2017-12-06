from flask import render_template
from . import  auth

@auth.rout('/login')
def log():
    return render_template('auth/login.html')