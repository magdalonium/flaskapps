# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."


@app.route('/bilde')
def show_bilde():
    return "<img src='static/bilde1.png' alt='magician obscuring the moon'>"


@app.route('/stiligbilde')
def show_stiligbilde():
    return "<img src='static/bilde1.png' alt='magician obscuring the moon' \
        style='width: 60%; margin: auto; display: block;'>"
       

import base64
from io import BytesIO
from matplotlib.figure import Figure

@app.route('/diagram')
def show_diagram():
    #Setter figur og akse
    fig = Figure(figsize=(6, 3), tight_layout=True)
    ax = fig.subplots()
    
    #Tegnekommandoer
    ax.plot([1, 2, 3], [1, 3, 2])

    #Gjør figuren om til en img-tag.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'>"


import numpy as np

def tegn_graf(fun, xmin = -1, xmax = 1):
    
    #Setter figur og akse
    fig = Figure(figsize=(6, 3), tight_layout=True)
    ax = fig.subplots()
    
    #Tegnekommandoer
    X = np.linspace(xmin, xmax)
    ax.plot(X, fun(X))
    ax.axhline(0, color="black")
    ax.grid(True)
    
    #Gjør figuren om til en img-tag.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'>"


def løs_andregradslikning(a, b, c):
    if b**2 - 4*a*c > 0:
        return [(-b - np.sqrt(b**2 - 4*a*c))/(2*a), (-b + np.sqrt(b**2 - 4*a*c))/(2*a)]
    elif b**2 - 4*a*c == 0:
        return -b/2
    else:
        return None


andregradslikning_mal = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Andregradslikningsløser</title>
    <link rel="stylesheet" href="/static/default.css" type="text/css">
    <style>
        .coeff {{width: 40px}}
    </style>
  </head>
  <body>
    <h1>Andregradslikningsløser</h1>
    <p>Løser andregradslikninger på formen ax² + bx + c = 0</p>
    <h2>Inntasting</h2>
    <form method='GET'>
            a = <input class="coeff" type="text" name="a">
            b = <input class="coeff" type="text" name="b">
            c = <input class="coeff" type="text" name="c">
            <input type="submit" value="Beregn">
    </form>
    <h2>Input</h2>
    <p>{inndata}</p>
    <h2>Output</h2>
    <p>{utdata}</p>
  </body>
</html>
"""

from flask import request

@app.route('/andregradslikning')
def show_andregradslikning():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    c = float(request.args.get('c', 0))
    inndata = str({"a":a, "b":b, "c":c})
    løsning = løs_andregradslikning(a, b, c)
    utdata = f"x = {løsning}"
    
    #Tegner funksjonen med nullpunktene. Begynner med å definere funksjonen.
    fun = lambda x: a*x**2 + b*x + c
    
    #Setter grensene slik at eventuelle løsninger kommer med.
    try:
        xmin = min(løsning) - 1
        xmax = max(løsning) + 1
    except Exception:
        xmin, xmax = -1, 1
    
    #Legger grafen til utdataene
    utdata += f"{tegn_graf(fun, xmax, xmin)}"

    return andregradslikning_mal.format(inndata = inndata, utdata = utdata)
