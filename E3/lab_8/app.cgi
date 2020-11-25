#!/usr/bin/python3

from flask import Flask
from flask import render_template, request

## Libs postgres
import psycopg2
import psycopg2.extras

app = Flask(__name__)

## SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist192456" 
DB_DATABASE=DB_USER
DB_PASSWORD="psql192456"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)


## Runs the function once the root page is requested.
## The request comes with the folder structure setting ~/web as the root
@app.route('/')
def list_accounts():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT * FROM account;"
    cursor.execute(query)
    return render_template("index.html", cursor=cursor)
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    cursor.close()
    dbConn.close()

@app.route('/accounts')
def list_accounts_edit():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT account_number, branch_name, balance FROM account;"
    cursor.execute(query)
    return render_template("accounts.html", cursor=cursor, params=request.args)
  except Exception as e:
    return str(e) 
  finally:
    cursor.close()
    dbConn.close()

@app.route('/balance')
def alter_balance():
  try:
    return render_template("balance.html", params=request.args)
  except Exception as e:
    return str(e)


@app.route('/update', methods=["POST"])
def update_balance():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    # Esta versão é vuneravel a SQL injection
    query = f'''UPDATE account SET balance={request.form["balance"]} WHERE account_number = '{request.form["account_number"]}';'''
    cursor.execute(query)
    return query
  except Exception as e:
    return str(e) 
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()


if __name__ == '__main__':
  app.run(port=5001)
