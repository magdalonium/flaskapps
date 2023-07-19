# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."


from time import strftime

@app.route('/klokke')
def show_klokke():
    klokkeslett = strftime('%H:%M:%S')
    return f"Klokken er {klokkeslett}."


@app.route('/input/<inndata>')
def show_input_test(inndata):
    return f"Du skrev inn {inndata}."


@app.route('/multiinput/<string:tekst>/<int:heltall>/<float:desimaltall>')
def show_multiinputtest(tekst, heltall, desimaltall):
    return f"Tekst: {tekst}<br>Heltall: {heltall}<br>Desimaltall: {desimaltall}"

@app.route('/kvadrat/<int:tall>')
def show_kvadrat(tall):
    return str(tall**2)

fancykvadrat_mal = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Fancykvadrat</title>
    <link rel="stylesheet" href="/static/default.css" type="text/css">
  </head>
  <body>
    <h1>Fancykvadrat</h1>
    <h2>Input</h2>
    <p>{inndata}</p>
    <h2>Output</h2>
    <p>{utdata}</p>
  </body>
<html>
"""

@app.route('/fancykvadrat/<int:tall>')
def show_fancykvadrat(tall):
    return fancykvadrat_mal.format(inndata = tall,
                                   utdata = tall**2)

#Tillegg
from flask import render_template
@app.route('/stigenerator')
def show_stigenerator():
    utdata = [None]
    return render_template("default.html", tittel = "Flask del 8: Mer om Jinja-uttrykk", utdata=utdata)
