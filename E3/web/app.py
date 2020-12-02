#!/usr/bin/python3
from flask import Flask, request, url_for, render_template  
from datetime import date

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
	body = "<h1>Sistema de Informação ODISSEIA</h1>\n"
	body += "<p><a href='%s'>Instituicoes</p>\n" %url_for('instituicao')
	body += "<p><a href='%s'>Medicos</p>\n" %url_for('medico')
	body += "<p><a href='%s'>Prescricoes</p>\n" %url_for('prescricao')
	body += "<p><a href='%s'>Analise</p>\n" %url_for('analise')
	body += "<p><a href='%s'>Realizar venda Farmacia</p>\n" %url_for('vendaFarm')
	body += "<p><a href='%s'>Listar substancias</p>\n" %url_for('listarSubstancias')
	body += "<p><a href='%s'>Listar glicemia</p>\n" %url_for('listarGlicemia')
	return composeHTML("Home Page", body)


#---------- Instituicao ----------#
@app.route('/instituicao')
def instituicao():
	body = "<h1>Intituicoes</h1>\n"
	body += "<p><a href='%s'>Inserir</p>\n" %url_for('instituicaoAdd')
	body += "<p><a href='%s'>Editar</p>\n" %url_for('instituicaoEdit')
	body += "<p><a href='%s'>Remover</p>\n" %url_for('instituicaoRm')
	return composeHTML("Instituicao", body)    

# Adicionar instituicao
@app.route('/instituicao/add')
def instituicaoAdd():
	try:
		return render_template('operations.html', title= 'Inserir Instituicao', name= 'Inserir Instituicao', action= url_for('instituicaoAddDB'), \
			values= {'nome': 'Nome', 'tipo': 'Tipo', 'num_regiao': 'Numero de Regiao', 'num_concelho': 'Numero de Concelho'})
	except Exception as e:
		return render_template('returnMainPage.html', text=str(e))
	
@app.route('/instituicao/add', methods=['POST'])
def instituicaoAddDB():
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		query = 'INSERT INTO instituicao VALUES (%s, %s, %s, %s);'
		cursor.execute(query, (request.form['nome'], request.form['tipo'], request.form['num_regiao'], request.form['num_concelho']))
		return render_template('returnMainPage.html', title= 'Resultado de Inserir Instituicao', text='Instituicao inserida com sucesso :)')
	except Exception as e:
		return render_template('returnMainPage.html', text=str(e))
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()


# Editar Instituicao
@app.route('/instituicao/edit')
def instituicaoEdit():
	try:
		return render_template('operations.html', name= 'Editar Instituicao', action= url_for('instituicaoEditDB'),\
			edit= {'nome': 'Nome da Instituicao a editar'},\
			values= {'tipo': 'Tipo', 'num_regiao': 'Numero de Regiao', 'num_concelho': 'Numero de Concelho'})
	except Exception as e: 
		return render_template('returnMainPage.html', text=str(e))
	
@app.route('/instituicao/edit', methods=['POST'])
def instituicaoEditDB():
	edits = ('nome',)
	attr = ('tipo', 'num_regiao', 'num_concelho')
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)

		# query
		query_set = 'UPDATE instituicao SET'
		query_where = ' WHERE'
		args_set = tuple()
		args_where = tuple()
		for key in request.form:
			if key in edits and request.form[key] == '':
				raise Exception("Inserir a chave completa da Instituicao a editar") 
			elif request.form[key] != '':  
				if key in attr:
					idx = attr.index(key)  # if index not found raise exception   
					query_set += ' ' + attr[idx] + '=%s,'
					args_set += (request.form[key], )
				elif key in edits:
					idx = edits.index(key)   # if index not found raise exception   
					query_where += ' ' + edits[idx] + '=%s AND'
					args_where += (request.form[key], )
				# else ignore if key is not recognized

		if not args_set:
			raise Exception("Inserir pelo menos um parametro a alterar")
		
		query_set = query_set[:-1]
		query_where = query_where[:-4]
		query = query_set + query_where + ';'
		args = tuple()
		args = args_set + args_where
		print(cursor.mogrify(query, args))
		cursor.execute(query, args)

		# results
		if cursor.rowcount == 0:
			return render_template('returnMainPage.html', text='Instituicao a editar nao existente :/')
		else:
			return render_template('returnMainPage.html', text='Instituicao editada com sucesso :)')

	except Exception as e:
		dbConn.rollback()
		return render_template('returnMainPage.html', text=str(e))
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()


