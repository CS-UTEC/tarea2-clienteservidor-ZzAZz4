from flask import Flask,render_template, request, session, Response, redirect

from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/espar/<num>')
def espar(num):
    return "true" if int(num) % 2 == 0 else "false"


@app.route('/esprimo/<num>')
def esprimo(num):
    max_test = int(int(num) ** 0.5 + 1)
    for i in range(2, max_test):
        if int(num) % i == 0:
            return "false"
    return "true"                    


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


@app.route('/create_user/<user_name>/<user_fullname>/<user_username>/<user_pw>')
def create_user(user_name, user_fullname, user_username, user_pw):
    user = entities.User(
            name = user_name,
            fullname = user_fullname,
            password = user_pw,
            username = user_username
    )
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()
    
    return "User created"

@app.route('/read_users')
def read_users():
    db_session = db.getSession(engine)
    ans = db_session.query(entities.User)
    users = ans[:]

    ret = '<table><tr><th>Name</th><th>Fullname</th><th>Username</th><th>Password</th>'
    
    for i in range(len(users)):
        ret += '<tr>'
        ret = ret + '<td>|| ' + users[i].name + '</td>'
        ret = ret + '<td>|| ' + users[i].fullname + '</td>'
        ret = ret + '<td>|| ' + users[i].username + '</td>'
        ret = ret + '<td>|| ' + users[i].password + '</td>'
        ret += '</tr>'

    return ret


@app.route('/login/<usr>/<pw>')
def login(usr, pw):
    db_session = db.getSession(engine)
    ans = db_session.query(entities.User).filter(
        entities.User.username == usr        
    ).filter(
        entities.User.password == pw
    )
    users = ans[:]

    if len(users) == 0:
        return "invalid"
    else:
        return "welcome " + usr



@app.route('/palindrome/<word>')
def palindrome(word):
    return word + (" is a palindrome!" if word == word[::-1] else " is not a palindrome") 


@app.route('/multiplo/<num1>/<num2>')
def multiplo(num1, num2):
    if int(num2) == 0:
        return "ERROR: input invalido para num2: no es posible dividir entre 0"
    return num1 + ('' if int(num1) % int(num2) == 0 else " no") + " es multiplo de " + num2

 

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
