#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from functools import wraps
from dotenv import Dotenv
import json
import preparar as preparar
import pickle
import os.path
import os
import requests
from flask import Flask, request, jsonify, session, redirect, render_template, send_from_directory,url_for, escape
from flask_mongoalchemy import MongoAlchemy
import constants

app = Flask(__name__)
puerto = 5000
app.secret_key = constants.SECRET_KEY

#app.SQLALCHEMY_DATABASE_URI = 'sqlite:///students.sqlite3'
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

app.config["AWS_ACCESS_KEY_ID"] = constants.AWS_ACCESS_KEY_ID
app.config["AWS_SECRET_ACCESS_KEY"] = constants.AWS_SECRET_ACCESS_KEY

#https://pythonhosted.org/Flask-MongoAlchemy/

app.config['MONGOALCHEMY_DATABASE'] = constants.MONGOALCHEMY_DATABASE
db = MongoAlchemy(app)

class registro(db.Document):
	colaborador = db.StringField()
	perfilDeTwitter = db.StringField()
	choice = db.StringField()


global cantPerfilesAmostrar
cantPerfilesAmostrar = 10

# Requires authentication decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated




def levantarPerfilesDeTwitter():
#	filename = "/var/www/twitterAmostrarCopaArgentina.p"
	filename = "static/bd/twitterAmostrar.p"
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
    print "aca"
    return render_template('login.html', env=env)


@app.route('/hello/', methods=['POST'])
def hello():
    name=request.form['yourname']
    email=request.form['youremail']
    return render_template('index.html', name=name, email=email)

@app.route('/comojugar2', methods=['POST'])
def comojugar2():
    print "como jugar22"
    return render_template('login.html')

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
    dicEsclavoToPerfilesAver[name]=perfiles[1:]
    print name
    msg, twitterPerf = preparar.armarMensaje(perfilAenviar,perfilesDeTwitter)
    if name not in dicEsclavoToPerfilesTwitterVistos.keys():
        dicEsclavoToPerfilesTwitterVistos[name]= []
        print "grabo"
    else:
        print "no grabo"
    if name not in dicUserToTuplasSeleccionadas.keys():
        dicUserToTuplasSeleccionadas[name]= []
    return render_template('jugar.html', name=name, perfiles = msg, nombreDelUsuario = twitterPerf)


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
    formulario = request.form
    if("btn1" in formulario):
        btn=request.form['btn1']
        if(btn== 'No se'):
            print "No se"
        elif(btn == "Ninguno"):
            print "Ninguno"
        elif(btn == "Boca"):
            print "Boca"
        elif(btn == "River"):
            print "River"
        elif(btn == "Racing"):
            print "Racing"
        elif(btn == "Independiente"):
            print "Independiente"
        elif(btn == "San Lorenzo"):
            print "San Lorenzo"
        elif(btn == "Huracan"):
            print "Huracan"
        elif(btn == "Belgrano"):
            print "Belgrano"
        elif(btn == "Talleres"):
            print "Talleres"
        elif(btn == "Rosario central"):
            print "Rosario central"
        elif(btn == "Newell's"):
            print "Newell's"
        elif(btn == "Estudiantes de la plata"):
            print "Estudiantes de la plata"
        elif(btn == "Gimnasia"):
            print "Gimnasia"
        elif(btn == "Colon"):
            print "Colon"
        elif(btn == "Velez"):
            print "Velez"
        elif(btn == "Lanus"):
            print "Lanus"
        elif(btn == "Banfield"):
            print "Banfield"
        elif(btn == "Atlético Tucumán".encode(utf-8)):
            print "Atlético Tucumán"
        elif(btn == "Temperley"):
            print "Temperley"
        elif(btn == "Union"):
            print "Union"
        elif(btn == "Tigre"):
            print "Tigre"
        else:
            print "boom"
    else:
        print "No"
    print "basura"
    print session.get('SessionName')
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
    print dicUserToTuplasSeleccionadas.keys()
    print dicidTwitterCuentaToVotacion.keys()
    print dicEsclavoToPerfilesAver.keys()
    print idTwitterCuenta


    #	asd = dicEsclavoToPerfilesTwitterVistos[name]
    #	asd.append(idTwitterCuenta)
    print "asd"
    dicEsclavoToPerfilesTwitterVistos[name].append(idTwitterCuenta)
    print "eee"
    #	dicEsclavoToPerfilesTwitterVistos[name] = asd
    dicUserToTuplasSeleccionadas[name].append([idTwitterCuenta,seleccionEquipo])
    print "ttt"
    #	fff = dicUserToTuplasSeleccionadas[name]
    #	print "antes de un apend"
    #	fff.append([idTwitterCuenta,seleccionEquipo])
    #	dicUserToTuplasSeleccionadas[name] = fff

    if (idTwitterCuenta not in dicidTwitterCuentaToVotacion.keys()):
        dicidTwitterCuentaToVotacion[idTwitterCuenta] = []
        print "agregado"
    print idTwitterCuenta
    elementito = [name,seleccionEquipo]
    print "elementito"
    dicidTwitterCuentaToVotacion[idTwitterCuenta].append(elementito)
    #	dicidTwitterCuentaToVotacion[idTwitterCuenta] = yyyy
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
        return render_template('finJuego.html', user=name, votacion = dicUserToTuplasSeleccionadas[name])

@app.route('/1')
def hello_world():
	return 'Hello from Flask!'



@app.route('/callback')
def callback_handling():
    code = request.args.get(constants.CODE_KEY)
    json_header = {constants.CONTENT_TYPE_KEY: constants.APP_JSON_KEY}
    token_url = 'https://{auth0_domain}/oauth/token'.format(
                    auth0_domain=env[constants.AUTH0_DOMAIN])
    token_payload = {
        constants.CLIENT_ID_KEY: env[constants.AUTH0_CLIENT_ID],
        constants.CLIENT_SECRET_KEY: env[constants.AUTH0_CLIENT_SECRET],
        constants.REDIRECT_URI_KEY: env[constants.AUTH0_CALLBACK_URL],
        constants.CODE_KEY: code,
        constants.GRANT_TYPE_KEY: constants.AUTHORIZATION_CODE_KEY
    }

    token_info = requests.post(token_url, json=token_payload,
                               headers=json_header).json()

    user_url = 'https://{auth0_domain}/userinfo?access_token={access_token}'\
        .format(auth0_domain=env[constants.AUTH0_DOMAIN],
                access_token=token_info[constants.ACCESS_TOKEN_KEY])

    user_info = requests.get(user_url).json()
    session[constants.PROFILE_KEY] = user_info
    return redirect('/login')


if __name__ == '__main__':
#  db.create_all()
#  	users = Table.create('elementos', schema=[HashKey('username')]);
	app.run()