# Remover instituicao
@app.route('/instituicao/remove')
def instituicaoRm():
	try:
		return render_template('operations.html', name='Remover instituicao', action=url_for('instituicaoRmDB'),\
			values= {'nome': 'Nome da Instituicao'})
	except Exception as e: 
		return render_template('returnMainPage.html', text=str(e))

@app.route('/instituicao/remove', methods=['POST'])
def instituicaoRmDB():
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		query = 'DELETE FROM venda_farmacia WHERE inst=(%s);'
		cursor.execute(query, (request.form['nome'], ))
		query = 'DELETE FROM analise WHERE inst=(%s);'
		cursor.execute(query, (request.form['nome'], ))
		query = 'SELECT num_cedula, num_doente, _data FROM consulta WHERE nome_instituicao=(%s);'
		cursor.execute(query, (request.form['nome'], ))
		consulta = cursor.fetchall()
		for entry in consulta:
			query = 'DELETE FROM prescricao WHERE num_cedula=(%s) AND num_doente=(%s) AND _data=(%s);'
			cursor.execute(query, entry)
			query = 'DELETE FROM analise WHERE num_cedula=(%s) AND num_doente=(%s) AND _data=(%s);'
			cursor.execute(query, entry)
		query = 'DELETE FROM consulta WHERE nome_instituicao=(%s);'
		cursor.execute(query, (request.form['nome'], ))
		query = 'DELETE FROM instituicao WHERE nome=(%s);'
		cursor.execute(query, (request.form['nome'], ))
		return render_template('returnMainPage.html', text='Instituicao removida com sucesso :)')
	except Exception as e:
		dbConn.rollback()
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

@app.route('/medico/add', methods=['POST'])
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
	try:
		return render_template('operations.html', name= 'Editar Medico', action= url_for('medicoEditDB'),\
			edit= {'num_cedula': 'Numero de Cedula a editar'},\
			values= {'nome': 'Nome do Medico', 'especialidade': 'Especialidade'})
	except Exception as e: 
		return render_template('returnMainPage.html', text=str(e))
	
@app.route('/medico/edit', methods=['POST'])
def medicoEditDB():
	edits = ('num_cedula',)
	attr = ('nome', 'especialidade')
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)

		# query
		query_set = 'UPDATE medico SET'
		query_where = ' WHERE'
		args_set = tuple()
		args_where = tuple()
		for key in request.form:
			print(key)
			if key in edits and request.form[key] == '':
				raise Exception("Inserir a chave completa do Medico a editar.") 
			elif request.form[key] != '':  
				if key in attr:
					idx = attr.index(key)   # if index not found raise exception   
					query_set += ' ' + attr[idx] + '=%s,'
					args_set += (request.form[key], )
				elif key in edits:
					idx = edits.index(key)   # if index not found raise exception   
					query_where += ' ' + edits[idx] + '=%s AND'
					args_where += (request.form[key], )

		if not args_set:
			raise Exception("Inserir pelo menos um parametro a alterar")
		query_set = query_set[:-1]
		query_where = query_where[:-4]
		query = query_set + query_where + ';'
		args = tuple()
		args = args_set + args_where
		print(cursor.mogrify(query, args))
		cursor.execute(query, args)

		# results
		if cursor.rowcount == 0:
			return render_template('returnMainPage.html', text='Medico a editar nao existente :/')
		else:
			return render_template('returnMainPage.html', text='Medico editado com sucesso :)')

	except Exception as e:
		dbConn.rollback()
		return render_template('returnMainPage.html', text=str(e))
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

@app.route('/medico/remove')
def medicoRm():
	try:
		return render_template('operations.html', name='Remover medico', action=url_for('medicoRmDB'),\
			values= {'num_cedula': 'Numero de Cedula'})
	except Exception as e: 
		return render_template('returnMainPage.html', text=str(e))

@app.route('/medico/remove', methods=['POST'])
def medicoRmDB():
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		query = 'DELETE FROM analise WHERE num_cedula=(%s);'
		cursor.execute(query, (request.form['num_cedula'], ))
		query = 'DELETE FROM prescricao_venda WHERE num_cedula=(%s);'
		cursor.execute(query, (request.form['num_cedula'], ))
		query = 'DELETE FROM prescricao WHERE num_cedula=(%s);'
		cursor.execute(query, (request.form['num_cedula'], ))
		query = 'DELETE FROM consulta WHERE num_cedula=(%s);'
		cursor.execute(query, (request.form['num_cedula'], ))
		query = 'DELETE FROM medico WHERE num_cedula=(%s);'
		cursor.execute(query, (request.form['num_cedula'], ))
		return render_template('returnMainPage.html', text='Medico removido com sucesso :)')
	except Exception as e:
		dbConn.rollback()
		return render_template('returnMainPage.html', text=str(e))
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

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


