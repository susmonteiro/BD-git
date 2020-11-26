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
    body += "<p><a href='%s'>Listar substancias</p>\n" %url_for('listarSubstancias')
    return composeHTML("Home Page", body)


#---------- Instituicao ----------#
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
            values= {'nome': 'Nome', 'tipo': 'Tipo', 'num_regiao': 'Numero de Regiao', 'num_concelho': 'Numero de Concelho'})
    except Exception as e:
        return render_template('returnMainPage.html', text=str(e))
    

@app.route('/instituicao/add/ai', methods=['POST'])
def instituicaoAddDB():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'INSERT INTO instituicao VALUES (%s, %s, %s, %s);'
        cursor.execute(query, (request.form['nome'], request.form['tipo'], request.form['num_regiao'], request.form['num_concelho']))
        return render_template('returnMainPage.html', text='Instituicao inserida com sucesso :)')
    except Exception as e:
        return render_template('returnMainPage.html', text=str(e))
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
        return render_template('returnMainPage.html', text=str(e))
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


#---------- Medico ----------#
@app.route('/medico')
def medico():
    body = "<h1>Medicos</h1>\n"
    body += "<p><a href='%s'>Inserir</p>\n" %url_for('medicoAdd')
    body += "<p><a href='%s'>Editar</p>\n" %url_for('medicoEdit')
    body += "<p><a href='%s'>Remover</p>\n" %url_for('medicoRm')
    return composeHTML("Inserir Medico", body)

@app.route('/medico/add')
def medicoAdd():
    try:
        return render_template('operations.html', name= 'Inserir Medico', action= url_for('medicoAddDB'), \
            values= {'num_cedula': 'Numero de Cedula', 'nome': 'Nome', 'especialidade': 'Especialidade' })
    except Exception as e:
        return render_template('returnMainPage.html', text=str(e))

@app.route('/medico/add/am', methods=['POST'])
def medicoAddDB():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'INSERT INTO medico VALUES (%s, %s, %s);'
        cursor.execute(query, (request.form['num_cedula'], request.form['nome'], request.form['especialidade']))
        return render_template('returnMainPage.html', text='Medico inserido com sucesso :)')
    except Exception as e:
        return render_template('returnMainPage.html', text=str(e))
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()
        

@app.route('/medico/edit')
def medicoEdit():
	return "Under Construction"

@app.route('/medico/remove')
def medicoRm():
	return "Under Construction"


#---------- Prescricao ----------#
@app.route('/prescricao')
def prescricao():
    body = "<h1>Prescricoes</h1>\n"
    body += "<p><a href='%s'>Inserir</p>\n" %url_for('prescricaoAdd')
    body += "<p><a href='%s'>Editar</p>\n" %url_for('prescricaoEdit')
    body += "<p><a href='%s'>Remover</p>\n" %url_for('prescricaoRm')
    return composeHTML("Inserir Prescricao", body)

@app.route('/prescricao/add')
def prescricaoAdd():
    try: 
        return render_template('operations.html', name= 'Inserir Prescricao', action= url_for('prescricaoAddDB'),\
            values= {'num_cedula': 'Numero de Cedula', 'num_doente': 'Numero de Doente', 'data': 'Data', 'substancia': 'Substancia', 'quant': 'Quantidade'}) 
    except Exception as e: 
        return render_template('returnMainPage.html', text=str(e))


@app.route('/prescricao/add/ap', methods=['POST'])
def prescricaoAddDB():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'INSERT INTO prescricao VALUES (%s, %s, %s, %s, %s);'
        cursor.execute(query, (request.form['num_cedula'], request.form['num_doente'], request.form['data'], request.form['substancia'], request.form['quant']))
        return render_template('returnMainPage.html', text='Prescricao inserida com sucesso :)')
    except Exception as e:
        return render_template('returnMainPage.html', text=str(e))

    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/prescricao/edit')
def prescricaoEdit():
	return "Under Construction"

@app.route('/prescricao/remove')
def prescricaoRm():
	return "Under Construction"


#---------- Analise ----------#
@app.route('/analise')
def analise():
    body = "<h1>Analises</h1>\n"
    body += "<p><a href='%s'>Inserir</p>\n" %url_for('analiseAdd')
    body += "<p><a href='%s'>Editar</p>\n" %url_for('analiseEdit')
    body += "<p><a href='%s'>Remover</p>\n" %url_for('analiseRm')
    return composeHTML("Inserir Analise", body)

@app.route('/analise/add')
def analiseAdd():
    try:
        return render_template('operations.html', name= 'Inserir Analise', action= url_for('analiseAddDB'),\
            values= {'num_analise': 'Numero de Analise', 'especialidade': 'Especialidade','num_cedula': 'Numero de Cedula',\
            'num_doente': 'Numero de Doente', 'data': 'Data', 'data_registo': 'Data de Registo', 'nome': 'Nome', 'quant': 'Quantidade', 'inst': 'Instituicao'})
    except Exception as e: 
        return render_template('returnMainPage.html', text=str(e))

@app.route('/analise/add/aa', methods=['POST'])
def analiseAddDB():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'INSERT INTO analise VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
        cursor.execute(query, (request.form['num_analise'], request.form['especialidade'], request.form['num_cedula'], request.form['num_doente'], \
        request.form['data'], request.form['data_registo'], request.form['nome'], request.form['quant'], request.form['inst']))
        return render_template('returnMainPage.html', text='Analise inserida com sucesso :)')
    except Exception as e:
        return render_template('returnMainPage.html', text=str(e))

    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/analise/edit')
def analiseEdit():
	return "Under Construction"

@app.route('/analise/remove')
def analiseRm():
    try:
        return render_template('operations.html', name='Remover Analise', action=url_for('analiseRmDB'),\
            values= {'num_analise': 'Numero de Analise'})
    except Exception as e: 
        return render_template('returnMainPage.html', text=str(e))

# /instituicoes/remove?nome="qq"&data=      {"nome": "qq"}
@app.route('/analise/remove/ra', methods=['POST'])
def analiseRmDB():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'DELETE FROM analise WHERE num_analise=(%s);'
        cursor.execute(query, (request.form['num_analise'], ))
        return render_template('returnMainPage.html', text='Analise removida com sucesso :)')
    except Exception as e:
        return render_template('returnMainPage.html', text=str(e))
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/listSub')
def listarSubstancias():
    try:
        return render_template('operations.html', name='Listar Substancias', action=url_for('listarSubstanciasDB'),\
            values = {'num_cedula': 'Numero de Cedula', 'mes': 'Mes', 'ano': 'Ano'})
    except Exception as e:
         return render_template('returnMainPage.html', text=str(e))

@app.route('/listSub/ls', methods=['POST'])
def listarSubstanciasDB():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'SELECT substancia FROM prescricao, EXTRACT(YEAR FROM _data) AS ano, EXTRACT(MONTH FROM _data) AS mes WHERE num_cedula = %s AND mes = %s AND ano = %s;'
        cursor.execute(query, (request.form['num_cedula'], request.form['mes'], request.form['ano']))
        #return ":)"
        return render_template('list.html', header='Substancias:', cursor=cursor)
    except Exception as e:
        return render_template('returnMainPage.html', text=str(e))
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
