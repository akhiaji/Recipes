import json
from twilio.rest import Client
from random import randint

from pprint import pprint
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist

ACCOUNT_SID = "AC0f0b3d8f29025a1ae379e8b248d9fa9a"
AUTH_TOKEN = "8ee51c3f08b08e236a23f0dee25edd06"


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


def main():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    decoder = json.JSONDecoder()
    json_data = decoder.decode(open("/home/akhilesh/Desktop/tutorial/items_quotes_22.json").read())
    recipes = []
    tags = {}
    print len(json_data)
    for i in json_data:
        recipes.append(Recipe(i))
        for j in i["tags"][2:]:
            if j in tags:
                tags[j] += 1
            else:
                tags[j] = 1
    sorted_tags = sorted(tags.iteritems(), key=lambda x: x[1], reverse=True)
    for i in sorted_tags:
        print i
    rb = RecipeBook(recipes)
    avg_rev_filter = Filter("avg_review", lambda x, y: x > y, 4)
    num_rev_filter = Filter("num_reviews", lambda x, y: x > y, 80)
    time_filter = Filter("time", lambda x, y: x < y, 60)
    tag_filter = Filter("tags", lambda a, t: t in a, "World Cuisine")
    rb.filters.append(avg_rev_filter)
    rb.filters.append(num_rev_filter)
    rb.filters.append(time_filter)
    rb.filter()
    for i in rb.recipes:
        print i.title
    print len(rb.recipes)
    selected_recipes = list(rb.select_recipe(3))
    ingredients = combine_ingredients(selected_recipes)
    client.api.account.messages.create(to="4085076998", from_="+15103301778", body=ingredients)
    # recipe1 = selected_recipes[0]
    # client.api.account.messages.create(to="4085076998", from_="+14086178028", body=recipe1.title)
    # client.api.account.messages.create(to="4085076998", from_="+14086178028", body="\n".join(recipe1.ingredients))
    # client.api.account.messages.create(to="4085076998", from_="+14086178028", body="\n".join(recipe1.instructions))
    all_ing = ""
    for i in recipes:
        all_ing += " ".join(i.ingredients)
    dist1 = FreqDist(all_ing)
    print dist1.most_common(50)



if __name__ == '__main__':
    main()