@app.route('/prescricao/add', methods=['POST'])
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
	try:
		return render_template('operations.html', name= 'Editar Prescricao', action= url_for('prescricaoEditDB'),\
			edit= {'num_cedula': 'Numero de Cedula a editar', 'num_doente': 'Numero de Doente a editar', \
					'data': 'Data a Editar', 'substancia': 'Substancia a Editar'},\
			values= {'quant': 'Nova Quantidade'})
	except Exception as e: 
		return render_template('returnMainPage.html', text=str(e))
	
@app.route('/prescricao/edit', methods=['POST'])
def prescricaoEditDB():
	edits = ('num_cedula', 'num_doente', '_data' ,'substancia')
	attr = ('quant', )
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)

		# query
		query_set = 'UPDATE prescricao SET'
		query_where = ' WHERE'
		args_set = tuple()
		args_where = tuple()
		for key in request.form:
			print(key)
			if key in edits and request.form[key] == '':
				raise Exception("Inserir a chave completa da prescricao a editar.") 
			elif request.form[key] != '':  
				if key in attr:
					idx = attr.index(key)   # if index not found raise exception   
					query_set += ' ' + attr[idx] + '=%s,'
					args_set += (request.form[key], )
				elif key in edits:
					idx = edits.index(key)   # if index not found raise exception   
					query_where += ' ' + edits[idx] + '=%s AND'
					args_where += (request.form[key], )

		if not args_set:
			raise Exception("Inserir pelo menos um parametro a alterar")
		query_set = query_set[:-1]
		query_where = query_where[:-4]
		query = query_set + query_where + ';'
		args = tuple()
		args = args_set + args_where
		print(cursor.mogrify(query, args))
		cursor.execute(query, args)

		# results
		if cursor.rowcount == 0:
			return render_template('returnMainPage.html', text='Prescricao a editar nao existente :/')
		else:
			return render_template('returnMainPage.html', text='Prescricao editada com sucesso :)')

	except Exception as e:
		dbConn.rollback()
		return render_template('returnMainPage.html', text=str(e))
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

@app.route('/prescricao/remove')
def prescricaoRm():
	try:
		return render_template('operations.html', name='Remover Prescricao', action=url_for('prescricaoRmDB'),\
			values= {'num_cedula': 'Numero de Cedula', 'num_doente': 'Numero de Doente', '_data': 'Data', 'substancia': 'Substancia'})
	except Exception as e: 
		return render_template('returnMainPage.html', text=str(e))

@app.route('/prescricao/remove', methods=['POST'])
def prescricaoRmDB():
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		query = 'DELETE FROM prescricao_venda WHERE num_cedula=(%s) AND num_doente=(%s) AND _data=(%s) AND substancia=(%s);'
		cursor.execute(query, (request.form['num_cedula'], request.form['num_doente'], request.form['_data'], request.form['substancia']))
		query = 'DELETE FROM prescricao WHERE num_cedula=(%s) AND num_doente=(%s) AND _data=(%s) AND substancia=(%s);'
		cursor.execute(query, (request.form['num_cedula'], request.form['num_doente'], request.form['_data'], request.form['substancia']))
		return render_template('returnMainPage.html', text='Prescricao removida com sucesso :)')
	except Exception as e:
		dbConn.rollback()
		return render_template('returnMainPage.html', text=str(e))
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()


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

@app.route('/analise/add', methods=['POST'])
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
	try:
		return render_template('operations.html', name= 'Editar Analise', action= url_for('analiseEditDB'), edit={'num_analise_edit': 'Numero de Analise a editar'},\
			values= {'num_analise': 'Numero de Analise', 'especialidade': 'Especialidade','num_cedula': 'Numero de Cedula',\
			'num_doente': 'Numero de Doente', '_data': 'Data', 'data_registo': 'Data de Registo', 'nome': 'Nome', 'quant': 'Quantidade', 'inst': 'Instituicao'})
	except Exception as e: 
		return render_template('returnMainPage.html', text=str(e))
	
