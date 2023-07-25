# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:12:09 2023

@author: magdalon
"""

#Tittel

#Innledning

#---more---

##Biblioteker

#Vi begynner med å importere bibliotekene vi har tenkt å bruke.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sympy as sp


from flask import Blueprint, Flask, render_template, url_for, request
from wtforms import Form, SubmitField, SelectField
from markupsafe import Markup
from pathlib import Path

NETTSTEDTITTEL = "VM-kalkulator"
INNLEDNING = [Markup("<p>Denne webappen bruker lagenes <a href='https://www.fifa.com/fifa-world-ranking/women?dateId=ranking_20230609'>Fifa-rating</a> til å <a href='https://en.wikipedia.org/wiki/FIFA_Women%27s_World_Ranking#Ranking_procedure'>regne ut</a> vinnersjanser i utslagsrundene i fotball-VM for kvinner.</p>"),
              Markup("<p>Jeg har tidligere gjort de samme beregningene for Fotball-VM for herrer i Quatar: <a href='https://magdalon.wordpress.com/2022/12/03/hvem-vinner-vm/'>Hvem vinner VM?</a></p>"),
              Markup("<h3>Teori</h3>"),
              Markup("<p>Vi finner sannsynligheten <i>p</i> for at lag 1 vinner med formelen:</p>"),
              Markup("<p style='text-align: center;'><math xmlns = 'http://www.w3.org/1998/Math/MathML'><mrow><mi>p</mi><mo>=</mo><mfrac><mn>1</mn><mrow><mn>1</mn><mo>+</mo><msup><mn>10</mn><mrow><mo>-</mo><mfrac><mi>x</mi><mn>2</mn></mfrac></mrow></msup></mrow></mfrac></mrow></math></p>"),
              Markup("<p>Hvor <i>x</i> avhenger av forholdet mellom rankingen til de to lagene:</p>"),
              Markup("<p style='text-align: center;'><math xmlns = 'http://www.w3.org/1998/Math/MathML'><mrow><mi>x</mi><mo>=</mo><mrow><mrow><mfrac><msub><mi>R</mi><mi>1</mi></msub><mn>200</mn></mfrac></mrow><mo>-</mo><mrow><mfrac><msub><mi>R</mi><mi>2</mi></msub><mn>200</mn></mfrac></mrow></mrow></mrow></math></p>"),
              Markup("<p> Siden vi ser på utslagsrundene ser vi vekk i fra sannsynligheten for uavgjort, så sannsynligheten for at lag 2 vinner blir <i>1 - p</i>.</p>")]

navn = Path(__file__).parts[-2]
bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')

score = {'Argentina' : 1682.45,
 'Australia' : 1919.69,
 'Brasil' : 1995.3,
 'Canada' : 1996.34,
 'Columbia' : 1702.64,
 'Costa Rica' : 1596.94,
 'Danmark' : 1866.25,
 'England' : 2040.76,
 'Filipinene' : 1512.97,
 'Frankrike' : 2026.65,
 'Haiti' : 1475.33,
 'Irland' : 1743.59,
 'Italia' : 1846.5,
 'Jamaica' : 1536.81,
 'Japan' : 1916.68,
 'Kina' : 1854.49,
 'Marokko' : 1334.08,
 'Nederland' : 1980.47,
 'New Zealand' : 1699.7,
 'Nigeria' : 1554.94,
 'Norge' : 1908.25,
 'Panama' : 1482.51,
 'Portugal' : 1745.13,
 'Spania' : 2002.28,
 'Sveits' : 1765.9,
 'Sverige' : 2049.71,
 'Sør-Afrika' : 1471.52,
 'Sør-Korea' : 1840.27,
 'Tyskland' : 2061.56,
 'USA' : 2090.03,
 'Vietnam' : 1648.,
 'Zambia' : 1298.31}

grupper = {'A': ['Norge', 'Sveits', 'New Zealand', 'Filipinene'],
           'B': ['Canada', 'Australia', 'Irland', 'Nigeria'],
           'C': ['Spania', 'Japan', 'Costa Rica', 'Zambia'],
           'D': ['England', 'Danmark', 'Kina', 'Haiti'],
           'E': ['USA', 'Nederland', 'Portugal', 'Vietnam'],
           'F': ['Frankrike', 'Brasil', 'Jamaica', 'Panama'],
           'G': ['Sverige', 'Italia', 'Argentina', 'Sør-Afrika'],
           'H': ['Tyskland', 'Sør-Korea', 'Columbia', 'Marokko']}
def p(score1, score2):
    return 1/(10**(-(score1 - score2)/400) + 1)

rekkefølge = ['A1', 'C2','C1', 'A2', 'E1','G2','G1','E2', 'B1', 'D2', 'D1', 'B2', 'H1', 'F2', 'F1', 'H2']

rating = 'FIFA-rating'
pg = 'Videre fra gruppe-spill'
p8 = 'Vinner åttendedels-finale'
pq = 'Vinner kvart-finale'
ps = 'Vinner semi-finale'
p1 = 'Vinner VM'

def beregn(lag):
    df = pd.DataFrame({rating : [score[l] for l in lag],
                       pg : 1,
                       p8 : 0,
                       pq : 0,
                       ps : 0,
                       p1 : 0},
                      index = lag)

    for n in range(0, 4):
        offset = 2**n
        for i in range(8//offset):
            forrige = df.columns[n + 1]
            neste = df.columns[n + 2]
            for j in range(offset):
                for k in range(offset):
                    a = df.index[2*offset*i + j]
                    b = df.index[2*offset*i + offset + k]
                    df.at[a, neste] += df.at[a,forrige]*df.at[b,forrige]*p(df.at[a, rating], df.at[b, rating])
                    df.at[b,neste] += df.at[a,forrige]*df.at[b,forrige]*p(df.at[b, rating], df.at[a, rating])

    return df

def forbered_enkel(**kwargs):
    df = beregn([kwargs[pos] for pos in rekkefølge])
    return [Markup(f"<p>Det er <b>{df[p1].max():.1%}</b> sannsynlighet for at <b>{df[p1].idxmax()}</b> vinner fotball-VM for kvinner 2023.</p>"),
            Markup(df.to_html(float_format=lambda x: f"{x:.3f}", justify='center')),
            ]

class Enkeltskjema(Form):
    A1 = SelectField("Vinner gruppe A", choices = grupper['A'], default = grupper['A'][0])
    A2 = SelectField("Andreplass gruppe A", choices = grupper['A'], default = grupper['A'][1])
    B1 = SelectField("Vinner gruppe B", choices = grupper['B'], default = grupper['B'][0])
    B2 = SelectField("Andreplass gruppe B", choices = grupper['B'], default = grupper['B'][1])
    C1 = SelectField("Vinner gruppe C", choices = grupper['C'], default = grupper['C'][0])
    C2 = SelectField("Andreplass gruppe C", choices = grupper['C'], default = grupper['C'][1])
    D1 = SelectField("Vinner gruppe D", choices = grupper['D'], default = grupper['D'][0])
    D2 = SelectField("Andreplass gruppe D", choices = grupper['D'], default = grupper['D'][1])
    E1 = SelectField("Vinner gruppe E", choices = grupper['E'], default = grupper['E'][0])
    E2 = SelectField("Andreplass gruppe E", choices = grupper['E'], default = grupper['E'][1])
    F1 = SelectField("Vinner gruppe F", choices = grupper['F'], default = grupper['F'][0])
    F2 = SelectField("Andreplass gruppe F", choices = grupper['F'], default = grupper['F'][1])
    G1 = SelectField("Vinner gruppe G", choices = grupper['G'], default = grupper['G'][0])
    G2 = SelectField("Andreplass gruppe G", choices = grupper['G'], default = grupper['G'][1])
    H1 = SelectField("Vinner gruppe H", choices = grupper['H'], default = grupper['H'][0])
    H2 = SelectField("Andreplass gruppe H", choices = grupper['H'], default = grupper['H'][1])
    beregn = SubmitField("Beregn!")

@bp.route('/enkel')
def vis_enkel():
    skjema = Enkeltskjema(request.args)
    print(request.args)
    if skjema.validate():
      utdata = forbered_enkel(**skjema.data)
    else:
      utdata = []
    return render_template("default.html",
                           tittel=NETTSTEDTITTEL,
                           innledning=INNLEDNING,
                           skjema = skjema,
                           utdata = utdata,
                           bakgrunn = "bilder/bakgrunn/rapinoe.jpg")

from wtforms import FormField, FieldList, StringField
from collections import defaultdict
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint

defaultdata = ImmutableMultiDict([('resultat-0-0', 'Norge'), ('resultat-0-1', 'Sveits'),('resultat-1-0', 'Canada'), ('resultat-1-1', 'Australia'), ('resultat-2-0', 'Spania'),('resultat-2-1', 'Japan'), ('resultat-3-0', 'England'), ('resultat-3-1', 'Danmark'),('resultat-4-0', 'USA'), ('resultat-4-1', 'Nederland'), ('resultat-5-0', 'Frankrike'),('resultat-5-1', 'Brasil'), ('resultat-6-0', 'Sverige'), ('resultat-6-1', 'Italia'),('resultat-7-0', 'Tyskland'), ('resultat-7-1', 'Sør-Korea'), ('beregn', 'Beregn')])


from wtforms.validators import data_required, ValidationError
vinnere = [gruppe[0] for gruppe in grupper.values()]
toere = [gruppe[1] for gruppe in grupper.values()]
default = list(zip(vinnere, toere))
def lag_tabellskjema(ra=defaultdata):
    class Tabellskjema(Form):
        resultat = FieldList(FieldList(SelectField(coerce=str, validators=[data_required()]), min_entries=2), min_entries=8, default=default)
        beregn = SubmitField('Beregn')
        def validate_resultat(form, field):
            for w, r in field.data:
                if w ==r:
                    raise ValidationError("Gruppevinner og gruppetoer er samme lag!")

    skjema = Tabellskjema(ra)
    for i, gruppe in enumerate(grupper.values()):
        for j in range(2):
            skjema.resultat[i][j].choices = gruppe
        skjema.resultat[i].default = gruppe[0:1]
    return skjema

skjema = lag_tabellskjema(defaultdata)

def forbered_inputtabell(resultat, **kwargs):
    lag = [resultat[ord(g) - 65][int(l) - 1] for g, l in rekkefølge]
    df = beregn(lag)
    return [Markup(f"<p>Det er <b>{df[p1].max():.1%}</b> sannsynlighet for at <b>{df[p1].idxmax()}</b> vinner fotball-VM for kvinner 2023.</p>"),
            Markup(df.to_html(float_format=lambda x: f"{x:.3f}", justify='center')),
            ]

@bp.route('/inputtabell')
def vis_inputtabell():
    skjema = lag_tabellskjema(request.args)
    if skjema.validate():
      utdata = forbered_inputtabell(**skjema.data)
    else:
      utdata = []
    return render_template("inputtabell.html",
                           tittel=NETTSTEDTITTEL,
                           innledning=INNLEDNING,
                           skjema = skjema,
                           utdata = utdata,
                           bakgrunn = "bilder/bakgrunn/rapinoe.jpg")

from matplotlib.figure import Figure
import base64
from io import BytesIO

plt.rcParams.update({'font.size': 14})
def tegn_søylediagram(df):
    #Setter opp tegnevinduet
    fig = Figure(figsize=(5.7, 4), tight_layout=True)
    ax = fig.subplots()

    #Tegner grafen
    farge = "green"
    with plt.xkcd():
        df[p1].sort_values().plot.barh(ax=ax, color=farge, edgecolor="black", width=0.8)

    #Returnerer en img-tag
    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return Markup(f"<img src='data:image/png;base64,{data}'>")

def forbered_søyle(resultat, **kwargs):
    lag = [resultat[ord(g) - 65][int(l) - 1] for g, l in rekkefølge]
    df = beregn(lag)
    return [Markup("<h4>Mest sannsynlige vinner</h4>"),
            Markup(f"<p>Det er <b>{df[p1].max():.1%}</b> sannsynlighet for at <b>{df[p1].idxmax()}</b> vinner fotball-VM for kvinner 2023.</p>"),
            Markup("<h4>Kampsannsynligheter</h4>"),
            Markup(df.to_html(float_format=lambda x: f"{x:.3f}",
                              formatters={rating: lambda x: f"{x:.2f}"},
                              justify='center')),
            Markup("<h4>Rangerte vinnersannsynligheter</h4>"),
            Markup(tegn_søylediagram(df))
            ]
@bp.route('/', endpoint='vis')
@bp.route('/søyle')
def vis_søyle():
    #print(request.args)
    skjema = lag_tabellskjema(request.args)
    if skjema.validate():
      utdata = forbered_søyle(**skjema.data)
    else:
      skjema = lag_tabellskjema()
      utdata = forbered_søyle(**skjema.data)
    return render_template("inputtabell.html",
                           tittel=NETTSTEDTITTEL,
                           innledning=INNLEDNING,
                           skjema = skjema,
                           utdata = utdata,
                           bakgrunn = "bilder/bakgrunn/rapinoe.jpg")



def forbered_bracket(resultat, **kwargs):
    pass

@bp.route('/bracket')
def vis_bracket():
    skjema = lag_tabellskjema(request.args)
    if skjema.validate():
      utdata = forbered_inputtabell(**skjema.data)
    else:
      utdata = []
    return render_template("bracket.html",
                           tittel=NETTSTEDTITTEL,
                           innledning=INNLEDNING,
                           skjema = skjema,
                           utdata = utdata,
                           bakgrunn = "bilder/bakgrunn/rapinoe.jpg")

app = Flask(__name__)
@app.route('/innhold')
def vis():
  utdata = []
  for rule in app.url_map.iter_rules():
    if not rule.arguments:
      utdata.append(Markup(f"<a href='{url_for(rule.endpoint)}'>{rule}</a>"))
  return render_template("default.html",
                         tittel = NETTSTEDTITTEL,
                         innledning=INNLEDNING,
                         utdata=utdata)

app.register_blueprint(bp)


