#!/usr/bin/python3
from flask import Flask, request, url_for

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
#app = Blueprint(request.base_url, __name__, url_prefix='/admin')

@app.route('/index.html')
@app.route('/')
def home():
    body = "<h1>Pagina Inicial</h1>\n"
    body += "<p><a href='%s'>Instituicoes</p>\n" %url_for('instituicao')
    body += "<p><a href='%s'>Medicos</p>\n" %url_for('medico')
    body += "<p><a href='%s'>Prescricoes</p>\n" %url_for('prescricao')
    body += "<p><a href='%s'>Analise</p>\n" %url_for('analise')
    return composeHTML("Home Page", body)


@app.route('/instituicao')
def instituicao():
    body = "<h1>Intituicoes</h1>\n"
    body += "<p><a href='%s'>Inserir</p>\n" %url_for('instituicaoAdd')
    body += "<p><a href='%s'>Editar</p>\n" %url_for('instituicaoEdit')
    body += "<p><a href='%s'>Remover</p>\n" %url_for('instituicaoRm')
    return composeHTML("Inserir Instituicao", body)    

@app.route('/instituicao/add')
def instituicaoAdd():
    body = '<form action="update" method="post">\n'
    body += '\t<label for="fname">First name:</label><br>\n'
    body += '\t<input type="text" id="fname" name="fname" value="John"><br>\n'
    body += '\t<label for="lname">Last name:</label><br>\n'
    body += '\t<input type="text" id="lname" name="lname" value="Doe">\n'
    return composeHTML("add", body)


@app.route('/instituicao/edit')
def instituicaoEdit():
	return "Under Construction"


@app.route('/instituicao/remove')
def instituicaoRm():
	body = '<form action="ri" method="post">\n'
	body += '\t<label for="nome">Nome Instituicao:</label><br>\n'
	body += '\t<input type="text" id="nome" name="nome"><br>\n'
	body += '\t<input type="submit" value="Submit">\n'
	body += '</form>\n'
	return composeHTML("Remover", body)

# /instituicoes/remove?nome="qq"&data=      {"nome": "qq"}
@app.route('/instituicao/remove/ri', methods=['POST'])
def instituicaoRmPOST():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = "DELETE FROM instituicao WHERE nome=(%s);"
        cursor.execute(query, (request.form["nome"], ))
        return cursor
        # return query
    except Exception as e:
        return str(e)
    finally:
        #dbConn.commit() # importante?
        cursor.close()
        dbConn.close()
	

@app.route('/medico')
def medico():
    body = "<h1>Medicos</h1>\n"
    body += "<p><a href='%s'>Inserir</p>\n" %url_for('medicoAdd')
    body += "<p><a href='%s'>Editar</p>\n" %url_for('medicoEdit')
    body += "<p><a href='%s'>Remover</p>\n" %url_for('medicoRm')
    return composeHTML("Inserir Medico", body)

@app.route('/medico/add')
def medicoAdd():
	return "Under Construction"

@app.route('/medico/edit')
def medicoEdit():
	return "Under Construction"

@app.route('/medico/remove')
def medicoRm():
	return "Under Construction"


@app.route('/prescricao')
def prescricao():
    body = "<h1>Prescricoes</h1>\n"
    body += "<p><a href='%s'>Inserir</p>\n" %url_for('prescricaoAdd')
    body += "<p><a href='%s'>Editar</p>\n" %url_for('prescricaoEdit')
    body += "<p><a href='%s'>Remover</p>\n" %url_for('prescricaoRm')
    return composeHTML("Inserir Prescricao", body)

@app.route('/prescricao/add')
def prescricaoAdd():
	return "Under Construction"

@app.route('/prescricao/edit')
def prescricaoEdit():
	return "Under Construction"

@app.route('/prescricao/remove')
def prescricaoRm():
	return "Under Construction"

@app.route('/analise')
def analise():
    body = "<h1>Analises</h1>\n"
    body += "<p><a href='%s'>Inserir</p>\n" %url_for('analiseAdd')
    body += "<p><a href='%s'>Editar</p>\n" %url_for('analiseEdit')
    body += "<p><a href='%s'>Remover</p>\n" %url_for('analiseRm')
    return composeHTML("Inserir Analise", body)

@app.route('/analise/add')
def analiseAdd():
	return "Under Construction"

@app.route('/analise/edit')
def analiseEdit():
	return "Under Construction"

@app.route('/analise/remove')
def analiseRm():
	return "Under Construction"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
# CGIHandler().run(app)