@app.route('/analise/edit', methods=['POST'])
def analiseEditDB():
	attr = ('num_analise_edit', 'num_analise', 'especialidade' ,'num_cedula', 'num_doente', '_data', 'data_registo', 'nome', 'quant', 'inst')
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)

		# query
		query = 'UPDATE analise SET'
		args = tuple()
		for key in request.form:
			if key == 'num_analise_edit' and request.form[key] == '':
				raise Exception("Inserir analise a editar.") 
			elif key == 'num_analise_edit':
				continue
			elif request.form[key] != '':  
				idx = attr.index(key)   # if index not found raise exception   
				query += ' ' + attr[idx] + '=%s,'
				args += (request.form[key], )
		
		query = query[:-1]
		query += ' WHERE num_analise=%s;'
		args += (request.form['num_analise_edit'], )
		print(query%args)        
		cursor.execute(query, args)

		# results
		if cursor.rowcount == 1:
			return render_template('returnMainPage.html', text='Analise editada com sucesso :)')
		else:
			return render_template('returnMainPage.html', text='Analise a editar nao existente :/')

	except Exception as e:
		dbConn.rollback()
		return render_template('returnMainPage.html', text=str(e))
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

@app.route('/analise/remove')
def analiseRm():
	try:
		return render_template('operations.html', name='Remover Analise', action=url_for('analiseRmDB'),\
			values= {'num_analise': 'Numero de Analise'})
	except Exception as e: 
		return render_template('returnMainPage.html', text=str(e))

# /instituicoes/remove?nome="qq"&data=      {"nome": "qq"}
@app.route('/analise/remove', methods=['POST'])
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

@app.route('/listSub', methods=['POST'])
def listarSubstanciasDB():
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		query = 'SELECT substancia FROM prescricao, EXTRACT(YEAR FROM _data) AS ano, EXTRACT(MONTH FROM _data) AS mes WHERE num_cedula = %s AND mes = %s AND ano = %s;'
		cursor.execute(query, (request.form['num_cedula'], request.form['mes'], request.form['ano']))
		#return ":)"
		# print([desc[0] for desc in cursor.description])
		# print([record for record in cursor])
		return render_template('list.html', header='Substancias:', cursor=cursor)
	except Exception as e:
		print(str(e))
		return render_template('returnMainPage.html', text='Argumentos invalidos.')
	finally:
		cursor.close()
		dbConn.close()


@app.route('/listGli')
def listarGlicemia():
	queryHead = "WITH EG(num_regiao, num_concelho, num_doente, quant) AS \
				(SELECT I.num_regiao, I.num_concelho, A.num_doente, A.quant\
				FROM instituicao AS I, analise AS A\
				WHERE I.nome = A.inst AND A.nome='Glicémia')"

	queryMax = queryHead + "\n" + \
		"SELECT EG.num_regiao, EG.num_concelho, EG.num_doente, EG.quant\
		FROM EG, (\
			SELECT num_regiao, num_concelho, MAX(quant) AS maxQ\
			FROM EG\
			GROUP BY (num_regiao, num_concelho)\
			) AS M\
		WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.maxQ\
		ORDER BY (EG.num_regiao, EG.num_concelho);"

	queryMin = queryHead + "\n" + \
		"SELECT EG.num_regiao, EG.num_concelho, EG.num_doente, EG.quant\
		FROM EG, (\
			SELECT num_regiao, num_concelho, MIN(quant) AS minQ\
			FROM EG\
			GROUP BY (num_regiao, num_concelho)\
			) AS M\
		WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.minQ\
		ORDER BY (EG.num_regiao, EG.num_concelho);"

	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		cursor.execute(queryMax)
		maxVect = cursor.fetchall()
		cursor.execute(queryMin)
		minVect = cursor.fetchall()

		resVect = [] #[[num_reg, num_concelho, [num_doenteMIN,..], minQuant, [num_doenteMAX,..], maxQuant]]

		while len(minVect) != 0 and len(maxVect) != 0:
			newVect = []
			newMinDoeVect = []
			newMinQuan = 0
			newMaxDoeVect = []
			newMaxQuan = 0

			newVect = maxVect[0][:2] # [num_reg, num_concelho]
			
			while len(maxVect) != 0:
				maxlst = maxVect[0]
				if newVect[0] != maxlst[0] or newVect[1] != maxlst[1]: #numReg e numConc diferentes
					break

				newMaxDoeVect.append(maxlst[2]) 	# add num_doente e quantidade
				newMaxQuan = maxlst[3]
				maxVect = maxVect[1:]		# update vector

			while len(minVect) != 0:
				minlst = minVect[0]
				if newVect[0] != minlst[0] or newVect[1] != minlst[1]: #numReg e numConc diferentes
					break

				newMinDoeVect.append(minlst[2]) 	# add num_doente e quantidade
				newMinQuan = minlst[3]
				minVect = minVect[1:]		# update vector

			newVect.append(newMinDoeVect)
			newVect.append(newMinQuan)
			newVect.append(newMaxDoeVect)
			newVect.append(newMaxQuan)

			resVect.append(newVect)

		return render_template('listdouble.html', header='Glicemia Minimo e Maximo por Concelho:', data=resVect)
	except Exception as e:
		return render_template('returnMainPage.html', text=str(e))
	finally:
		cursor.close()
		dbConn.close()



