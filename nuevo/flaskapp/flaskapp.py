from flask import Flask
from flask import Flask, session, redirect, url_for, escape, request,render_template
import json
import preparar as preparar
import pickle
import os.path
#from flask.ext.pymongo import PyMongo
#from flask_pymongo import PyMongo
#from mongokit import Connection, Document
#from flask.ext.mongoalchemy import MongoAlchemy
from flask_mongoalchemy import MongoAlchemy

#from flask_sqlalchemy import SQLAlchemy
#from boto.dynamodb2.fields import HashKey
#from boto.dynamodb2.table import Table
#from flask.ext.dynamo import Dynamo
#import boto3
#from boto.dynamodb2.layer1 import DynamoDBConnection
#from boto.regioninfo import RegionInfo
app = Flask(__name__)
puerto = 5000
app.secret_key = "holamanolacomova"
#app.SQLALCHEMY_DATABASE_URI = 'sqlite:///students.sqlite3'
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["AWS_ACCESS_KEY_ID"] = "AKIAINSPSQ3GTANJH64A"
app.config["AWS_SECRET_ACCESS_KEY"] = "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"

#https://pythonhosted.org/Flask-MongoAlchemy/
app.config['MONGOALCHEMY_DATABASE'] = 'test'
db = MongoAlchemy(app)

class registro(db.Document):
	colaborador = db.StringField()
	perfilDeTwitter = db.StringField()
	choice = db.StringField()

global asd
asd = 0

global cantPerfilesAmostrar
cantPerfilesAmostrar = 3

def levantarPerfilesDeTwitter():
	filename = "/var/www/twitterAmostrarCopaArgentina.p"
#	filename = "static/bd/twitterAmostrar.p"
	if os.path.isfile(filename):
		filehandler = open(filename,'rb')
		ret = pickle.load(filehandler)
		filehandler.close()
		print "levantada"
		return ret

global perfilesDeTwitter
perfilesDeTwitter = levantarPerfilesDeTwitter()

print len(perfilesDeTwitter)

global clavesJson
clavesJson = ["Primero","Segundo","Tercero","Cuarto","Quinto","Sexto"]

global dicPerfilesDeTwitterToCantidadVistos
dicPerfilesDeTwitterToCantidadVistos = {}

global dicEsclavoToPerfilesTwitterVistos
dicEsclavoToPerfilesTwitterVistos = {} #user->idTwitterCuenta

global dicEsclavoToPerfilesAver
dicEsclavoToPerfilesAver = {}

global dicUserToTuplasSeleccionadas
dicUserToTuplasSeleccionadas = {} # user -> idTwitterCuenta,choice
global dicidTwitterCuentaToVotacion
dicidTwitterCuentaToVotacion = {} #idTwitterCuenta ->user,choice
asd = 0
# Define a route for the default URL, which loads the form

@app.route('/')
@app.route('/login', methods=['POST','GET'])
def login():
    return render_template('login.html')


@app.route('/hello/', methods=['POST'])
def hello():
    name=request.form['yourname']
    email=request.form['youremail']
    return render_template('index.html', name=name, email=email)

@app.route('/hello2', methods=['POST'])
def hello2():
    name=request.form['name']
    return render_template('index.html', name=name)

@app.route('/gracias/', methods=['POST'])
def gracias():
	usuario=request.form['usuario']
	respuestas=request.form['respuestas']
	return render_template('finJuego.html', user=usuario, respuestas= respuestas)


@app.route('/jugarPrimeraVez', methods=['POST'])
def jugarPrimeraVez():
	global dicEsclavoToPerfilesAver
	global dicEsclavoToPerfilesTwitterVistos
	global asd
	global dicUserToTuplasSeleccionadas

	name=request.form['usuario']
	perfiles = preparar.obtenerPerfiles(name,dicEsclavoToPerfilesTwitterVistos,perfilesDeTwitter,dicPerfilesDeTwitterToCantidadVistos,cantPerfilesAmostrar) #perfilesDeTwitter[0:2]    #MIRAR ESTOOOOOOOOOOOOO SELECCION DE PERFILES
	perfilAenviar = perfiles[0]
	print perfiles
	print perfilAenviar
	dicEsclavoToPerfilesAver[name]=perfiles[1:]
	print name
	msg = preparar.armarMensaje(perfilAenviar,perfilesDeTwitter)
	if name not in dicEsclavoToPerfilesTwitterVistos.keys():
		dicEsclavoToPerfilesTwitterVistos[name]= []
		print dicEsclavoToPerfilesTwitterVistos.keys()
		print len(dicEsclavoToPerfilesTwitterVistos)
		print "grabo"
	else:
		print "no grabo"
	print dicEsclavoToPerfilesTwitterVistos.keys() 
	print "-------------------------"
	print asd
	asd = 1
	print asd
	if name not in dicUserToTuplasSeleccionadas.keys():
		dicUserToTuplasSeleccionadas[name]= []
	return render_template('jugar.html', name=name, perfiles = msg)


@app.route('/mostrarTodoRegistro')
def mostrarTodoRegistro():
   return render_template('mostrarTodoRegistro.html', registros = registro.query.all() )


@app.route('/yajugue', methods=['POST'])
def yajugue():
	global asd
	global dicEsclavoToPerfilesTwitterVistos
	global dicUserToTuplasSeleccionadas
	global dicidTwitterCuentaToVotacion
	global dicEsclavoToPerfilesAver

	print "YA jUGUE futbol"
	print request.form
	name=request.form['usuario']
	print name
	seleccionEquipo=request.form['teams']
	print seleccionEquipo
	idTwitterCuenta = request.form['id_datosTwitter']
	print idTwitterCuenta
	print name
	print "-------"
	print asd
	asd = 2
	print asd
	print "-------------------------------------"	
	print name
	print dicEsclavoToPerfilesTwitterVistos.keys()
	asd = dicEsclavoToPerfilesTwitterVistos[name]
	asd.append(idTwitterCuenta)
	dicEsclavoToPerfilesTwitterVistos[name] = asd
	fff = dicUserToTuplasSeleccionadas[name]
	print "antes de un apend"
	fff.append([idTwitterCuenta,seleccionEquipo])
	dicUserToTuplasSeleccionadas[name] = fff

	if (idTwitterCuenta not in dicidTwitterCuentaToVotacion.keys()):
		dicidTwitterCuentaToVotacion[idTwitterCuenta] = []
	print idTwitterCuenta
	dicidTwitterCuentaToVotacion[idTwitterCuenta] = dicidTwitterCuentaToVotacion[idTwitterCuenta].append([name,seleccionEquipo])
	print "antes del commit"
	agregar = registro(colaborador= name ,perfilDeTwitter= idTwitterCuenta,choice=seleccionEquipo)
	agregar.save()
	print"coommit"

	perfiles = dicEsclavoToPerfilesAver[name]    
	if(len(perfiles) > 0):
		perfilAenviar = perfiles[0]
		dicEsclavoToPerfilesAver[name]=perfiles[1:]
		msg = preparar.armarMensaje(perfilAenviar,perfilesDeTwitter)
		return render_template('jugar.html', name=name, perfiles = msg)
	else:
		return render_template('finJuego.html', user=name, votacion = fff)



@app.route('/1')
def hello_world():
	return 'Hello from Flask!'

if __name__ == '__main__':
#  db.create_all()
#  	users = Table.create('elementos', schema=[HashKey('username')]);
	app.run()
