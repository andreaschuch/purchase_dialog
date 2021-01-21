
from random import choice, randint
from copy import copy

max_number_combinations = 3
max_quantity = 20

commodities = ["apples", "pears", "cucumbers", "carrots"]

template_intros= ["", "I would like", "Give me", "Can I have", "Could you give me", "I would like to have"]

template_appendices = ["please", ""]

template_and = "and"

space = " "

texts = []


def to_token(token):
    return "["+str(token)+"]"


def to_quantity(group_number):
    return "{\"entity\": \"quantity\", \"group\": \"" +str(group_number)+"\"}"


def to_commodity(group_number):
    return "{\"entity\": \"commodity\", \"group\": \"" +str(group_number)+"\"}"


for number_of_combinations in range(1, max_number_combinations+1):
    for template_intro in template_intros:
        text = template_intro + space
        my_commodities = copy(commodities)
        for group in range(1, number_of_combinations+1):
            commodity = choice(my_commodities)
            my_commodities.remove(commodity)
            quantity = randint(1, max_quantity)
            if 1 < group == number_of_combinations:
                text = text + template_and + space
            text = text + to_token(quantity) + to_quantity(group) + space + to_token(commodity) + to_commodity(group) + space
        texts.append(text.strip())


for text in texts:
    print(text)


