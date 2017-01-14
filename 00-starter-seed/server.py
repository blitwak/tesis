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
from sortedcontainers import SortedList
import heapq
#from flask import Markup
#https://pythonhosted.

# from gevent.wsgi import WSGIServer

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
    perfilDeTwitterID = db.IntField()
    choice = db.StringField()
    perfilDeTwitterScreenName = db.StringField()

class perfilesBD (db.Document):
	perfilDeTwitterScreenName = db.StringField()
	perfilDeTwitterID = db.IntField()
	yaDecidido = db.BoolField()


#db.registro.find().count()
#use test
#mongo --shell
#db.bios.remove( { } )

global cantPerfilesAmostrar
cantPerfilesAmostrar = 10

global cantidadesHeap
cantidadesHeap = []
heapq.heapify(cantidadesHeap)             # for a min heap
heapq._heapify_max(cantidadesHeap)        # for a maxheap!!
#cantidadesHeap = SortedList()
#http://stackoverflow.com/questions/2501457/what-do-i-use-for-a-max-heap-implementation-in-python
#https://pymotw.com/2/heapq/

global dicCantidadTOperfilesTwitter
dicCantidadTOperfilesTwitter = {}


def levantarPerfilesDeTwitter():
#	filename = "/var/www/twitterAmostrarCopaArgentina.p"
#	filename = "bd/twitterAmostrar3.p"
    filename = "bd/twitterAmostrarCopaArgentina.p"
    if os.path.isfile(filename):
		filehandler = open(filename,'rb')
		dic = pickle.load(filehandler)
		filehandler.close()
#        ret = preparar.armarGrupos(dic,cantPerfilesAmostrar)
		return dic

global perfilesDeTwitter
perfilesDeTwitter = levantarPerfilesDeTwitter()

global posiblesClaves
posiblesClaves = perfilesDeTwitter.keys()

for perfilDeTwitterKEY in posiblesClaves:
	perfilDeTwitterScreenName1 = perfilesDeTwitter[perfilDeTwitterKEY][1]
	print perfilDeTwitterScreenName1
	yaDecidido1 = False
	unPerfilBD = perfilesBD(perfilDeTwitterScreenName = perfilDeTwitterScreenName1, perfilDeTwitterID= perfilDeTwitterKEY, yaDecidido = yaDecidido1)
	unPerfilBD.save()


print "la cantidad de claves es " + str(len(posiblesClaves))

global dicColaboradorToPerfilesVistos
dicColaboradorToPerfilesVistos = {}

global dicColaboradorToUltimoVisto
dicColaboradorToUltimoVisto = {}

global dicperfilTwitterToCantidades
dicperfilTwitterToCantidades = {}

global dicColaboradorToprogessBar
dicColaboradorToprogessBar = {}

# global dicPerfilToDecidido
# dicPerfilToDecidido = {}

# for posibleClave in posiblesClaves:
#     dicPerfilToDecidido[posibleClave] = False


def obtenerPerfilAmirar(nameColaborador):
    vistosPorColaborador = dicColaboradorToPerfilesVistos[nameColaborador]
    for posiblePerfil in posiblesClaves:
        if(posiblePerfil not in vistosPorColaborador):
            return posiblePerfil
    print "No hay mas perfiles"
    return null


def armarMensaje(clave):
    global perfilesDeTwitter
    perfil = perfilesDeTwitter[clave]
    dic = {}
    dic["id"]= clave
    dic["name"]= perfil[0]
    dic["screenName"]= perfil[1]
    dic["desc"]= perfil[2]
    dic["banner"]= perfil[3]
    dic["image"]= perfil[4]
    print dic 
    return json.dumps(dic),perfil[1]


def hayMayoriaDeEquipo(listaVotacion):
    equipoSeleccionado = {}
    for seleccion in listaVotacion:
        equipo = seleccion[1]
        if (equipo in equipoSeleccionado.keys()):
            equipoSeleccionado[equipo] = equipoSeleccionado[equipo] + 1
        else:
            equipoSeleccionado[equipo] = 1
    cantVotantes = len(listaVotacion)
    limite = cantVotantes * 0.8
    for votado in equipoSeleccionado.keys():
        cantidadVotos = equipoSeleccionado[votado]
        if(cantidadVotos >= limite):
            print "Ya esta decidido"
            return True
    return False

print len(perfilesDeTwitter)

# global clavesJson
# clavesJson = ["Primero","Segundo","Tercero","Cuarto","Quinto","Sexto"]

# global dicPerfilesDeTwitterToCantidadVistos
# dicPerfilesDeTwitterToCantidadVistos = {}

# global dicEsclavoToPerfilesTwitterVistos
# dicEsclavoToPerfilesTwitterVistos = {} #user->idTwitterCuenta

# global dicEsclavoToPerfilesAver
# dicEsclavoToPerfilesAver = {}

# global dicEsclavoToUltimoVisto
# dicEsclavoToUltimoVisto = {}

global dicColaboradorToTuplasSeleccionadas
dicColaboradorToTuplasSeleccionadas = {} # user -> idTwitterCuenta,choice
global dicidTwitterCuentaToVotacion
dicidTwitterCuentaToVotacion = {} #idTwitterCuenta ->user,choice
# asd = 0
# Define a route for the default URL, which loads the form

