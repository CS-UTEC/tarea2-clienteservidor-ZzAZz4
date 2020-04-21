from flask import Flask,render_template, request, session, Response, redirect

from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


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
