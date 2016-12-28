# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, session, redirect, url_for, escape, request,render_template
import json
import preparar as preparar
import pickle
import os.path
from flask_sqlalchemy import SQLAlchemy
# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "holamanolacomova"
#app.SQLALCHEMY_DATABASE_URI = 'sqlite:///students.sqlite3'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)





class registro(db.Model):
	id = db.Column('registro_id', db.Integer, primary_key = True)
	colaborador = db.Column(db.String(100))
	perfilDeTwitter = db.Column(db.String(64))
	choice = db.Column(db.String(30))

	def __init__(self, colaborador,perfilDeTwitter,choice):
		self.colaborador = colaborador
		self.perfilDeTwitter = perfilDeTwitter
		self.choice = choice

cantPerfilesAmostrar = 3

def levantarPerfilesDeTwitter():
	filename = "static/bd/twitterAmostrar.p"
	if os.path.isfile(filename):
		filehandler = open(filename,'rb')
		ret = pickle.load(filehandler)
		filehandler.close()
	return ret

perfilesDeTwitter = levantarPerfilesDeTwitter ()

clavesJson = ["Primero","Segundo","Tercero","Cuarto","Quinto","Sexto"]

dicPerfilesDeTwitterToCantidadVistos = {}


dicEsclavoToPerfilesTwitterVistos = {} #user->idTwitterCuenta

dicEsclavoToPerfilesAver = {}

dicUserToTuplasSeleccionadas = {} # user -> idTwitterCuenta,choice
dicidTwitterCuentaToVotacion = {} #idTwitterCuenta ->user,choice


@app.route('/countme/<input_str>')
def count_me(input_str):
    return input_str

# Define a route for the default URL, which loads the form
@app.route('/')
@app.route('/login', methods=['POST','GET'])
def login():
    return render_template('login.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
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
	name=request.form['usuario']
	perfiles = preparar.obtenerPerfiles(name,dicEsclavoToPerfilesTwitterVistos,perfilesDeTwitter,dicPerfilesDeTwitterToCantidadVistos,cantPerfilesAmostrar) #perfilesDeTwitter[0:2]    #MIRAR ESTOOOOOOOOOOOOO SELECCION DE PERFILES
	perfilAenviar = perfiles[0]
	dicEsclavoToPerfilesAver[name]=perfiles[1:]
	msg = preparar.armarMensaje(perfilAenviar,perfilesDeTwitter)
	if name not in dicEsclavoToPerfilesTwitterVistos.keys():
		dicEsclavoToPerfilesTwitterVistos[name]= []
	if name not in dicUserToTuplasSeleccionadas.keys():
		dicUserToTuplasSeleccionadas[name]= []
	return render_template('jugar.html', name=name, perfiles = msg)


@app.route('/mostrarTodoRegistro')
def mostrarTodoRegistro():
   return render_template('mostrarTodoRegistro.html', registros = registro.query.all() )


@app.route('/yajugue', methods=['POST'])
def yajugue():
	name=request.form['usuario']
	seleccionEquipo=request.form['teams']
	idTwitterCuenta = request.form['id_datosTwitter']
	asd = dicEsclavoToPerfilesTwitterVistos[name]
	asd.append(idTwitterCuenta)
	dicEsclavoToPerfilesTwitterVistos[name] = asd
	fff = dicUserToTuplasSeleccionadas[name]
	fff.append([idTwitterCuenta,seleccionEquipo])
	dicUserToTuplasSeleccionadas[name] = fff

	if (idTwitterCuenta not in dicidTwitterCuentaToVotacion.keys()):
		dicidTwitterCuentaToVotacion[idTwitterCuenta] = []
	print idTwitterCuenta
	dicidTwitterCuentaToVotacion[idTwitterCuenta] = dicidTwitterCuentaToVotacion[idTwitterCuenta].append([name,seleccionEquipo])

	elemento = registro(name,idTwitterCuenta,seleccionEquipo)
	db.session.add(elemento)
	db.session.commit()

	perfiles = dicEsclavoToPerfilesAver[name]    
	if(len(perfiles) > 0):
		perfilAenviar = perfiles[0]
		dicEsclavoToPerfilesAver[name]=perfiles[1:]
		msg = preparar.armarMensaje(perfilAenviar,perfilesDeTwitter)
		return render_template('jugar.html', name=name, perfiles = msg)
	else:
		return render_template('finJuego.html', user=name, votacion = fff)

if __name__ == '__main__':
	db.create_all()
	app.run()
