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
from flask import render_template, request, url_for
from wtforms import Form, IntegerField, FloatField, StringField, SubmitField
from markupsafe import Markup


class Inndataskjema(Form):
    inndata = StringField(default="Barbie")
    submit = SubmitField("Lag sti")

@app.route('/stigenerator/input')
def show_inputgenerator():
    skjema = Inndataskjema(request.args)
    if skjema.validate():
      sti = url_for('.show_input_test', inndata = skjema.inndata.data)
      utdata =  [Markup(f"Prøv å følge stien: <a href='{sti}'>{sti}</a>")]
    else:
      utdata = []
    return render_template("default.html",
                           tittel="Flask del 3 - Stigenerator",
                           skjema = skjema,
                           utdata = utdata)


class Multiinputskjema(Form):
    tekst = StringField(default = "Ken")
    heltall = IntegerField(default = 42)
    desimaltall = FloatField(default = 3.14)
    submit = SubmitField("Lag sti")

@app.route('/stigenerator/multiinput')
def show_multiinputgenerator():
    skjema = Multiinputskjema(request.args)
    if skjema.validate():
      sti = url_for('.show_multiinputtest',
                    tekst = skjema.tekst.data,
                    heltall = skjema.heltall.data,
                    desimaltall = skjema.desimaltall.data)
      utdata =  [Markup(f"Prøv å følge stien: <a href='{sti}'>{sti}</a>")]
    else:
      utdata = []
    return render_template("default.html",
                           tittel="Flask del 3 - Stigenerator",
                           skjema = skjema,
                           utdata = utdata)

class Kvadratskjema(Form):
    tall = IntegerField(default="2")
    submit = SubmitField("Lag sti")

@app.route('/stigenerator/kvadrat')
def show_kvadratgenerator():
    skjema = Kvadratskjema(request.args)
    if skjema.validate():
      sti = url_for('.show_kvadrat', tall = skjema.tall.data)
      utdata =  [Markup(f"Prøv å følge stien: <a href='{sti}'>{sti}</a>")]
    else:
      utdata = []
    return render_template("default.html",
                           tittel="Flask del 3 - Stigenerator",
                           skjema = skjema,
                           utdata = utdata)

@app.route('/stigenerator/fancykvadrat')
def show_fancykvadratgenerator():
    skjema = Kvadratskjema(request.args)
    if skjema.validate():
      sti = url_for('.show_fancykvadrat', tall = skjema.tall.data)
      utdata =  [Markup(f"Prøv å følge stien: <a href='{sti}'>{sti}</a>")]
    else:
      utdata = []
    return render_template("default.html",
                           tittel="Flask del 3 - Stigenerator",
                           skjema = skjema,
                           utdata = utdata)

