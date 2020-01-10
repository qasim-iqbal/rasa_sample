from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.channels import HttpInputChannel
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.channels.channel import UserMessage
from rasa_core.channels.direct import CollectingOutputChannel
from rasa_core.channels.rest import HttpInputComponent
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin

logger = logging.getLogger(__name__)
class SimpleWebBot(HttpInputComponent):
    """A simple web bot that listens on a url and responds."""

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/status", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @cross_origin(supports_credentials=True)
        @custom_webhook.route("/", methods=['POST'])
        def receive():

            sender_id = request.form['sender']
            text = request.form['message']
            out = CollectingOutputChannel()
            on_new_message(UserMessage(text, out, sender_id))
            responses = [m for _, m in out.messages]

            data = {
                "response": responses
            }
            return jsonify(data)
    
        return custom_webhook

def run(serve_forever=True):
    #path to your NLU model
    interpreter = RasaNLUInterpreter("./models/nlu/default/delianlu")
    # path to your dialogues models
    agent = Agent.load("./models/dialogue", interpreter=interpreter)
    #http api endpoint for responses
    input_channel = SimpleWebBot()
    
    if serve_forever:
        agent.handle_channel(HttpInputChannel(5004, "/chat", input_channel))
    return agent

    # print("api is up *****")

if __name__ == '__main__':
	# train_dialogue()
	run()