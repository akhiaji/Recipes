import json
from pprint import pprint
from nltk.stem.porter import PorterStemmer

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
        self.filtered = False

    def filter(self):
        self.filtered = True
        new_recipes = []
        for i in self.recipes:
            for j in self.filters:
                attr = getattr(i, j.attr)
                if j.comparator(attr, j.threshold):
                    new_recipes.append(i)
        self.recipes = new_recipes


class Filter(object):

    def __init__(self, attr, comparator, threshold=None):
        self.attr = attr
        self.comparator = comparator
        self.threshold = threshold




def main():
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


if __name__ == '__main__':
    main()



