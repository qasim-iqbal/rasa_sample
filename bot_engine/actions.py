from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

class ActionLoanRequest(Action):
    def name(self):
        return 'action_loan_request'

    def run(self, dispatcher, tracker, domain):

        loan_amount = tracker.get_slot('amount')
        loan_amount = float(loan_amount)
        print(amount)
        max_amount = 50000.0
        min_amount = 25000.0

        if amount > max_amount:
            response = """Sorry, The amount is too high"""
        elif amount < min_amount:
            response = """Sorry, The amount is too little"""
        else:
            response = "Yes, the amount is good"

        dispatcher.utter_message(response)
        return [SlotSet('amount',amount)]