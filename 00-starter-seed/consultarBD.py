#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_mongoalchemy import MongoAlchemy
from flask import Flask
import constants

app = Flask(__name__)

app.config['MONGOALCHEMY_DATABASE'] = constants.MONGOALCHEMY_DATABASE
db = MongoAlchemy(app)

class registro(db.Document):
    colaborador = db.StringField()
    perfilDeTwitterID = db.IntField()
    choice = db.StringField()
    perfilDeTwitterScreenName = db.StringField()

#db.registro.find().count()
#use test
#mongo --shell
#db.bios.remove( { } )
#https://pythonhosted.org/Flask-MongoAlchemy/

def main():
	registros = registro.query.all()
	print len(registros)
	for unregistro in registros:
		print unregistro.colaborador,unregistro.choice,unregistro.perfilDeTwitterScreenName
	return

if __name__ == "__main__":
	main()