import base64
import itertools
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, render_template, request
import pandas as pd
import random
import re
import GeneticAlgorithm

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/lab1", methods=["GET", "POST"])
def lab1():
    if request.method == "POST":
        ideal = [int(x) for x in str(request.form.get("ideal")).replace(" ", "").split(",")]
        str_products = str(request.form.get("products")).replace(" ", "")
        products = [parse_products(string) for string in str_products.split("},{")]
        result = GeneticAlgorithm.genetic_algorithm(products, ideal)
        if not(result is None):
            print("Лучшее решение:", result.genes, " ", result.fitness)
        product_names = [products[i].name for i in range(len(result.genes)) if result.genes[i] == 1]
        result_string = ", ".join(product_names)
        return render_template("lab1.html", result=result_string)

    return render_template("lab1.html")


def parse_products(products):
    pattern = r'\"(.*?)\",\s*\[(.*?)\],\s*\"Цена:(\d+)\"'
    matches = re.findall(pattern, products)
    if matches:
        name, characteristics_str, price = matches[0]
        # Преобразуем строку с характеристиками в список чисел
        characteristics = [int(x) for x in re.sub(r'[\[\]]', '', characteristics_str).split(',')]
        return GeneticAlgorithm.Product(name, characteristics, int(price))
    else:
        return None


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))