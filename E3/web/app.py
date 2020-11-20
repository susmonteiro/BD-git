#!/usr/bin/python3
from wsgiref.handlersimport CGIHandler
from flask import Flask, request

import psycopg2
import psycopg2.extras
def headerHTML(title):
    return "<html lang=\"en-US\">\n<head>\n<title>%s</title>\n</head>\n"%title

def composeHTML(title, body):
    return "<!DOCTYPE html>\n" + headerHTML(title) + "<body>\n" + body + "</body>\n" + "</html>"

## SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist192456" 
DB_DATABASE=DB_USER
DB_PASSWORD="psql192456"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)


app = Flask(__name__)

@app.route('/index.html')
@app.route('/')
def home():
    body = "<h1>Main Page</h1>\n"
    body += "<p><a href='/instituicoes'>Instituicoes</p>\n"
    body += "<p><a href='/medicos'>Medicos</p>\n"
    body += "<p><a href='/prescricoes'>Prescricoes</p>\n"
    body += "<p><a href='/analise'>Analise</p>\n"
    return composeHTML("Home Page", body)


""" @app.route('/instituicoes/add')
def instituicoes():
    body = '<form action="update" method="post">\n'
    body += '\t<label for="fname">First name:</label><br>\n'
    body += '\t<input type="text" id="fname" name="fname" value="John"><br>\n'
    body += '\t<label for="lname">Last name:</label><br>\n'
    body += '\t<input type="text" id="lname" name="lname" value="Doe">\n'
 """

@app.route('/instituicoes/remove', methods=['POST'])
def remove_instituicoes():
    if request.method == 'POST':
        try:
            dbConn = psycopg2.connect(DB_CONNECTION_STRING)
            cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
            query = "DELETE FROM instituicoes WHERE nome=(%s);"
            cursor.execute(query, (request.form["nome"], ))
        except Exception as e:
            print(e)


CGIHandler().run(app)