@app.route('/venda')
def vendaFarm():
	try:
		return render_template('operations.html', name='Venda Farmacia', action=url_for('vendaFarmDB'),\
			values = {'substancia': 'Substancia', 'quant': 'Quantidade', 'preco': 'Preco', 'inst': 'Instituicao', 'num_doente': 'Numero de Doente'})
	except Exception as e:
		 return render_template('returnMainPage.html', text=str(e))


def inserirVendaFarm(cursor, request):	
	attr = ('substancia', 'quant', 'preco' ,'inst')

	# get num_venda
	query = 'SELECT MAX(num_venda) FROM venda_farmacia;'
	cursor.execute(query)
	num_venda = cursor.fetchone()[0] + 1

	# data de hoje
	today = date.today()
	data_registo = today.strftime("%Y-%m-%d")
	
	# query venda_farmacia
	queryhead = 'INSERT INTO venda_farmacia ('
	querytail = 'VALUES ('
	args = tuple()
	for key in request.form:
		if key == 'num_doente':
			continue
		elif request.form[key] != '':  
			idx = attr.index(key)   # if index not found raise exception   
			queryhead += attr[idx] + ', '
			querytail += '%s, '
			args += (request.form[key], )
	
	queryhead += 'num_venda, data_registo) '
	querytail += '%s, %s);'
	args += (num_venda, data_registo)
	query = queryhead + querytail
	print(query%args)        
	cursor.execute(query, args)
	return num_venda

def inserirPrescrVenda(cursor, request, num_venda, num_doente):
	queryVenda = 'SELECT substancia , quant FROM venda_farmacia WHERE num_venda = ' + str(num_venda)
	cursor.execute(queryVenda)
	res = cursor.fetchone()
	subst = res[0]
	quant_venda = res[1]

	queryPresc = 'SELECT num_cedula, _data, quant FROM prescricao WHERE num_doente = %s AND substancia = %s AND quant >= %s' 
	cursor.execute(queryPresc, (num_doente, subst, quant_venda))
	
	if cursor.rowcount == 0:
		return "Doente nao tem prescricao valida associada. \nVenda Farmacia realizada com sucesso."
	else:
		presc = cursor.fetchone()
		query = 'INSERT INTO prescricao_venda VALUES (%s, %s, %s, %s, %s);'
		cursor.execute(query, (presc[0], num_doente, presc[1], subst, num_venda))

		# Atualiza valor da quantidade da prescricao
		quant_presc = presc[2]
		quant = quant_presc - quant_venda 
		query = 'UPDATE prescricao SET quant=%s WHERE num_cedula=%s AND num_doente=%s AND _data=%s AND substancia=%s;'
		cursor.execute(query, (quant, presc[0], num_doente, presc[1], subst))

		return "Doente tem prescricao valida associada. \nPrescricao Venda e Venda Farmacia realizadas com sucesso."

	
		
@app.route('/venda', methods=['POST'])
def vendaFarmDB():
	
	dbConn=None
	cursor=None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		
		# inserir venda_farmacia
		num_venda = inserirVendaFarm(cursor, request)
		
		# query prescricao
		if request.form['num_doente'] != '':
			resStr = inserirPrescrVenda(cursor, request, num_venda, request.form['num_doente'])
		else:
			resStr = "Venda Farmacia realizada com sucesso."
		
		return render_template('returnMainPage.html', text=resStr)

	except Exception as e:
		dbConn.rollback()
		return render_template('returnMainPage.html', text=str(e))
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()



if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0')
