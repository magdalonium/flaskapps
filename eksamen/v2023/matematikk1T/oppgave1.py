# -*- coding: utf-8 -*-
import numpy as np
import base64
from flask import Flask, render_template, request, url_for
from io import BytesIO
from markupsafe import Markup
from matplotlib.figure import Figure
from sympy import (Eq, Function, mathml, Symbol, symbols,
 sympify)
from wtforms import ( FieldList, FloatField, Form,
  IntegerField, StringField, SubmitField )
from wtforms.validators import DataRequired
from wtforms import RadioField
from sympy import lambdify, solveset


##Oppgavetekst
"""
De siste årene har Lars bodd på Svalbard fra 1. februar til 1. oktober. Hvert år har han målt temperaturen utenfor huset sitt på ulike tidspunkt noen dager hver uke.
Han har funnet at funksjonen <i>T</i> gitt ved
T(x) = 0,048x4 −1,4x3 +13,36x2 − 45,8x + 35,2 , 2 ≤ x ≤10

er en rimelig bra modell for gjennomsnittstemperaturen <i>T(x) [deg]C</i> hvert døgn de månedene han bor på Svalbard, når han lar <i>x=2</i> svare til 1. februar, <i>x=3</i> til 1. mars, <i>x=4</i> til 1. april og så videre.
a) Omtrent hvor mange døgn i perioden 1. februar–1. oktober er gjennomsnittstemperaturen over 0[deg]C ifølge modellen?
b) Bestem stigningstallet til den rette linjen som går gjennom punktene (3, <i>T</i>(3)) og (7, <i>T</i>(7)). Gi en praktisk tolkning av dette stigningstallet.
"""


#Konstanter

NETTSTEDTITTEL = "Eksamen 1T V2023 Del 1"
x = Symbol("x")


app = Flask(__name__)

#Vi setter opp en enkel innholdsside som inneholder lenker til enkeltoppgavene vi lager senere. Vi finner sider og nettadresser ved å gå gjennom applikasjonen vår sitt <code>url_map</code>-objekt med en for-løkke. Hver gang vi legger til en regel med <code>@app.route</code> kommer det en ny oppføring i dette objektet.

#Vi henter ut stien til hver regel med koden url_for(rule.endpoint) og bruker dette til å gjøre regeloppføringene om til klikkbare lenker.

@app.route('/')
def vis():
  utdata = []
  for rule in app.url_map.iter_rules():
    if not rule.arguments:
      utdata.append(Markup(f"<a href='{url_for(rule.endpoint)}'>{rule}</a>"))
  return render_template("base.html", tittel = NETTSTEDTITTEL, utdata=utdata)

class Skjema(Form):
    funksjonsuttrykk = StringField()
    x1 = FloatField(default=3)
    x2 = FloatField(default=7)
    beregn = SubmitField()

@app.route('løsning')
def vis_løsning():
    pass
