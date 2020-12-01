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
	body += "<p><a href='%s'>Listar glicemia</p>\n" %url_for('listarGlicemia')
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
	

@app.route('/instituicao/add', methods=['POST'])
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
@app.route('/instituicao/remove', methods=['POST'])
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
		return render_template('operations.html', name= 'Numero de Analise', action= url_for('analiseEditDB'),\
			values= {'num_analise_edit': 'Numero de Analise a editar', 'num_analise': 'Numero de Analise', 'especialidade': 'Especialidade','num_cedula': 'Numero de Cedula',\
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
		dbConn.commit()
		cursor.close()
		dbConn.close()


@app.route('/listGli')
def listarGlicemia():
	queryHead = "WITH EG(num_regiao, num_concelho, num_doente, quant) AS \
				(SELECT I.num_regiao, I.num_concelho, A.num_doente, A.quant\
				FROM instituicao AS I, analise AS A\
				WHERE I.nome = A.inst AND A.especialidade='Glicémia')"

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

		resVect = [] #[num_reg, num_concelho, [num_doenteMIN,..], minQuant, [num_doenteMAX,..], maxQuant,]

		while len(minVect) != 0 and len(maxVect) != 0:
			newVect = []
			newMinDoeVect = []
			newMinQuan = 0
			newMaxDoeVect = []
			newMaxQuan = 0

			newVect = maxVect[0][:2]
			while len(maxVect) != 0:
				maxlst = maxVect[0]
				if newVect[0] != maxlst[0] or newVect[1] != maxlst[1]: #numReg e numConc diferentes
					break

				while len(minVect) != 0:
					minlst = minVect[0]
					if newVect[0] != minlst[0] or newVect[1] != minlst[1]: #numReg e numConc diferentes
						break

					newMinDoeVect.append(minlst[2]) 	# add num_doente e quantidade
					newMinQuan = minlst[3]
					minVect = minVect[1:]		# update vector

				newMaxDoeVect.append(maxlst[2]) 	# add num_doente e quantidade
				newMaxQuan = maxlst[3]
				maxVect = maxVect[1:]		# update vector

			newVect.append(newMinDoeVect)
			newVect.append(newMinQuan)
			newVect.append(newMaxDoeVect)
			newVect.append(newMaxQuan)

			resVect.append(newVect)


		return render_template('listdouble.html', header='Glicemia Minimo e Maximo por Concelho:', data=resVect)
	except Exception as e:
		return render_template('returnMainPage.html', text=str(e))
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()


if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0')
