# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions
#
#
# # This is a simple example for a custom action which utters "Hello World!"
#
from random import choice
from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction


class ValidatePurchaseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_purchase_form"

    async def extract_commodity(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return None

    async def extract_entity(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return None

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        print(slots_mapped_in_domain)
        for group in range(10):
            try:
                commodity = next(tracker.get_latest_entity_values(entity_type="commodity", entity_group=str(group)))
            except StopIteration:
                commodity = None
            try:
                quantity = next(tracker.get_latest_entity_values(entity_type="quantity", entity_group=str(group)))
            except StopIteration:
                quantity = None

        print("!!!!!!!!!!!!!!!! called required slots!!!!!!!!!!!!!!!!!!!!!!!!!")
        return slots_mapped_in_domain


class ActionAnythingElse(Action):
    def name(self) -> Text:
        return "action_anything_else"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        price = tracker.get_slot('price')
        all_commodities = tracker.get_slot('all_commodities')
        commodities_missing_quantities = tracker.get_slot('commodities_missing_quantities')
        new_commodities = []
        for group in range(10):
            try:
                commodity = next(tracker.get_latest_entity_values(entity_type="commodity", entity_group=str(group)))
            except StopIteration:
                commodity = None
            try:
                quantity = next(tracker.get_latest_entity_values(entity_type="quantity", entity_group=str(group)))
            except StopIteration:
                quantity = None

            if commodity and quantity:
                new_commodity = {"commodity": commodity, "quantity": quantity, "price": price}
                if commodity in commodities_missing_quantities:
                    commodities_missing_quantities = list(filter(lambda a: a != commodity and a!=commodity+"s", commodities_missing_quantities))
                new_commodities.append(new_commodity)
            elif commodity:
                commodities_missing_quantities.append(commodity)
            elif quantity:
                commodity = commodities_missing_quantities.pop(0)
                new_commodity = {"commodity": commodity, "quantity": quantity, "price": price}
                new_commodities.append(new_commodity)

        all_commodities.extend(new_commodities)

        if commodities_missing_quantities:
            commodity_missing_quantity = commodities_missing_quantities[0]
            templates = domain['responses']['utter_ask_quantity']
            utterance = choice(templates)['text'].format(commodity=commodity_missing_quantity)
            dispatcher.utter_message(text=utterance)
        elif new_commodities:
            dispatcher.utter_message(template="utter_anything_else")
        else:
            dispatcher.utter_message(template="utter_ask_commodity")

        return [SlotSet("all_commodities", all_commodities),
                SlotSet('commodities_missing_quantities',  commodities_missing_quantities)]


class ActionPay(Action):
    def name(self) -> Text:
        return "action_pay"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

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
        print(all_commodities)
        price = 0.0
        for commodity in all_commodities:
            price += float(commodity['price']) * float(commodity['quantity'])
            # print(price)

        templates = domain['responses']['utter_price']
        utterance = choice(templates)['text'].format(price=price, currency=tracker.get_slot('currency'))
        dispatcher.utter_message(text=utterance)

        return []
