#!/usr/bin/python3
from flask import Flask, request, url_for, render_template  

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
    try:
        return render_template('operations.html', name= 'Inserir Instituicao', action= url_for('instituicaoAddDB'), \
            values= {'Nome':'nome', 'Tipo': 'tipo', 'Numero de Regiao': 'num_regiao', 'Numero de Concelho': 'num_concelho'})
    except Exception as e:
        return str(e)
    

@app.route('/instituicao/add/ai', methods=['POST'])
def instituicaoAddDB():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'INSERT INTO instituicao VALUES (%s, %s, %s, %s);'
        cursor.execute(query, (request.form['nome'], request.form['tipo'], request.form['num_regiao'], request.form['num_concelho']))
        return 'Instituicao inserida com sucesso :)'
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/instituicao/edit')
def instituicaoEdit():
	return "Under Construction"


@app.route('/instituicao/remove')
def instituicaoRm():
	body = '<form action="%s" method="post">\n' %url_for('instituicaoRmDB')
	body += '\t<label for="nome">Nome Instituicao:</label><br>\n'
	body += '\t<input type="text" id="nome" name="nome"><br>\n'
	body += '\t<input type="submit" value="Submit">\n'
	body += '</form>\n'
	return composeHTML("Remover", body)

# /instituicoes/remove?nome="qq"&data=      {"nome": "qq"}
@app.route('/instituicao/remove/ri', methods=['POST'])
def instituicaoRmDB():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'DELETE FROM instituicao WHERE nome=(%s);'
        cursor.execute(query, (request.form['nome'], ))
        return tuple(cursor)
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
    app.run(debug = True, host='0.0.0.0')
