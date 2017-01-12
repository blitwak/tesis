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
from flask import Markup
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

#db.registro.find().count()
#use test
#mongo --shell
#db.bios.remove( { } )

global cantPerfilesAmostrar
cantPerfilesAmostrar = 10

global cantidadesHeap
cantidadesHeap = SortedList()

global dicCantidadTOperfilesTwitter
dicCantidadTOperfilesTwitter = {}


def levantarPerfilesDeTwitter():
#	filename = "/var/www/twitterAmostrarCopaArgentina.p"
	filename = "bd/twitterAmostrar3.p"
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

global dicColaboradorToPerfilesVistos
dicColaboradorToPerfilesVistos = {}

global dicColaboradorToUltimoVisto
dicColaboradorToUltimoVisto = {}

global dicperfilTwitterToCantidades
dicperfilTwitterToCantidades = {}

global dicColaboradorToprogessBar
dicColaboradorToprogessBar = {}

def obtenerPerfilAmirar(nameColaborador):
    global cantidadesHeap
    global dicCantidadTOperfilesTwitter
    global posiblesClaves
    global dicColaboradorToPerfilesVistos


    cantidadAagregar = []
    vistosPorColaborador = dicColaboradorToPerfilesVistos[nameColaborador]
    bloq=True
    while(True):
        if(len(cantidadesHeap)>0):
            cantidad = cantidadesHeap.pop()
            perfilesDeTwitter = dicCantidadTOperfilesTwitter[cantidad]
            for perilTwitter in perfilesDeTwitter:
                if (perilTwitter not in vistosPorColaborador):
                    for cant in cantidadAagregar:
                        cantidadesHeap.add(cant)    
                    return perilTwitter
            cantidadAagregar.append(cantidad)
        else:
            for cant in cantidadAagregar:
                cantidadesHeap.add(cant)    
            for posibleClave in posiblesClaves:
                if posibleClave not in vistosPorColaborador:
                    if(bloq):
                        bloq = False
                    else:
                        return posibleClave
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
    limite = cantVotantes * 0.75
    for votado in equipoSeleccionado.keys():
        cantidadVotos = equipoSeleccionado[votado]
        if(cantidadVotos > limite):
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

    nameColaborador = session[constants.PROFILE_KEY]['nickname']
    print nameColaborador

    if nameColaborador not in dicColaboradorToPerfilesVistos.keys():
        dicColaboradorToPerfilesVistos[nameColaborador]= []

    if nameColaborador not in dicColaboradorToTuplasSeleccionadas.keys():
        dicColaboradorToTuplasSeleccionadas[nameColaborador]= []

    perfilDeTwitterID = obtenerPerfilAmirar(nameColaborador)

#    perfiles = preparar.obtenerPerfiles(name,dicEsclavoToPerfilesTwitterVistos,perfilesDeTwitter,dicPerfilesDeTwitterToCantidadVistos,cantPerfilesAmostrar) #perfilesDeTwitter[0:2]    #MIRAR ESTOOOOOOOOOOOOO SELECCION DE PERFILES
 #   print perfiles
  #  perfilAenviar = perfiles[0]
   # dicEsclavoToPerfilesAver[name]=perfiles[1:]

    msg, perfilDeTwitterScreenName = armarMensaje(perfilDeTwitterID)

    print msg
    dicColaboradorToprogessBar[nameColaborador] = 0 
    dicColaboradorToUltimoVisto[nameColaborador] = perfilDeTwitterID
#    value = Markup(msg)
    return render_template('jugar.html',env=env, perfiles = msg, nombreDelUsuario = perfilDeTwitterScreenName)


