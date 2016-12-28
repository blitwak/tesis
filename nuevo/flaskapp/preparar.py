import json
def obtenerPerfiles(identidad,dicEsclavoToPerfilesTwitterVistos,perfilesDeTwitter,dicPerfilesDeTwitterToCantidadVistos,cantPerfilesAmostrar):
	cantidadVistas = []
	posiblesPerfiles = []
	if (identidad in dicEsclavoToPerfilesTwitterVistos.keys()):
		perfilesVistos = dicEsclavoToPerfilesTwitterVistos[identidad]
	else:
		perfilesVistos = []

	for idTwitterCuenta in perfilesDeTwitter.keys():
		if(idTwitterCuenta not in perfilesVistos):
			posiblesPerfiles.append(idTwitterCuenta)
			if (idTwitterCuenta in dicPerfilesDeTwitterToCantidadVistos.keys()):
				cantidadVistas.append(dicPerfilesDeTwitterToCantidadVistos[idTwitterCuenta])
			else:
				cantidadVistas.append(0)			
#		print perfilesDeTwitter[idTwitterCuenta][0]
	if len(posiblesPerfiles) <= cantPerfilesAmostrar:
		return posiblesPerfiles
	else:
		aDevolver = []
		maxVistas = max(cantidadVistas) + 1
		clavesVistas = dicPerfilesDeTwitterToCantidadVistos.keys()
		for i in range(cantPerfilesAmostrar):
			minValor = min(cantidadVistas)
			indiceMin = cantidadVistas.index(minValor)
			idTwitterCuenta = posiblesPerfiles[indiceMin]
			aDevolver.append(idTwitterCuenta)
			cantidadVistas[indiceMin] = maxVistas
			if(idTwitterCuenta in clavesVistas):
				dicPerfilesDeTwitterToCantidadVistos[idTwitterCuenta] = dicPerfilesDeTwitterToCantidadVistos[idTwitterCuenta] + 1
			else:
				dicPerfilesDeTwitterToCantidadVistos[idTwitterCuenta] =  1
			clavesVistas.append(idTwitterCuenta)
		return aDevolver
def armarMensaje(clave,perfilesDeTwitter):
	perfil = perfilesDeTwitter[clave]
	dic = {}
	dic["id"]= clave
	dic["name"]= perfil[0]
	dic["screenName"]= perfil[1]
	dic["desc"]= perfil[2]
	dic["banner"]= perfil[3]
	dic["image"]= perfil[4]
	return json.dumps(dic)