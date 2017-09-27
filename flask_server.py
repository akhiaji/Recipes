from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from Recipe import *
import random


app = Flask(__name__)
rb = None
@app.route("/", methods=['POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    text = request.form["Body"]
    title_filter = Filter("title", lambda x, y: y.upper() in x.upper(), text)
    rb.filters.append(title_filter)
    recipes = rb.filter()
    if len(recipes) > 0:
        print len(recipes)
        recipe = random.choice(recipes)
        ingredients = "\n".join(recipe.ingredients)
        instructions = "\n".join(recipe.instructions)
        message = "{}: \n {} \n INSTRUCTIONS: \n \n {}".format(recipe.title.upper(), ingredients, instructions)
    else:
        message = "No such recipes"
    rb.filters.remove(title_filter)
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)

@app.before_first_request
def initialize_recipes():
    decoder = json.JSONDecoder()
    json_data = decoder.decode(open("/home/akhilesh/Desktop/tutorial/items_quotes_22.json").read())
    recipes = []
    for i in json_data:
        recipes.append(Recipe(i))
    global rb
    rb = RecipeBook(recipes)
    avg_rev_filter = Filter("avg_review", lambda x, y: x > y, 4)
    num_rev_filter = Filter("num_reviews", lambda x, y: x > y, 80)
    time_filter = Filter("time", lambda x, y: x < y, 60)
    rb.filters.append(avg_rev_filter)
    rb.filters.append(num_rev_filter)
    rb.filters.append(time_filter)
    print len(rb.recipes)

if __name__ == "__main__":
    app.run(host="0.0.0.0:PORT80")