# Requires authentication decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
 #       print "que onda?"
        if constants.PROFILE_KEY not in session:
            print "vamo a index"
            session.clear()
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
#    global dicEsclavoToPerfilesAver
 #   global dicEsclavoToPerfilesTwitterVistos
  #  global dicUserToTuplasSeleccionadas

	global dicColaboradorToTuplasSeleccionadas
	global dicColaboradorToPerfilesVistos
	global dicColaboradorToUltimoVisto
	global dicColaboradorToprogessBar
	global dicColaboradorToUltimoVisto


	nameColaborador = session[constants.PROFILE_KEY]['nickname']
	print nameColaborador

	if nameColaborador not in dicColaboradorToPerfilesVistos.keys():
		dicColaboradorToPerfilesVistos[nameColaborador]= []

	if nameColaborador not in dicColaboradorToTuplasSeleccionadas.keys():
		dicColaboradorToTuplasSeleccionadas[nameColaborador]= []

	perfilDeTwitterID = obtenerPerfilAmirar(nameColaborador)

	msg, perfilDeTwitterScreenName = armarMensaje(perfilDeTwitterID)


	if (nameColaborador in dicColaboradorToprogessBar.keys()):
		cantidadPerfilesAnalizados = dicColaboradorToprogessBar[nameColaborador]
	else:
		dicColaboradorToprogessBar[nameColaborador] = 0
		cantidadPerfilesAnalizados = 0

	dicColaboradorToUltimoVisto[nameColaborador] = [perfilDeTwitterID,perfilDeTwitterScreenName]

	return render_template('jugar.html',env=env, perfiles = msg, nombreDelUsuario = perfilDeTwitterScreenName,cantidadPerfilesAnalizados = cantidadPerfilesAnalizados)


@app.route('/yajugue', methods=['POST'])
def yajugue():
    global dicColaboradorToTuplasSeleccionadas
    global dicColaboradorToprogessBar
    global posiblesClaves
    global dicColaboradorToPerfilesVistos
    global dicidTwitterCuentaToVotacion

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
        elif(btn == "Estudiantes"):
            equipoSeleccionado = "Estudiantes"
            print "Estudiantes"
        elif(btn == "Gimnasia"):
            equipoSeleccionado = "Gimnasia"
            print "Gimnasia"
        else:
            print "boom"
    else:
        print "No"
    nameColaborador = session['username']
    print nameColaborador

    [perfilDeTwitterID,perfilDeTwitterScreenName] = dicColaboradorToUltimoVisto[nameColaborador]
    print perfilDeTwitterID



    dicColaboradorToPerfilesVistos[nameColaborador].append(perfilDeTwitterID)
    dicColaboradorToTuplasSeleccionadas[nameColaborador].append([perfilDeTwitterID,equipoSeleccionado])

    if (perfilDeTwitterID not in dicidTwitterCuentaToVotacion.keys()):
        dicidTwitterCuentaToVotacion[perfilDeTwitterID] = []

    elementito = [nameColaborador,equipoSeleccionado]
    dicidTwitterCuentaToVotacion[perfilDeTwitterID].append(elementito)

    if( len(dicidTwitterCuentaToVotacion[perfilDeTwitterID]) > 10):
        posiblesClaves.remove(perfilDeTwitterID)

        aModificar = perfilesBD.query.filter(perfilesBD.perfilDeTwitterID == perfilDeTwitterID).first()
        aModificar.yaDecidido = True
        aModificar.save()

	elif( len(dicidTwitterCuentaToVotacion[perfilDeTwitterID]) > 4):
		if(hayMayoriaDeEquipo(dicidTwitterCuentaToVotacion[perfilDeTwitterID])):
			#borro de posibles claves
			posiblesClaves.remove(perfilDeTwitterID)
			aModificar = perfilesBD.query.filter(perfilesBD.perfilDeTwitterID == perfilDeTwitterID).first()
			aModificar.yaDecidido = True
			aModificar.save()




    agregar = registro(colaborador= nameColaborador ,perfilDeTwitterID= perfilDeTwitterID,choice=equipoSeleccionado,perfilDeTwitterScreenName = perfilDeTwitterScreenName)
    agregar.save()

    cantidadPerfilesAnalizados = dicColaboradorToprogessBar[nameColaborador]
    cantidadPerfilesAnalizados = cantidadPerfilesAnalizados + 1

    if(cantidadPerfilesAnalizados == 10):
        dicColaboradorToprogessBar[nameColaborador] = 0
        return render_template('finJuego.html',env=env, user=nameColaborador)
    else:
        perfilDeTwitterID = obtenerPerfilAmirar(nameColaborador)
        msg, perfilDeTwitterScreenName = armarMensaje(perfilDeTwitterID)
        dicColaboradorToUltimoVisto[nameColaborador] = [perfilDeTwitterID,perfilDeTwitterScreenName]
        dicColaboradorToprogessBar[nameColaborador] = cantidadPerfilesAnalizados
        return render_template('jugar.html',env=env, perfiles = msg, nombreDelUsuario = perfilDeTwitterScreenName, cantidadPerfilesAnalizados=cantidadPerfilesAnalizados)

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
	# http_server = WSGIServer(('', 3000), app)
	# http_server.serve_forever()