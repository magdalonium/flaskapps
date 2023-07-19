# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."


generell_mal = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Lineær regresjon</title>
    <link rel="stylesheet" href="/static/default.css" type="text/css">
    <style>
        .tall {{width: 40px}}
    </style>
  </head>
  <body>
    <h1>Lineær regresjon</h1>
    <h2>Inntasting</h2>
    {skjema}
    <h2>Input</h2>
    <p>{inndata}</p>
    <h2>Output</h2>
    {utdata}
  </body>
<html>
"""

skjema =f"""<form method='GET'>
      <table class='regneark'>
        
        <tr>
          <th>x</th>
          {"<td><input name='x'></td>"*10}
        </tr>
        <tr>
          <th>y</th>
          {"<td><input name='y'></td>"*10}
        </tr>
      </table>
    <p>
      <input type="submit" value="Beregn">
    </p>
    </form>
"""

from scipy.optimize import curve_fit

def linreg(x, y):
    #Modellfunksjon
    def modell(x, a, b):
        return a*x + b

    #Startgjett
    a0 = (y[-1] - y[0])/(x[-1] - x[0]) #skjør metode, svikter når x[-1] = x[0]
    b0 = y[0] - a0*x[0]
    
    #Gjennomfører regresjonen
    res = curve_fit(modell, x, y, [a0, b0])

    #Lager og returnerer et løsningsobjekt.
    
    løsning = {'funksjon' : lambda x: modell(x, *res[0]),
               'a': res[0][0],
               'b': res[0][1]}
    return løsning


import base64
import numpy as np

from io import BytesIO
from matplotlib.figure import Figure 

def tegn_linreg(fun, x, y):
    #Setter opp x-verdiene
    xmin, xmax = np.min(x), np.max(x)
    X = np.linspace(xmin, xmax)

    #Setter opp tegnevinduet
    fig = Figure(figsize=(6, 3), tight_layout=True)
    ax = fig.subplots()
    
    #Tegner regresjonslinje og data
    ax.plot(X, fun(X), color="blue")
    ax.scatter(x, y, color="orange")
    ax.grid()
    
    #Returnerer en img-tag
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'>"


from flask import request

@app.route('/linreg')
def show_linreg():
    if len(request.args)>0:
        x = [float(e) for e in request.args.getlist('x') if e]
        y = [float(e) for e in request.args.getlist('y') if e]
        inndata = str(x) + "<br>" + str(y)
        løsning = linreg(x, y)
        utdata = "<p>y = {a:.3g}x + {b:.3g}</p>\n".format(**løsning)
        utdata += tegn_linreg(løsning['funksjon'], x, y)+"\n"
    else:
        inndata=""
        utdata =""
    return generell_mal.format(skjema = skjema,
                               inndata = inndata,
                               utdata = utdata)
