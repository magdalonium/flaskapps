# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."


skjema = """
<form method='GET'>
    <input type="text" name="tekst">
    <input type="submit" value="Send inn">
</form>
"""

@app.route('/skjema')
def show_skjema():
    return skjema


from flask import request

@app.route('/svar')
def show_svar():
    tekst = request.args.get('tekst', '')
    output = f"<p>Du skrev inn: {tekst}</p>"
    output += skjema
    return output
    

from markupsafe import escape

@app.route('/sikkertsvar')
def show_sikkertsvar():
    tekst = escape(request.args.get('tekst', ''))
    output = f"<p>Du skrev inn: {tekst}</p>"
    output += skjema
    return output


inputkvadrat_mal = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Kvadrer!</title>
    <link rel="stylesheet" href="/static/default.css" type="text/css">
  </head>
  <body>
    <h1>Inputkvadrat</h1>
    <h2>Inntasting</h2>
    <form method='GET'>
      <input type="number" name="tall">
      <input type="submit" value="Beregn">
    </form>
    <h2>Input</h2>
    <p>{inndata}</p>
    <h2>Output</h2>
    <p>{utdata}</p>
  </body>
<html>
"""

@app.route('/inputkvadrat')
def show_inputkvadrat():
    tall = int(request.args.get('tall', 0))
    return inputkvadrat_mal.format(inndata = tall, utdata = tall**2)


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
    <form method="GET">
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
<html>
"""

import numpy as np

def løs_andregradslikning(a, b, c):
    if b**2 - 4*a*c > 0:
        return [(-b - np.sqrt(b**2 - 4*a*c))/(2*a), (-b + np.sqrt(b**2 - 4*a*c))/(2*a)]
    elif b**2 - 4*a*c == 0:
        return -b/2
    else:
        return None


@app.route('/andregradslikning')
def show_andregradslikning():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    c = float(request.args.get('c', 0))  
    inndata = {"a":a, "b":b, "c":c}
    løsning = løs_andregradslikning(a, b, c)
    utdata = f"x = {løsning}"
    return andregradslikning_mal.format(inndata = inndata, utdata = utdata)

