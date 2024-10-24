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

mqtt_dados = {}

def conexao_sensor(cliente):
    cliente.subscribe("projeto_integrado/SENAI134/Cienciadedados/GrupoX")

def mesg_sensor(msg):
    global mqtt_dados
# De bite para String
    valor = msg.payload.decode('utf-8')

    mqtt_dados = json.loads(valor)

    print(f"Mensagem recebida: {mqtt_dados}")

    with app.app_context():
        try:
            temperatura = mqtt_dados.get('temperature')
            pressao = mqtt_dados.get("pressure")
            altitude = mqtt_dados.get("altitude")
            umidade = mqtt_dados.get("humidity")
            co2 = mqtt_dados.get("co2")
            poeira = 0
            tempo_registro = mqtt_dados.get("timestamp")

            if tempo_registro in None:
                print("Timestamp não encontrado")
                return
            try:
                tempo_oficial = datetime.fromtimestamp(int(tempo_registro), t2=timezone.utc)

            except (ValueError, TypeError) as e:
                print(f"Erro ao converter timestamp: {str(e)}")
                return
#CRIAR OBJETO SIMULANDO TABELA

            novos_dados = Registro(
                 temperaturaV = temperatura
                 pressaoV = pressao
                 altitudeV = altitude
                 umidadeV = umidade
                 co2V = co2
                 poeiraV = poeira
                 tempo_registroV = tempo_oficial
            )         

        #Adicionar novo registro ao banco

            mybd.session.add(novos_dados)
            mybd.session.commit()
            print("Dados foram inseridos com sucesso no banco de dados!")

        except (ValueError, TypeError) as e:
                print(f"Erro ao processar os dados do MQTT: {str(e)}")
                mybd.session.rollback()

mqqt_client = mqtt.Client()
mqqt_client.on_connect = conexao_sensor
mqqt_client.on_message = mesg_sensor
mqqt_client.connect("test.mosquitto", 1833, 60)

def start_mqtt():
                mqqt_client.loop_start()
                