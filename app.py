import sys
from random import shuffle

from flask import Flask, render_template

import data

app = Flask(__name__)


def correct_word(counter):
    if counter % 10 == 1 and counter % 100 != 11:
        return str(counter) + " тур"
    elif counter % 10 == 2 and counter % 100 != 12 or counter % 10 == 3 and counter % 100 != 13 or counter % 10 == 4 \
            and counter % 100 != 14:
        return str(counter) + " тура"
    else:
        return str(counter) + " туров"


def random_tour(tours):
    lst = list(range(1, len(tours.keys())))
    shuffle(lst)
    return lst


def count_tours(tours, city):
    counter = 0
    for i in range(1, len(tours.keys())):
        if tours[i]["departure"] == city:
            counter += 1
    return counter


def min_and_max_nights(tours, city):
    maximum = float("-inf")
    minimal = float("inf")
    for i in range(1, len(tours.keys())):
        if tours[i]["departure"] == city and tours[i]["nights"] > maximum:
            maximum = tours[i]["nights"]
        if tours[i]["departure"] == city and tours[i]["nights"] < minimal:
            minimal = tours[i]["nights"]
    return minimal, maximum


def min_and_max_price(tours, city):
    maximum = float("-inf")
    minimal = float("inf")
    for i in range(1, len(tours.keys())):
        if tours[i]["departure"] == city and tours[i]["price"] > maximum:
            maximum = tours[i]["price"]
        if tours[i]["departure"] == city and tours[i]["price"] < minimal:
            minimal = tours[i]["price"]
    return minimal, maximum


@app.route('/')
def render_main():
    random = random_tour(tours=data.tours)
    return render_template(
        "index.html", title=data.title, subtitle=data.subtitle, description=data.description,
        departures=data.departures, tours=data.tours, random=random)


@app.route("/departure/<city>/")
def render_departure(city):
    price = min_and_max_price(tours=data.tours, city=city)
    nights = min_and_max_nights(tours=data.tours, city=city)
    word = correct_word(count_tours(tours=data.tours, city=city))
    length = len(data.tours)
    if city in data.departures:
        return render_template(
            "departure.html", departures=data.departures, tours=data.tours,
            city=city, method=price, nights=nights, len=length, word=word)


@app.route("/tours/<hotel>/")
def render_tour(hotel):
    for key in data.tours:
        if hotel == data.tours[key]["title"].split(" ")[0]:
            return render_template("tour.html", departures=data.departures, tours=data.tours[key])


@app.errorhandler(404)
def render_not_found(error):
    return render_template("error.html", error=error), 404


@app.errorhandler(500)
def render_server_error(error):
    return render_template("error.html", error=error), 500


if __name__ == '__main__':
    app.run()
