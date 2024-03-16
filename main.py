import itertools
import json
import tkinter as tk
import numpy as np
from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
import GeneticAlgorithm
import FuzzyLogic
from LinguisticVariablesAndScales import LinguisticScale

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
        if not (result is None):
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


@app.route('/lab2', methods=["GET", "POST"])
def lab2():
    if request.method == "POST":
        mf1_params = [int(x) for x in str(request.form.get('mf1_params')).replace(" ", "").split(",")]
        mf2_params = [int(x) for x in str(request.form.get('mf2_params')).replace(" ", "").split(",")]
        crisp_values = [int(x) for x in str(request.form.get('crisp_values')).replace(" ", "").split(",")]

        result = FuzzyLogic.union(mf1_params, mf2_params, crisp_values)
        img = FuzzyLogic.draw_fuzzy_set(mf1_params, mf2_params, crisp_values, result)
        return render_template("lab2.html",
                               result=result,
                               img=img,
                               mf1=mf1_params,
                               mf2=mf2_params,
                               crisp=crisp_values)
    return render_template("lab2.html")


@app.route("/lab3", methods=["GET", "POST"])
def lab3():
    if request.method == "POST":
        data = request.form.to_dict()
        headers = []
        values = []
        user_values = []
        for key in data:
            if len(json.loads(data[key])) == 0:
                break
            if key == "user_values":
                user_values = [int(x) for x in str(json.loads(data[key]).replace(" ", "")).split(",")]
                print(user_values)
                continue
            try:
                obj = json.loads(data[key])
                header = obj['header']
                val = [int(i) for i in obj['values']]
                headers.append(header)
                values.append(val)
            except json.JSONDecodeError:
                pass
        if len(headers) > 0:
            linguistic = LinguisticScale(len(headers), headers, values, user_values)
        else:
            linguistic = LinguisticScale()
        img = linguistic.plot_membership_functions()
        return jsonify(img=img, list=linguistic.result_func_list)
    return render_template("lab3.html")


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