@app.route('/yajugue', methods=['POST'])
def yajugue():
    # global asd
    # global dicEsclavoToPerfilesTwitterVistos
    global dicColaboradorToTuplasSeleccionadas
    global dicColaboradorToprogessBar
    # global dicidTwitterCuentaToVotacion
    # global dicEsclavoToPerfilesAver
    # global dicEsclavoToUltimoVisto


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
        # elif(btn == "Huracan"):
        #     equipoSeleccionado = "Huracan"
        #     print "Huracan"
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
        # elif(btn == "Colon"):
        #     equipoSeleccionado = "Colon"
        #     print "Colon"
        # elif(btn == "Velez"):
        #     equipoSeleccionado = "Velez"
        #     print "Velez"
        # elif(btn == "Lanus"):
        #     equipoSeleccionado = "Lanus"
        #     print "Lanus"
        # elif(btn == "Banfield"):
        #     equipoSeleccionado = "Banfield"
        #     print "Banfield"
        # elif(btn == "Atletico Tucuman"):
        #     equipoSeleccionado = "Atletico Tucuman"
        #     print "Atletico Tucuman"
        # elif(btn == "Temperley"):
        #     equipoSeleccionado = "Temperley"
        #     print "Temperley"
        # elif(btn == "Union"):
        #     equipoSeleccionado = "Union"
        #     print "Union"
        # elif(btn == "Tigre"):
        #     equipoSeleccionado = "Tigre"
        #     print "Tigre"
        else:
            print "boom"
    else:
        print "No"
    nameColaborador = session['username']
    print nameColaborador

    perfilVisto = dicColaboradorToUltimoVisto[nameColaborador]
    print perfilVisto

    dicColaboradorToPerfilesVistos[nameColaborador].append(perfilVisto)
    dicColaboradorToTuplasSeleccionadas[nameColaborador].append([perfilVisto,equipoSeleccionado])

    if (perfilVisto not in dicidTwitterCuentaToVotacion.keys()):
        dicidTwitterCuentaToVotacion[perfilVisto] = []
    #     print "agregado"

    elementito = [nameColaborador,equipoSeleccionado]
    dicidTwitterCuentaToVotacion[perfilVisto].append(elementito)


    global cantidadesHeap
    global dicCantidadTOperfilesTwitter
    global posiblesClaves
    global dicperfilTwitterToCantidades

    if(perfilVisto not in dicperfilTwitterToCantidades.keys()):
        dicperfilTwitterToCantidades[perfilVisto] = 1
        cantidadesHeap.add(1)
        cantidad = 1
    else:
        cantidad = dicperfilTwitterToCantidades[perfilVisto] + 1
        dicperfilTwitterToCantidades[perfilVisto] =  cantidad
        cantidadesHeap.add(cantidad)
        cantidadesHeap.remove(cantidad - 1)
    if (cantidad in dicCantidadTOperfilesTwitter.keys()):
        print "cantidad aparece"
        if(cantidad > 3):
            print "no agarro el else"
            equipoDecidido = hayMayoriaDeEquipo(dicidTwitterCuentaToVotacion[perfilVisto])
            if(equipoDecidido):
                # perfilesDeTwitter = dicCantidadTOperfilesTwitter[cantidad-1]
                # perfilesDeTwitterAagregar = perfilesDeTwitter.remove(perfilVisto)
                dicCantidadTOperfilesTwitter[cantidad-1].remove(perfilVisto)
                posiblesClaves.remove(perfilVisto)
                cantidadesHeap.remove(cantidad)                    
            else:
                # perfilesDeTwitter = dicCantidadTOperfilesTwitter[cantidad]
                # perfilesDeTwitterAagregar = perfilesDeTwitter.append(perfilVisto)
                dicCantidadTOperfilesTwitter[cantidad].append(perfilVisto)

                # perfilesDeTwitter = dicCantidadTOperfilesTwitter[cantidad-1]
                # perfilesDeTwitterAagregar = perfilesDeTwitter.remove(perfilVisto)
                dicCantidadTOperfilesTwitter[cantidad-1].remove(perfilVisto)

        else:
            # print "agarro el else"
            # perfilesDeTwitter = dicCantidadTOperfilesTwitter[cantidad]
            # print perfilVisto
            # print perfilesDeTwitter
            dicCantidadTOperfilesTwitter[cantidad].append(perfilVisto)
            # print dicCantidadTOperfilesTwitter[cantidad]
            if(cantidad != 1):
                # print "entro a distinto"
                # perfilesDeTwitter = dicCantidadTOperfilesTwitter[cantidad-1]
                # perfilesDeTwitterAagregar = perfilesDeTwitter.remove(perfilVisto)
                dicCantidadTOperfilesTwitter[cantidad-1].remove(perfilVisto)

    else:
        # print "aca"
        # print perfilVisto
        dicCantidadTOperfilesTwitter[cantidad] = [perfilVisto]
        # print dicCantidadTOperfilesTwitter[cantidad]
        # print "post aca"


    agregar = registro(colaborador= nameColaborador ,perfilDeTwitter= perfilVisto,choice=equipoSeleccionado)
    agregar.save()

    cantidadPerfilesAnalizados = dicColaboradorToprogessBar[nameColaborador]
    cantidadPerfilesAnalizados = cantidadPerfilesAnalizados + 1

    if(cantidadPerfilesAnalizados == 10):
        dicColaboradorToprogessBar[nameColaborador] = 0
        return render_template('finJuego.html',env=env, user=nameColaborador)
    else:
        perfilDeTwitterID = obtenerPerfilAmirar(nameColaborador)
        msg, perfilDeTwitterScreenName = armarMensaje(perfilDeTwitterID)
        dicColaboradorToUltimoVisto[nameColaborador] = perfilDeTwitterID
        dicColaboradorToprogessBar[nameColaborador] = cantidadPerfilesAnalizados
        return render_template('jugar.html',env=env, perfiles = msg, nombreDelUsuario = perfilDeTwitterScreenName)

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
