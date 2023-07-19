# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 16:40:57 2023

@author: magdalon
"""

#Eksamen i Matematikk 1T vår 2023: Del 1 - webapp

#Jeg har sett på hvordan vi kan lage webapper som løser Eksamen i Matematikk 1T våren 2023 etter den nye læreplanen. Vi skal lage webapper for prosentregning, arealberegninger, regresjon og proporsjonale størrelser. Vi skal lage webappene med Flask, Jinja og WTForms.

#---more---

##Oppsett

###Mal

#Vi setter opp en standard HTML-mal med Jinja som vi kan bruke til å hente inn tall og returnere svar i webappen vår. Vi lagrer denne malen som <kbd>base.html</kbd> i undermappen <kbd>templates</kbd>. Denne malen bruker stilarket <kbd>default.css</kbd> som er lagret i undermappen <kbd>static</kbd>.

#Denne malen tar inn variablene <code>tittel</code>, <code>skjema</code> og <code>utdata</code>.
#*Tittelen er en tekststreng med sidetittelen.
#*Skjema er et WTForms-objekt som vi bruker til å lage et input-skjema. Vi bruker en for-blokk i malen til å skrive ut alle feltene i skjemaet. Skjemadataene blir sendt til serveren med <kbd>GET</kbd>-metoden, dvs. i adressefeltet.
#*Utdata er en liste eller ordliste med utdata. Dersom utdata er en liste skriver vi hvert element ut som et avsnitt, men hvis utdata er en ordliste skriver vi det ut som en definisjonliste med <i>nøkkel-verdi</i>-par.

#base.html

###Biblioteker og funksjoner

#Vi begynner med å importere bibliotekene vi har tenkt å bruke. Vi lager all Python-koden vi skriver i filen <kbd>1PH22-del1.py</kbd>.

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

#Konstanter

NETTSTEDTITTEL = "Eksamen 1T V2023 Del 1"
x = Symbol("x")


###App

#Vi kan nå sette opp app-objektet med <code>Flask</code>.

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

#Vi kan nå åpne et Anaconda/Python-skall og navigere oss til arbeidsmappen vår. Vi setter opp en testserver for webappen vår ved å skrive:

#flask --app 1PH22-del1 --debug run

#BILDE

#Vi finner webappen vår i en nettleser ved å skrive inn <kbd>localhost:5000</kbd>.

#BILDE

#Etterhvert som vi legger til visningsfunksjoner vil denne listen bli lengre.

##Oppgave 1: Trigonometri

"""
[BILDE]En rettvinklet trekant har sidelengder 8, 6, 10. Se figuren til høyre.
Vis at
(sin<i>u</i>)<sup>2</sup> + (cos<i>u</i>)<sup>2</sup> = 1
"""
from sympy import Rational
TOL = 1e-5

class Skjema1(Form):
    Sidelengde = FieldList(IntegerField(validators=[DataRequired()]), min_entries=3, default = [6, 8, 10])
    beregn = SubmitField('Beregn!')

def tegn_trekant(k1, k2, h):
    #Finner toppen av trekanten
    a = (h**2 + k1**2 - k2**2)/(2*k1)
    b = np.sqrt(-(h - k1 - k2)*(h - k1 + k2)*(h + k1 - k2))*np.sqrt(h + k1 + k2)/(2*k1)
    #Setter opp tegnevinduet
    fig = Figure(figsize=(6, 3), tight_layout=True)
    ax = fig.subplots()
    #Tegner trekanten
    ax.fill([0, k1, a], [0, 0, b], alpha=0.3,
            color="red", edgecolor="red")
    ax.axis(False)
    ax.axis('scaled')
    #Returnerer en img-tag
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return Markup(f"<img src='data:image/png;base64,{data}'>")

def oppgave1(**kwargs):
    k1, k2, h = sorted(kwargs['Sidelengde'])
    ret = {}
    ret["Tegning"] = tegn_trekant(k1, k2, h)
    if np.abs(h**2 - (k1**2 + k2**2)) > TOL:
        ret["Kommentar"]= "Ikke rettvinklet. Prøv med sidelengdene 6, 8 og 10"
    sinu = Rational(k2, h)
    cosu = Rational(k1, h)
    ret["sinu**2 + cosu**2"] = sinu**2 + cosu**2
    ret["sinu**2 + cosu**2 = 1"] = sinu**2 + cosu**2==1
    return ret

@app.route('/oppgave1')
def vis1():
    skjema = Skjema1(request.args)
    if skjema.validate():
      utdata = oppgave1(**skjema.data) if skjema.validate() else []
    else:
      utdata = []
    return render_template("base.html",
                           tittel=NETTSTEDTITTEL + " - " + "Oppgave 1",
                           skjema = skjema,
                           utdata = utdata)

#%%
###Tillegg: Utledning av formelen for toppunktet
#[SKISSE]

if __name__ == '__main__':
    from sympy import nonlinsolve
    k1, k2, h, a, b = symbols(["k1", "k2", "h", "a", "b"], positive=True)
    l1 = Eq(a**2 + b**2, h**2)
    l2 = Eq((k1 - a)**2 + b**2, k2**2)

    løsn = nonlinsolve([l1, l2], [a, b])
    print(løsn)
    av, bv = list(løsn)[1]
    print(av)
    print(bv)

#%%
##Oppgave 2
"""
Funksjonen <i>f</i> er gitt ved
<i>f(x) = x<sup>2</sup> - 2x - 8</i>
I hvilke punkter skjærer grafen til funksjonen <i>x</i>-aksen?
"""

class Skjema2(Form):
    funksjonsuttrykk = StringField(validators = [DataRequired()], filters = [sympify], default ="x**2 - 2*x - 8")
    beregn = SubmitField('Beregn!')

def skjæringspunkt(f):
    løsn = solveset(f)
    X = list(løsn)
    return X

def tegn_funksjon(f, X=None, xlim=None):
    if xlim:
        xmin, xmax = xlim
    elif X:
        xmin, xmax = float(min(X)) - 1, float(max(X)) + 1
    else:
        xmin, xmax = -1, 1
    variabler = f.free_symbols
    if len(variabler)==0:
        fun = lambda x: [float(f)]*len(x)
    else:
        variabel = list(variabler)[0]
        fun = lambdify(variabel, f)

    T = np.linspace(xmin, xmax)
    print(T)
    print(fun(T))
    #Setter opp tegnevinduet
    fig = Figure(figsize=(6, 3), tight_layout=True)
    ax = fig.subplots()
    #Tegner grafen
    ax.plot(T, fun(T))
    if X: ax.scatter(X, [0]*len(X), color="red")
    ax.axhline(0, color="black")
    ax.grid()
    #Returnerer en img-tag
    buf = BytesIO()
    fig.set_size_inches(7, 3)
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return Markup(f"<img src='data:image/png;base64,{data}'>")

def oppgave2(funksjonsuttrykk, **kwargs):
    if len(funksjonsuttrykk.free_symbols) > 1:
        return ["For mange variabler!"]
    X = skjæringspunkt(funksjonsuttrykk)
    graf = tegn_funksjon(funksjonsuttrykk, X)
    return [f"Skjæringspunkt: {X}",
            graf]

@app.route('/oppgave2')
def vis2():
    skjema = Skjema2(request.args)
    if skjema.validate():
      utdata = oppgave2(**skjema.data)
    else:
      utdata = []
    return render_template("base.html",
                           tittel=NETTSTEDTITTEL + " - " + "Oppgave 2",
                           skjema = skjema,
                           utdata = utdata)


#%%

#Oppgave 3

"""
Gitt likningen
<i>x<sup>3</sup> - 5x<sup>2</sup> - 8x + 12 = (x - 1)(x + a)(x - b)</i>
Bestem <i>a</i> og <i>b</i> slik at likningen blir en identitet.
"""

#Generalisering: Løse tredjegradslikninger

def formater_matematikk(expr):
    subs = [("<mfenced>", "<mrow><mo>(</mo>"),
            ("</mfenced>", "<mo>)</mo></mrow>")]
    tekst = mathml(expr , printer='presentation')
    for g, n in subs:
        tekst =  tekst.replace(g, n)
    return Markup("<math>" + tekst + "</math>")

def oppgave3(venstreside, **kwargs):
    likn = Eq(venstreside, venstreside.factor())
    return formater_matematikk(likn)

class Skjema3(Form):
    venstreside = StringField(validators = [DataRequired()], filters = [sympify], default ="x**3 - 5*x**2 - 8*x + 12")
    beregn = SubmitField('Beregn!')


@app.route('/oppgave3')
def vis3():
    skjema = Skjema3(request.args)
    if skjema.validate():
      utdata = [oppgave3(**skjema.data)]
    else:
      utdata = []
    return render_template("base.html",
                           tittel=NETTSTEDTITTEL + " - " + "Oppgave 3",
                           skjema = skjema,
                           utdata = utdata)



#%%

##Oppgave 4

"""
Nedenfor ser du grafen til en rasjonal funksjon <i>f</i>.
Bestem <i>f</i>(<i>x</i>). Husk å argumentere for at svaret ditt er riktig.
[BILDE]
"""
from sympy import limit, singularities, oo, nonlinsolve

def finn_funksjon(va, ha, punkt):
    a, b, c, x = symbols(["a", "b", "c", "x"])
    f = a*(x + c)/(x + b)
    l1 = Eq(list(singularities(f, x))[0], va)
    l2 = Eq(limit(f, x, oo), ha)
    l3 = Eq(f.subs(x, punkt[0]), punkt[1])
    løsn = nonlinsolve([l1, l2, l3], [a, b, c])
    av, bv, cv = list(løsn)[0]
    return f.subs({a: av, b: bv, c:cv})

if __name__ == '__main__':
    print(finn_funksjon(1, 3, (0, 6)))

def tegn_rasjonal_funksjon(f, va, ha):
    variabler = f.free_symbols
    if len(variabler) == 1:
        variabel = list(variabler)[0]
        fun = lambdify(variabel, f)
    else:
        return "Kunne ikke tegne funksjonen"
    xlim = [va - 8, va + 8]
    ylim = [ha - 7, ha + 6]
    T1 = np.linspace(xlim[0], va-TOL)
    T2 = np.linspace(va + TOL, xlim[1])

    #Setter opp tegnevinduet
    fig = Figure(figsize=(6, 3), tight_layout=True)
    ax = fig.subplots()
    #Tegner grafen
    ax.plot(T1, fun(T1), color="#b2d9c7")
    ax.plot(T2, fun(T2), color="#b2d9c7")
    ax.axvline(va, linestyle="--", color="#0048aa")
    ax.axhline(ha, linestyle="--", color="#0048aa")
    if xlim[0] < va < xlim[1]:
        ax.axvline(0, color="black")
    if ylim[0] < ha < ylim[1]:
        ax.axhline(0, color="black")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.grid()
    #Returnerer en img-tag
    buf = BytesIO()
    fig.set_size_inches(7, 3)
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return Markup(f"<img src='data:image/png;base64,{data}'>")

if __name__ == '__main__':
    print(tegn_funksjon(finn_funksjon(1, 3, (0, 6)), 1, 3))

def oppgave4(va, ha, px, py, **kwargs):
    f = finn_funksjon(va, ha, (px, py))
    return [f,
            formater_matematikk(Eq(Function("f")(x), f, doit=False)),
            tegn_rasjonal_funksjon(f, va, ha)]

class Skjema4(Form):
    va = FloatField("Vertikal asymptote", default = 1)
    ha = FloatField("Horisontal asymptote", default = 3)
    px = FloatField("Punkt-x", default = 0)
    py = FloatField("Punkt-y", default = 6)
    finn = SubmitField('Finn funksjon!')

@app.route('/oppgave4')
def vis4():
    skjema = Skjema4(request.args)
    if skjema.validate():
      utdata = oppgave4(**skjema.data)
    else:
      utdata = []
    return render_template("base.html",
                           tittel=NETTSTEDTITTEL + " - " + "Oppgave 4",
                           skjema = skjema,
                           utdata = utdata)

##Oppgave 5

"""
[BILDE]
Ovenfor ser du grafen til den deriverte av en funksjon .
Nullpunktene til er x = -5, x = -2, x=4 og x=6
Lag en skisse som viser hvordan grafen til <i>f</i> kan se ut.
Husk å argumentere for hvorfor du mener skissen er riktig.
"""

def finn_funksjon5(nullpunkter, positiv):
    return (-1)**(1-positiv) * np.product(x - np.array(nullpunkter))

def oppgave5(nullpunkter, positiv, **kwargs):
    f = finn_funksjon5(nullpunkter, positiv)
    utdata = [Markup("<h2>Løsning</h2>"),
              Markup("<h3>Funksjonsuttrykk</h3>"),
              formater_matematikk(Eq(Function('f')(x), f)),
              formater_matematikk(Eq(Function('f')(x), f.expand())),
              Markup("<h3>Grafen til f(x)</h3>"),
              tegn_funksjon(f, nullpunkter),
              Markup("<h3>Grafen til f'(x)</h3>"),
              tegn_funksjon(f.diff(x), xlim = [min(nullpunkter) - 1, max(nullpunkter) + 1]),
              ]
    return utdata



class Skjema5(Form):
    nullpunkter = FieldList(FloatField(validators=[DataRequired()]), min_entries=4, default = [-4, -2, 4, 6])
    positiv = RadioField("f(0) positiv", validators=[DataRequired()], choices=[( True, 'Sann'), (False, 'Usann')], default=True, coerce=bool)
    finn = SubmitField('Finn funksjon!')

@app.route('/oppgave5')
def vis5():
    skjema = Skjema5(request.args)
    if skjema.validate():
      utdata = oppgave5(**skjema.data)
    else:
      utdata = []
    return render_template("base.html",
                           tittel=NETTSTEDTITTEL + " - " + "Oppgave 5",
                           skjema = skjema,
                           utdata = utdata)


