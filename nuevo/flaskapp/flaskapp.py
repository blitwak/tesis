from flask import Flask
from flask import Flask, session, redirect, url_for, escape, request,render_template
import json
import preparar as preparar
import pickle
import os.path
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "holamanolacomova"
#app.SQLALCHEMY_DATABASE_URI = 'sqlite:///students.sqlite3'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
global asd
asd = 0


class registro(db.Model):
	id = db.Column('registro_id', db.Integer, primary_key = True)
	colaborador = db.Column(db.String(100))
	perfilDeTwitter = db.Column(db.String(64))
	choice = db.Column(db.String(30))

	def __init__(self, colaborador,perfilDeTwitter,choice):
		self.colaborador = colaborador
		self.perfilDeTwitter = perfilDeTwitter
		self.choice = choice

global cantPerfilesAmostrar
cantPerfilesAmostrar = 3

def levantarPerfilesDeTwitter():
	filename = "/var/www/twitterAmostrarCopaArgentina.p"
#	filename = "static/bd/twitterAmostrarCopaArgentina.p"
	if os.path.isfile(filename):
		filehandler = open(filename,'rb')
		ret = pickle.load(filehandler)
		filehandler.close()
		print "levantada"
		return ret

#	else:
		#print "no entro"
		#ret = {201032752: [u'Club Atl\xe9tico Uni\xf3n', u'clubaunion', u'Twitter oficial del Club Atl\xe9tico Uni\xf3n de Santa Fe.', u'http://pbs.twimg.com/profile_images/641646225041846274/rmJgG9lN_normal.png', u'https://pbs.twimg.com/profile_banners/201032752/1445378175'], 505347396: [u'Club Atl\xe9tico Col\xf3n', u'ColonOficial', u'Bienvenidos a la cuenta oficial en Twitter del Club Atl\xe9tico Col\xf3n', u'http://pbs.twimg.com/profile_images/806325049649229824/6NAHjAtP_normal.jpg', u'https://pbs.twimg.com/profile_banners/505347396/1481673792'], 188356649: [u'C. A. Independiente', u'Independiente', u'Cuenta Oficial del Club Atl\xe9tico Independiente.', u'http://pbs.twimg.com/profile_images/803916220932247552/ugJbk-Fi_normal.jpg', u'https://pbs.twimg.com/profile_banners/188356649/1482029837'], 338400297: [u'Rosario Central', u'CARCoficial', u'Cuenta oficial del Club Atl\xe9tico Rosario Central', u'http://pbs.twimg.com/profile_images/677256336061669376/WqxaSE_X_normal.jpg', u'https://pbs.twimg.com/profile_banners/338400297/1481929521'], 276223178: [u'Club A. Temperley', u'TemperleyOK', u'\u2022 CUENTA OFICIAL DEL CLUB ATL\xc9TICO TEMPERLEY \u2022 Donde los sue\xf1os se cumplen \u2022 \u26051974 \u26051982 \u27301995 \u27301996 \u27301999 \u27302014 \u26052014 \u2022 Contacto: prensa@temperley.org.ar', u'http://pbs.twimg.com/profile_images/611209880591069184/Ly5JlfvD_normal.png', u'https://pbs.twimg.com/profile_banners/276223178/1478713188'], 783689678: [u'Club Atl\xe9tico Lan\xfas', u'clublanus', u'Twitter oficial del Club Atl\xe9tico Lan\xfas. Fundado el 3 de enero de 1915. El Club de barrio m\xe1s grande del Mundo.', u'http://pbs.twimg.com/profile_images/792875030224961537/Rq9Bx24e_normal.jpg', u'https://pbs.twimg.com/profile_banners/783689678/1475782945'], 575667065: [u"Newell's Old Boys", u'CANOBoficial', u"Club Atl\xe9tico Newell's Old Boys", u'http://pbs.twimg.com/profile_images/811620180472266752/a6g1P93J_normal.jpg', u'https://pbs.twimg.com/profile_banners/575667065/1473185077'], 162918448: [u'Atl\xe9tico Tucum\xe1n Of.', u'ATOficial', u'Twitter Oficial del Club Atl\xe9tico Tucum\xe1n. Facebook: https://t.co/pLs844M4FP\nInstagram: Clubatleticotucumanoficial', u'http://pbs.twimg.com/profile_images/803919676711571456/gCQheT6N_normal.jpg', u'https://pbs.twimg.com/profile_banners/162918448/1478312562'], 273667377: [u'Club Atl\xe9tico Tigre', u'catigreoficial', u'Twitter Oficial del Club Atl\xe9tico Tigre. Fundado el 3 de Agosto de 1902. Primera Divisi\xf3n del F\xfatbol Argentino.', u'http://pbs.twimg.com/profile_images/771342186940076032/aU2Jm0p7_normal.jpg', u'https://pbs.twimg.com/profile_banners/273667377/1472060316'], 42933426: [u'Boca Jrs. Oficial', u'BocaJrsOficial', u'Twitter oficial del Club Atl\xe9tico Boca Juniors / https://t.co/IZiKeMQJuw / https://t.co/9jE45F0GSu / https://t.co/uhVPA9vSUU.', u'http://pbs.twimg.com/profile_images/803613906329604096/uBYvVHsD_normal.jpg', u'https://pbs.twimg.com/profile_banners/42933426/1481916263'], 240008403: [u'San Lorenzo', u'SanLorenzo', u'Twitter Oficial del Club Atl\xe9tico San Lorenzo de Almagro. Informaci\xf3n actualizada, coberturas en vivo y todo acerca de la vida de San Lorenzo.', u'http://pbs.twimg.com/profile_images/805759246256242691/cFiazeMD_normal.jpg', u'https://pbs.twimg.com/profile_banners/240008403/1458772608'], 118056286: [u'GIMNASIA', u'gimnasiaoficial', u'Club de Gimnasia y Esgrima La Plata. Fundado el 3 de junio de 1887. Decano del f\xfatbol de Am\xe9rica. Campe\xf3n Argentino 1929 y Copa Centenario AFA 1993/1994.', u'http://pbs.twimg.com/profile_images/583323196243517440/sQGOuGHb_normal.jpg', u'https://pbs.twimg.com/profile_banners/118056286/1482795385'], 276204298: [u'V\xe9lez Sarsfield', u'Velez', u'Twitter Oficial del Club Atl\xe9tico V\xe9lez Sarsfield.\r\nEl primero en ser un gran club.', u'http://pbs.twimg.com/profile_images/770698276781826048/JSk38W7i_normal.jpg', u'https://pbs.twimg.com/profile_banners/276204298/1482343833'], 1112088823: [u'Belgrano', u'Belgrano', u'Twitter Oficial del Club Atl\xe9tico Belgrano.\r\nAsociaci\xf3n Civil fundada el 19 de marzo de 1905.\r\nAlberdi, C\xf3rdoba, Argentina.', u'http://pbs.twimg.com/profile_images/813387900293414912/1glAgGmm_normal.jpg', u'https://pbs.twimg.com/profile_banners/1112088823/1481728541'], 284128412: [u'Estudiantes de L.P.', u'EdelpOficial', u'Cuenta Oficial del Club Estudiantes de La Plata. #EDLP', u'http://pbs.twimg.com/profile_images/768526728385925122/HRwpUSHN_normal.jpg', u'https://pbs.twimg.com/profile_banners/284128412/1482190103'], 196845049: [u'Talleres', u'CATalleresdecba', u'Twitter Oficial del Club Atl\xe9tico Talleres de C\xf3rdoba.', u'http://pbs.twimg.com/profile_images/806860257037271040/deLsM-m0_normal.jpg', u'https://pbs.twimg.com/profile_banners/196845049/1479307122'], 274140988: [u'CA Hurac\xe1n', u'CAHuracan', u'Twitter Oficial del Club Atl\xe9tico Hurac\xe1n', u'http://pbs.twimg.com/profile_images/813114473875730432/3IpyIRRK_normal.jpg', u'https://pbs.twimg.com/profile_banners/274140988/1408402045'], 95227165: [u'Racing Club', u'RacingClub', u'Twitter oficial de Racing Club, el primer grande. Avellaneda, Argentina.', u'http://pbs.twimg.com/profile_images/806590307794096129/XtRJq-q8_normal.jpg', u'https://pbs.twimg.com/profile_banners/95227165/1479258323'], 706027358: [u'Club A. Banfield', u'CAB_oficial', u'Cuenta Oficial de Twitter del Club Atl\xe9tico Banfield. Fundado el 21 de enero de 1896.', u'http://pbs.twimg.com/profile_images/804098374593105926/ZoDoLgws_normal.jpg', u'https://pbs.twimg.com/profile_banners/706027358/1474908338'], 161734463: [u'River Plate', u'CARPoficial', u'Cuenta oficial del Club Atl\xe9tico River Plate.', u'http://pbs.twimg.com/profile_images/803808585994108928/B3TzNLVW_normal.jpg', u'https://pbs.twimg.com/profile_banners/161734463/1480526867']}
		#return ret


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

	print "YA JUGUE"
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
	elemento = registro(name,idTwitterCuenta,seleccionEquipo)
	db.session.add(elemento)
	db.session.commit()
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
  db.create_all()
  app.run()
