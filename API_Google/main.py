from datetime import datetime, timezone
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import paho.mqtt.client as mqtt

# CONEXÃO COM O BANCO DE DADOS

app = Flask("registro")

# A conexão com banco haverá modificações na base de dados

app.config["AQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:senai%40134@127.0.0.1/bd_medidor"

mybd = SQLAlchemy(app)

# CONEXÃO DOS SENSORES

