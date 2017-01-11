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
import codecs

#https://pythonhosted.

# Load Env variables
env = None

try:
    env = Dotenv('./.env')
except IOError:
    env = os.environ

app = Flask(__name__, static_url_path='')
app.secret_key = constants.SECRET_KEY

#https://pythonhosted.org/Flask-MongoAlchemy/

app.config["AWS_ACCESS_KEY_ID"] = constants.AWS_ACCESS_KEY_ID
app.config["AWS_SECRET_ACCESS_KEY"] = constants.AWS_SECRET_ACCESS_KEY

app.config['MONGOALCHEMY_DATABASE'] = constants.MONGOALCHEMY_DATABASE
db = MongoAlchemy(app)
app.debug = True

class registro(db.Document):
	colaborador = db.StringField()
	perfilDeTwitter = db.IntField()
	choice = db.StringField()


global cantPerfilesAmostrar
cantPerfilesAmostrar = 10

def levantarPerfilesDeTwitter():
#	filename = "/var/www/twitterAmostrarCopaArgentina.p"
	filename = "bd/twitterAmostrar.p"
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

global dicEsclavoToUltimoVisto
dicEsclavoToUltimoVisto = {}

global dicUserToTuplasSeleccionadas
dicUserToTuplasSeleccionadas = {} # user -> idTwitterCuenta,choice
global dicidTwitterCuentaToVotacion
dicidTwitterCuentaToVotacion = {} #idTwitterCuenta ->user,choice
asd = 0
# Define a route for the default URL, which loads the form

# Requires authentication decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated


# Controllers API
@app.route('/')
@app.route('/login', methods=['POST','GET'])
def login():
    return render_template('login.html', env=env)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return render_template('login.html', env=env)


@app.route('/public/<path:filename>')
def static_files(filename):
    return send_from_directory('./public', filename)

@app.route('/index', methods=['POST','GET'])
@requires_auth
def index():
    print "paso por aca si iii"
    return render_template('index.html',
                           user=session[constants.PROFILE_KEY], env=env)


#@app.route('/dashboard')
#@requires_auth
#def dashboard():
#    return render_template('dashboard.html', user=session[constants.PROFILE_KEY])



@app.route('/jugarPrimeraVez', methods=['POST'])
def jugarPrimeraVez():
    global dicEsclavoToPerfilesAver
    global dicEsclavoToPerfilesTwitterVistos
    global asd
    global dicUserToTuplasSeleccionadas

    name = session[constants.PROFILE_KEY]['nickname']
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

    global dicEsclavoToUltimoVisto
    dicEsclavoToUltimoVisto[name] = perfilAenviar
    return render_template('jugar.html',env=env, perfiles = msg, nombreDelUsuario = twitterPerf)


@app.route('/yajugue', methods=['POST'])
def yajugue():
    global asd
    global dicEsclavoToPerfilesTwitterVistos
    global dicUserToTuplasSeleccionadas
    global dicidTwitterCuentaToVotacion
    global dicEsclavoToPerfilesAver
    global dicEsclavoToUltimoVisto


    formulario = request.form
    if("btn1" in formulario):
        btn=request.form['btn1']
        print btn
        if(btn== 'No se'):
            print "No se"
            equipoSeleccionado = "No se"
        elif(btn == "Ninguno"):
            print "Ninguno"
            equipoSeleccionado = "Ninguno"
        elif(btn == "Boca"):
            print "Boca"
            equipoSeleccionado = "Boca"
        elif(btn == "River"):
            print "River"
            equipoSeleccionado = "River"
        elif(btn == "Racing"):
            print "Racing"
            equipoSeleccionado = "Racing"
        elif(btn == "Independiente"):
            equipoSeleccionado = "Independiente"
            print "Independiente"
        elif(btn == "San Lorenzo"):
            equipoSeleccionado = "San Lorenzo"
            print "San Lorenzo"
        elif(btn == "Huracan"):
            equipoSeleccionado = "Huracan"
            print "Huracan"
        elif(btn == "Belgrano"):
            equipoSeleccionado = "Belgrano"
            print "Belgrano"
        elif(btn == "Talleres"):
            equipoSeleccionado = "Talleres"
            print "Talleres"
        elif(btn == "Rosario central"):
            equipoSeleccionado = "Rosario central"
            print "Rosario central"
        elif(btn == "Newell's"):
            equipoSeleccionado = "Newell's"
            print "Newell's"
        elif(btn == "Estudiantes de la plata"):
            equipoSeleccionado = "Estudiantes de la plata"
            print "Estudiantes de la plata"
        elif(btn == "Gimnasia"):
            equipoSeleccionado = "Gimnasia"
            print "Gimnasia"
        elif(btn == "Colon"):
            equipoSeleccionado = "Colon"
            print "Colon"
        elif(btn == "Velez"):
            equipoSeleccionado = "Velez"
            print "Velez"
        elif(btn == "Lanus"):
            equipoSeleccionado = "Lanus"
            print "Lanus"
        elif(btn == "Banfield"):
            equipoSeleccionado = "Banfield"
            print "Banfield"
        elif(btn == "Atletico Tucuman"):
            equipoSeleccionado = "Atletico Tucuman"
            print "Atlético Tucumán"
        elif(btn == "Temperley"):
            equipoSeleccionado = "Temperley"
            print "Temperley"
        elif(btn == "Union"):
            equipoSeleccionado = "Union"
            print "Union"
        elif(btn == "Tigre"):
            equipoSeleccionado = "Tigre"
            print "Tigre"
        else:
            print "boom"
    else:
        print "No"
    name = session['username']
    perfilVisto = dicEsclavoToUltimoVisto[name]
    print name
    print perfilVisto

    dicEsclavoToPerfilesTwitterVistos[name].append(perfilVisto)
    dicUserToTuplasSeleccionadas[name].append([perfilVisto,equipoSeleccionado])

    if (perfilVisto not in dicidTwitterCuentaToVotacion.keys()):
        dicidTwitterCuentaToVotacion[perfilVisto] = []
        print "agregado"

    elementito = [name,equipoSeleccionado]
    dicidTwitterCuentaToVotacion[perfilVisto].append(elementito)

    agregar = registro(colaborador= name ,perfilDeTwitter= perfilVisto,choice=equipoSeleccionado)
    agregar.save()

    perfiles = dicEsclavoToPerfilesAver[name]

    if(len(perfiles) > 0):
        perfilAenviar = perfiles[0]
        dicEsclavoToPerfilesAver[name]=perfiles[1:]
        msg, twitterPerf = preparar.armarMensaje(perfilAenviar,perfilesDeTwitter)
        dicEsclavoToUltimoVisto[name] = perfilAenviar
        return render_template('jugar.html',env=env, perfiles = msg, nombreDelUsuario = twitterPerf)
    else:
        return render_template('finJuego.html', user=name, votacion = dicUserToTuplasSeleccionadas[name])


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
    session['username'] = user_info['nickname']
    return redirect('/index')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000))
