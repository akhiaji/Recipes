import json
from twilio.rest import Client
from random import randint

from pprint import pprint
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist


class Recipe(object):

    def __init__(self, data):
        self.ingredients = data["ingredients"]
        self.instructions = data["instructions"]
        self.time = data["time"]
        self.num_reviews = data["num_reviews"]
        self.avg_review = data["avg_reviews"]
        self.tags = data["tags"][2:]
        self.title = data["title"]


class RecipeBook(object):

    def __init__(self, recipes=()):
        self.recipes = list(recipes)
        self.filters = []

    def filter(self):
        new_recipes = set()
        for i in self.recipes:
            num_filters = 0
            for j in self.filters:
                attr = getattr(i, j.attr)
                if j.comparator(attr, j.threshold):
                    num_filters += 1
            if num_filters == len(self.filters):
                new_recipes.add(i)

        return list(new_recipes)

    def select_recipe(self, num=None):
        if num is None:
            num = 1
        recipes = set()
        while len(recipes) < num:
            recipes.add(self.recipes[randint(0, len(self.recipes))])
        return recipes




class Filter(object):

    def __init__(self, attr, comparator, threshold=None):
        self.attr = attr
        self.comparator = comparator
        self.threshold = threshold



def combine_ingredients(recipes):
    string = "Ingredients\n-------------------\n"
    for i in list(recipes):
        string += "\n".join(i.ingredients)
    return string
