# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from random import choice

class ActionAnythingElse(Action):

    def name(self) -> Text:
        return "action_anything_else"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(domain)

        commodity = tracker.get_slot('commodity')

        price = tracker.get_slot('price')
        quantity = tracker.get_slot('quantity')
        new_commodity = {"commodity": commodity, "quantity": quantity, "price": price}

        all_commodities = tracker.get_slot('all_commodities')
        all_commodities.append(new_commodity)

        dispatcher.utter_message(template = "utter_anything_else")

        # price_init = domain["slots"]["price"]["initial_value"]
        commodity_init = domain["slots"]["commodity"]["initial_value"]
        quantity_init = domain["slots"]["quantity"]["initial_value"]

        # print(price_init)
        print(commodity_init)
        print(quantity_init)

        return [SlotSet("all_commodities", all_commodities),
                SlotSet('commodity', commodity_init), SlotSet('quantity', quantity_init)] #TODO: SlotSet('price', price_init)


class ActionPay(Action):
    def name(self) -> Text:
        return "action_pay"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        print(domain)

        dispatcher.utter_message(template="utter_thanks")

        return []


class ActionPrice(Action):
    def name(self) -> Text:
        return "action_utter_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        print(domain)

        all_commodities = tracker.get_slot('all_commodities')
        price = 0.0
        for commodity in all_commodities:
            price += float(commodity['price']) * float(commodity['quantity'])
            print(price)

        templates = domain['responses']['utter_price']
        utterance = choice(templates)['text'].format(price=price, currency=tracker.get_slot('currency'))
        dispatcher.utter_message(text=utterance)

        return []
