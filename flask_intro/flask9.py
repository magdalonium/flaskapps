# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."


personer = ['Amund', 'Benjamin', 'Cecilie']

from flask import render_template

@app.route('/personer')
def show_personer():
    return render_template("personer.html", personer=personer)


isfavoritter = {'Amund' : 'Krone-is',
              'Benjamin' : 'Pin-up',
              'Cecilie' : 'Lolipop'}

@app.route('/isfavoritter')
def show_isfavoritter():
    return render_template("isfavoritter.html", isfavoritter=isfavoritter)


@app.route('/listetest')
def show_listetest():
    return render_template("listetest.html", isfavoritter=isfavoritter)


@app.route('/cycletest')
def show_cycletest():
    return render_template("cycletest.html", isfavoritter=isfavoritter)


elementer = [(None, "Dette er et eksempel"),
             ("programkode","print('Hei verden!')"),
             ("sitat", "I'm not here to be perfect, I'm here to be real"),
             ("liste", ['Amund', 'Benjamin', 'Cecilie'])]

from numpy.random import random

@app.route('/logisktest')
def show_logisktest():
    vinner = random() < 0.2
    return render_template("logisktest.html", vinner=vinner, elementer=elementer)


import base64
import numpy as np
from io import BytesIO
from matplotlib.figure import Figure

def løs_andregradslikning(a, b, c):
    if b**2 - 4*a*c > 0:
        return [(-b - np.sqrt(b**2 - 4*a*c))/(2*a), (-b + np.sqrt(b**2 - 4*a*c))/(2*a)]
    elif b**2 - 4*a*c == 0:
        return [-b/2]
    else:
        return None

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
    return f"data:image/png;base64,{data}"


from flask import request

@app.route('/andregradslikning')
def show_andregradslikning():
    if len(request.args) > 0:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        c = float(request.args.get('c', 0))
        inndata = {"a":a, "b":b, "c":c}

        løsninger = løs_andregradslikning(a, b, c)
    
        #Tegner funksjonen med nullpunktene. Begynner med å definere funksjonen.
        fun = lambda x: a*x**2 + b*x + c
    
        #Setter grensene slik at eventuelle løsninger kommer med.
        try:
            xmin = min(løsninger) - 1
            xmax = max(løsninger) + 1
        except Exception:
            xmin, xmax = -1, 1
    
        #Legger grafen til utdataene
        bildedata = tegn_graf(fun, xmax, xmin)
        
    else:
        inndata = None
        løsninger = None
        bildedata = None

    return render_template("andregradslikning.html", inndata = inndata, løsninger = løsninger, bilde=bildedata)

