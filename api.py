from flask import Flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin

import io
import json
import pytds
import os
import traceback

from rasa_nlu.model import Metadata, Interpreter
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
from rasa_nlu import config as cnf


import logging

from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter

import bot_engine.actions

from db import db_conn

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World"

def getStatefulResponse(intent, stage):
    response = ""
    try:
        with db_conn() as conn:
            sql = "Select IntentID From luIntent where Intent like '%{0}%'".format(intent)
            cursor = conn.cursor()
            cursor.execute(sql)
            response = cursor.fetchone()[0]

        with db_conn() as conn:
            sql = "Select IntentID From luIntent where Intent like '%{0}%'".format(intent)
            cursor = conn.cursor()
            cursor.execute(sql)
            response = cursor.fetchone()[0]
    except:
        print("some error showed up")
        response = "default response"
    return response

def getResponse(intent):
    with db_conn() as conn:
        try:
            sql = "Select Response From datResponse where Intent like '%{0}%'".format(intent)
            cursor = conn.cursor()
            cursor.execute(sql)
            response = cursor.fetchone()[0]
            
        except:
            response = "sorry, could not find that intent"
    return response

@app.route('/chat', methods=['POST'])
@cross_origin(supports_credentials=True)
def chat():
    if request.method == 'POST':
        response = ""

        # try:
            # interpreter = Interpreter.load('./bot_engine/models/nlu/default/nlu')
        interpreter = RasaNLUInterpreter('./bot_engine/models/nlu/default/nluModel')
        agent = Agent.load('./bot_engine/models/dialogue', interpreter = interpreter)

        resp = agent.handle_message("hi")
        print(resp)
        #     print(request.form)
        #     user_query = request.form['query']

        #     resp = agent.handle_message(user_query)
        #     data = interpreter.parse(user_query)
        #     print(data)

        #     confidence = data['intent']['confidence'] 

        #     if confidence < 0.70:
        #         response = "Sorry, I did not get that. Could you repeat that?"

        #     current = data['intent']['name']
        #     # response = getResponse(current)
        #     response = resp
        #     data = {
        #         "request": current,
        #         "response": response
        #     }
        # except:
        #     traceback.print_exc()
        #     current = ""
        #     data = "something didn't work at the api end"

        data = {
            "request": "stuf",
            "response": resp
        }
        return jsonify(data)

