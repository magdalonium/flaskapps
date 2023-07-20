# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 18:43:28 2023

@author: magdalon
"""

#Eksamen i Matematikk 1P(LK20) høst 2022: Del 1 - webapp

#Jeg har sett på hvordan vi kan lage webapper som løser Eksamen i Matematikk 1P høsten 2022 etter den nye læreplanen. Vi skal lage webapper for prosentregning, arealberegninger, regresjon og proporsjonale størrelser. Vi skal lage webappene med Flask, Jinja og WTForms.

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
from scipy.optimize import curve_fit
from sympy import Eq, Function, mathml, Symbol, sympify
from werkzeug.datastructures import ImmutableMultiDict
from wtforms import ( FieldList, FloatField, Form,
  FormField, IntegerField, SelectField, StringField,
  SubmitField )
from wtforms.validators import ( NumberRange,
  DataRequired )

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
    else:
      utdata.append(rule.rule)
  return render_template("base.html", tittel = "Hjem", utdata=utdata)

#Vi kan nå åpne et Anaconda/Python-skall og navigere oss til arbeidsmappen vår. Vi setter opp en testserver for webappen vår ved å skrive:

#flask --app 1PH22-del1 --debug run

#BILDE

#Vi finner webappen vår i en nettleser ved å skrive inn <kbd>localhost:5000</kbd>.

#BILDE

#Etterhvert som vi legger til visningsfunksjoner vil denne listen bli lengre.

##Oppgave 1

"""
I 2022 må innbyggerne i Lindesnes kommune betale 3,0 ‰ i eiendomsskatt. Eiendomsskatten beregnes ut fra en eiendoms likningsverdi.
Familien Hansen har en bolig med likningsverdi 2 500 000 kroner.
a) Hvor mye betaler familien Hansen i eiendomsskatt i 2022?
I 2023 vil satsen øke fra 3,0 ‰ til 3,5 ‰.
b) Hvor mange prosentpoeng er endringen på?
"""

###Grunnleggende

#Vi lager et skjema som henter inn tallene fra oppgaven. Dette skjemaet får fire felt: To flyttallsfelt(<code>FloatField</code>) som henter inn eiendomsskattesatsen, et heltallsfelt(<code>IntegerField</code>) som henter inn likningsverdien og et innsendingsfelt (<code>SubmitField</code>) som gir oss en knapp for å sende inn. Vi gir tallfeltene valideringskravet <code>NumberRange(0)</code>, dette betyr at ingen av verdiene kan være negative. Vi gir disse datafeltene filteret <code>lambda x: x/1000 if x else x</code>, dette gjør at datafeltet automatisk regner om fra promille til prosentfaktor. Siden vi kan ha mer enn et valideringskrav og mer enn et filter, bruker vi i begge tilfeller lister.

class Skjema1(Form):
  sats2022 = FloatField("Eiendomsskatt 2022 (‰)",
                        [NumberRange(0)],
                        filters=[lambda x: x/1000 if x else x])
  sats2023 = FloatField("Eiendomsskatt 2022 (‰)",
                        [NumberRange(0)],
                        filters=[lambda x: x/1000 if x else x])
  likningsverdi = IntegerField("Liknignsverdi",
                               [NumberRange(0)])
  beregn = SubmitField('Beregn!')

#Vi lager en funksjon som svarer på oppgaven. Denne funksjonen får et ekstra parameter, <code>**kwargs</code>, dette gjør at alle ekstra argumenter til ordlisten <code>kwargs</code>.

def eiendomsskatt(sats2022, sats2023, likningsverdi, **kwargs):
  return {"eiendomsskatt2022": sats2022*likningsverdi,
          "eiendomsskatt2023": sats2023*likningsverdi}

#Vi registrerer en visningsfunksjon. Denne tar inn eventuelle data og returner en nettside hvor vi har satt inn skjemaet og eventuelle utdata. Vi tester om skjemaet er riktig fylt ut med skjemaets <code>validate</code>-metode. Dersom dette er riktig, sender vi skjemadataene som argumenter til <code>eiendomsskatt</code>-funksjonen. <code>**</code>-operatoren pakker ut en ordliste til en liste med <i><code>nøkkel=verdi</code></i>-par som vi kan bruke som funksjonsargumenter.

@app.route('/oppgave1')
def vis1():
  skjema = Skjema1(request.args)
  if skjema.validate():
    utdata = eiendomsskatt(**skjema.data)
  else:
    utdata = []
  return render_template("base.html",
                         tittel="Oppgave 1",
                         skjema = skjema,
                         utdata = utdata)

#BILDE


#%%

###Avansert: Flere boliger og år

#Vi ser at vi legger inn satsene to ganger. Vi kan derfor skrive om funksjonen vår til å legge inn eiendomsskattesatsene som en liste med (<i>år</i>, <i>sats</i>)-par. På samme måte kan vi legge inn boliger som en liste med (<i>familie</i>, <i>bolig</i>)-par.

#Vi lager først delskjemaer for satser og boliger.

class Satsskjema(Form):
  år = IntegerField("Årstall")
  verdi = FloatField("Sats(‰)",
                     [NumberRange(0)],
                     filters=[lambda x: x/1000 if x else x])


class Boligskjema(Form):
  familie = StringField("Familie")
  likningsverdi = FloatField("Boligverdi",
                             [NumberRange(0)])

#Vi kan nå legge inn delskjemaene som lister ved å først sende dem til <code>FormField</code> som for å gjøre dem om til datafelter, før vi sender de resulterende objektene til <code>FieldList</code> som gir oss en liste med disse feltene. Vi gir <code>FieldList</code>-konstruktørene det ekstra argumentet <code>min_entries</code> for å styre hvor mange felter vi skal vise i et tomt skjema.

#Vi legger også til noen nye kontroll-knapper: <kbd>Legg til bolig</kbd> og <kbd>Legg til år</kbd> for å legge til datafelter til listene våre, <kbd>Nullstill</kbd> for å tømme skjemaet og <kbd>Oppgavedata</kbd> for å0 legge inn tallene fra oppgaven.

class Eiendomsskatteskjema(Form):
  satser = FieldList(FormField(Satsskjema),
                     min_entries=2)
  boliger = FieldList(FormField(Boligskjema),
                      min_entries = 1)
  beregn = SubmitField("Beregn!")
  nybolig = SubmitField("Legg til bolig")
  nysats = SubmitField("Legg til år")
  nullstill = SubmitField("Nullstill")
  fyllinn = SubmitField("Oppgavedata")

#Vi lager en ny mal som arver fra <kbd>base.html</kbd>. Denne malen viser inntastingsfeltene for satser som en tabell og inntastingsfeltene for boliger som en annen tabell. Vi legger til så mange ekstra kolonner i bolig-feltet som det er oppgitt satser. Legg merke til at årstallene fra sats-skjemaet blir kolonneoverskrifter i bolig-skjemaet.

#[Oppgave1A]

#Siden dataformatet vårt er endret lager vi en ny eiendomsskattefunksjon. Denne gangen tar vi inn en verdi og en liste med satser. Vi gjør satser-listen til et Numpy-<code>array</code> og retunerer produktet av arrayet med likningsverdien. Dette gir oss en liste med eiendomsskatten hvert år for en bolig.

def eiendomsskatt_A(likningsverdi, satser, **kwargs):
  return np.array(satser)*likningsverdi

#Før vi lager visningsfunksjonen lager vi et dataobjekt for tallene fra oppgaveteksten.

oppgave1data = ImmutableMultiDict([('satser-0-år', '2022'), ('satser-0-verdi', '3'), ('satser-1-år', '2023'), ('satser-1-verdi', '3.5'), ('boliger-0-familie', 'Hansen'), ('boliger-0-likningsverdi', '2500000'), ('beregn', 'Beregn!')])

#Vi kan nå lage en visningsfunksjon. Det nye er at vi legger til en <code>if</code>-blokk som tester om noen av de nye knappene er trykket. Deretter lager vi en liste med satser, kodesnutten <code>if sats.validate(skjema)</code> gjør at vi bare tar med elementer som er riktig fylt inn.

#Til slutt går vi gjennom listen med familier. For alle familier regner vi ut eiendomskatten alle år. Vi legger resultatet inn i en ordliste med familienavnet som nøkkel. Dette gjør at vi er litt sikrere på at inntastingen og resultatet kommer på samme linje i tabellen vår.

@app.route('/oppgave1/avansert')
def vis_oppgave1_avansert():
  skjema = Eiendomsskatteskjema(request.args)
  if skjema.nybolig.data:
    skjema.boliger.append_entry()
  elif skjema.nysats.data:
    skjema.satser.append_entry()
  elif skjema.nullstill.data:
    skjema = Eiendomsskatteskjema()
  elif skjema.fyllinn.data:
    skjema = Eiendomsskatteskjema(oppgave1data)

  s = [sats.verdi.data for sats in skjema.satser if sats.validate(skjema)]
  utdata = {b.familie.data: eiendomsskatt_A(b.likningsverdi.data, s) for b in skjema.boliger if b.validate(skjema)}
  return render_template("oppgave1A.html",
                         skjema = skjema,
                         utdata = utdata)


#[BILDE]

#%%


##Oppgave 2

"""
David eier en tomt. Arealet av tomten er 600 m2. Reguleringsplanen for tomten har et krav som sier at han ikke kan bygge på mer enn 30 % av tomtens areal.
På tomten ønsker David å bygge
• en bolig som har en grunnflate med areal 140 m2
• en garasje med bredde 6 m og lengde 8 m
Gjør beregninger, og avgjør om det vil være mulig for David å bygge både huset og garasjen på tomten dersom han skal holde seg innenfor kravet i reguleringsplanen.
"""

#Denne oppgaven er ganske lik den forrige, så vi lager bare en enkel løsning. Vi lager først et skjema for tallene fra oppgaven. Dette er bare en mengde med flyttallsfelt og et inntastingsfelt. Vi gir alle feltene en standardverdi med argumentet <code>default</code>.

class Skjema2(Form):
  tomteareal = FloatField("Tomteareal",
                          [NumberRange(0)],
                          default=600)
  regulering = FloatField("Største utbyggingsgrad (%)",
                          [NumberRange(0)],
                          filters=[lambda x: x/100 if x else x],
                          default=3000)
  boligareal = FloatField("Boligareal",
                          [NumberRange(0)],
                          default=140)
  garasjebredde = FloatField("Garasjebredde",
                             [NumberRange(0)],
                             default=6)
  garasjelengde = FloatField("Garasjelengde",
                             [NumberRange(0)],
                             default=8)
  beregn = SubmitField("Beregn!")


#Vi kan nå lage en beregningsfunksjon som tar inn tallene fra oppgaven og returnerer mellomregningene og et endelig svar på oppgaven.

def beregning2(tomteareal, regulering, boligareal, garasjebredde, garasjelengde, **kwargs):
  byggeareal = regulering *tomteareal
  garasjeareal = garasjebredde*garasjelengde
  nødvendig_areal = boligareal + garasjeareal
  mulig = byggeareal > nødvendig_areal
  return {"byggeareal": byggeareal,
          "garasjeareal": garasjeareal,
          "nødvendig_areal": nødvendig_areal,
          "mulig": mulig}

#Vi registrerer visningsfunksjonen for denne oppgaven på samme måte som for oppgave 1. Vi bruker fortsatt <kbd>base.html</kbd> som mal. Siden skjemaet er "ferdigutfylt" vil <code>validate</code> bli sann dersom brukeren ikke har sendt inn data. For å ikke forulempe brukeren tester vi derfor om hun har sendt inn data ved å teste om <code>request.args</code> finnes samtidig som vi validerer.

@app.route('/oppgave2')
def vis2():
  skjema = Skjema2(request.args)
  if request.args and skjema.validate():
    utdata = beregning2(**skjema.data)
  else:
    utdata = []
  return render_template("base.html",
                         tittel="Oppgave 2",
                         skjema = skjema,
                         utdata = utdata)

#[BILDE]


#%%


##Oppgave 3

"""
[BILDE]
Ovenfor ser du grafen til en funksjon .
a) Sett opp et mulig uttrykk for f(x).
   Husk å forklare hvordan du tenker.
b) Bestem, hvis det er mulig, f(16), f(400), f(9/4) og f(-25).
Om du mener det ikke er mulig å bestemme én eller flere av verdiene, må du huske å argumentere for dette.
"""

###Enkel

#Vi begynner med å løse denne oppgaven enklest mulig, og lager et skjema hvor <i>x</i>- og <i>y</i>-feltene er lister med heltallsfelt. Siden det er fem tallpar i oppgaven, sier vi at det skal være minst fem elementer i disse listene. Vi legger også til en liste med nye elementer, vi lar denne listen starte med 4 tomme elementer. Siden oppgaven ber oss om å regne ut funksjonsverdien til brøker lar vi innput-feltet for nye verdier være tekst (<code>StringField</code>). Dette gjør at vi kan skrive inn brøker og bruke Sympy-funksjonen <code>sympify</code> til å konvertere teksten til et (Sympy-)tall.

class Skjema3(Form):
  X = FieldList(IntegerField(), min_entries=5)
  Y = FieldList(IntegerField(), min_entries=5)
  nye = FieldList(StringField(), min_entries=4)
  beregn = SubmitField("Beregn!")


#Vi lager så kode for å finne <i>f(x)</i> ved regresjonsanalyse. Vi begynner med en modellfunksjon, og lager så en funksjon som tar inn <i>x</i>- og <i>y</i>-verdier og en modellfunksjon og gjennomfører regresjonsanalysen med funksjonen <code>curve_fit</code> fra biblioteket scipy.optimize. Funksjonen returnerer parametrene og funksjonen.

#Vi antar at funksjonen er på formen <i>f(x) = ax<sup>b</sup></i>.

def potensmodell(x, a, b):
  return a*x**b

def beregn3(X, Y, modell = potensmodell):
  res = curve_fit(modell, X, Y)
  fun = lambda x: modell(x, *res[0])
  return {"par" : res[0],
          "fun" : fun}

#For å illustrere svaret lager vi en funksjon som tar inn funksjonen vi har funnet og dataene og tegner dem sammen. Resultatet blir HTML-koden for å tegne bildet. Denne funksjonen følger fremgangsmåten i Matplotlib-dokumentasjonen.

def tegn(fun, X, Y):
  #Setter opp x-verdiene
  xmin, xmax = np.min(X), np.max(X)
  t = np.linspace(xmin, xmax)
  #Setter opp tegnevinduet
  fig = Figure(figsize=(6, 3), tight_layout=True)
  ax = fig.subplots()
  #Tegner regresjonslinje og data
  ax.plot(t, fun(t), color="blue")
  ax.scatter(X, Y, color="orange")
  ax.grid()
  #Returnerer en img-tag
  buf = BytesIO()
  fig.savefig(buf, format="png")
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  return Markup(f"<img src='data:image/png;base64,{data}'>")

#Siden oppgaven ber oss om å regne ut nye funksjonsverdier lager vi en funksjon som gjør dette for oss. Siden vi risikerer at oppgavene ikke har løsninger må vi gjøre dette inne i en <code>try...except</code>-blokk. Vi tar inn den nye verdien som en tekst og forsøker (<i>try</i>) å konvertere teksten til et tall og regne ut funksjonsverdien. Vi noterer også om denne verdien er reell med attributtet <code>is_real</code>. Dersom utregningen feiler setter vi funksjonsverdien til <i>None</i>. Vi returnerer et talltrippel med verdi, funksjonsverdi og om løsningen er reell.

def evaluer(fun, v):
  try:
    res = fun(sympify(v))
    real = res.is_real
  except Exception:
    res = None
    real = None
  return v, res, real


#Vi lager en visningsfunksjon på samme måte som tidligere. Vi filtrerer vekk de tomme feltene i listene med koden <code>[x for x in skjema.X.data if x]</code>. Dersom vi har både <i>x</i>- og <i>y</i>-verdier gjør vi en regresjonsanalyse og bruker resultatet fra regresjonsanalysen til å tegne funksjonsgrafen og regne ut de nye funksjonsverdiene. Vi bruker fortsatt standardmalen <kbd>base.html</kbd> til å vise skjema og resultater på skjermen.

@app.route('/oppgave3')
def vis3():
  skjema = Skjema3(request.args)
  utdata = [skjema.data]
  X = [x for x in skjema.X.data if x]
  Y = [y for y in skjema.Y.data if y]
  N = [n for n in skjema.nye.data if n]
  if X and Y:
    res = beregn3(X, Y)
    utdata = [res]
    utdata.append(tegn(res['fun'], X, Y))
    utdata.append([evaluer(res['fun'], v) for v in N])
  else:
    utdata = None
  return render_template("base.html",
                         tittel="Oppgave 3",
                         skjema = skjema,
                         utdata = utdata)

#[BILDE]

#Vi leser av svaret [1, 0.5] dette betyr at funksjonen er 1*x**0.5 som er det samme som <math><msqrt><mi>x</mi></msqrt></math>.

#Vi ser at funksjonsverdien finnes for alle fire verdier. Vi ser samtidig at når <i>x = -25</i> blir løsningen kompleks. På 1P-nivå vil vi ikke regne med komplekse tall, og heller si at <i>f(-25)</i> ikke er definert.

#%%


###Avansert løsning: Input-tabell

#Vi har funnet en mulig funksjon, og er rimelig sikre på at det er det riktige. Men samtidig kunne dataene også passet til en logaritmefunksjon eller en polynomfunksjon. Som et eksempel på hvordan vi kan legge til flere regresjonsmodeller legger vi inn muligheten for å tilpasse dataene til en andregradsfunksjon på formen <i>f(x) = ax<sup>2</sup> + bx + c</i>. Samtidig ønsker vi å legge inn knapper for å legge til flere punkter, nullstille og å sette inn oppgavedataene slik som vi gjorde i oppgave 1.

#Vi legger inn et datafelt av typen <code>SelectField</code>, dette gir oss en nedtrekksmeny for å velge regresjonsmodell. Vi legger inn listen med valg med argumentet <code>choices</code>.

class Regresjonsskjema(Form):
  modell = SelectField(choices=['polynom', 'potens'], default='potens')
  X = FieldList(IntegerField(), min_entries=5)
  Y = FieldList(IntegerField(), min_entries=5)
  nye = FieldList(StringField(), min_entries=4)
  beregn = SubmitField("Beregn!")
  leggtil = SubmitField("Legg til rad")
  nullstill = SubmitField("Nulstill")
  oppgavedata = SubmitField("Oppgavedata")



#Vi lager en ny mal. Denne malen setter opp input-feltene som en tabell. Malen skriver også ut utdataene på en mer elegant måte.

#[oppgave3A.html]

#Vi legger til en andregradsmodellfunksjon.

def polynommodell(x, a, b, c):
  return a*x**2 + b*x + c

#Vi lager en ordliste med modellfunksjonene.

modell = {'polynom': polynommodell,
          'potens': potensmodell}

#Vi legger inn oppgavedataene som en inputdatastruktur.

oppgave3data = ImmutableMultiDict([('X-0', '4'), ('X-1', '25'), ('X-2', '49'), ('X-3', '81'), ('X-4', '100'), ('Y-0', '2'), ('Y-1', '5'), ('Y-2', '7'), ('Y-3', '9'), ('Y-4', '10'), ('nye-0', '16'), ('nye-1', '400'), ('nye-2', '9/4'), ('nye-3', '-25'), ('beregn', 'Beregn!')])

#Vi lager en funksjon som skriver ut den ferdige funksjonen. Vi definerer Sympy-symbolet <code>x</code> og bruker dette som et argument til funksjonen vi har funnet. Resultatet blir et symbolsk funksjonsuttrykk.

#Vi skriver ut dette funksjonsuttrykket på formatet MathML med Sympy-funksjonen <code>mathml</code>. MathML er et <i>markup</i> språk som ligner på HTML/XML som gjør at vi kan vise matematiske uttrykk i nettlesere. For å et korrekt HTML-element må vi sette MathML-blokken inni en <code>math</code>-blokk.

#For å få med venstresiden i funksjonen gir vi mathml-funksjonen argumentet <code>Eq(f(x), fun(x))</code>.

def funksjon_til_html(fun):
    f, x = Function("f"), Symbol("x")
    expr = mathml(Eq(f(x), fun(x)).evalf(2),
                  printer="presentation")
    return Markup("<math>" + expr + "</math>")

#Vi kan nå registere en visningsfunksjon som:
#* instansierer et skjemaobjekt med eventuelle data
#* bruker en <code>if</code>-blokk til å hånterere de alternative knappene.
#* henter ut lister med <i>x</i>-verdier, <i>y</i>-verdier og nye <i>x</i>-verdier.
#* dersom det er data finner vi funksjonen, tegner situasjonen og lager en HTML-versjon av funksjonen.
#* til slutt kaller funksjonen <kbd>render_template</kbd> med templaten <kbd>oppgave3A.html</kbd>.


@app.route('/oppgave3/avansert')
def vis_avansert3():
  print(request.args)
  skjema = Regresjonsskjema(request.args)
  if skjema.leggtil.data:
    skjema.X.append_entry()
    skjema.Y.append_entry()
  elif skjema.nullstill.data:
    skjema = Regresjonsskjema()
  elif skjema.oppgavedata.data:
    skjema = Regresjonsskjema(oppgave3data)

  X = [x for x in skjema.X.data if x]
  Y = [y for y in skjema.Y.data if y]
  N = [n for n in skjema.nye.data if n]

  if X and Y:
    ut = beregn3(X, Y, modell[skjema.modell.data])
    ut['tegning'] = (tegn(ut['fun'], X, Y))
    ut['funksjonsverdier'] = [evaluer(ut['fun'], v) for v in N]
    ut['uttrykk'] = funksjon_til_html(ut['fun'])
  else:
    ut = None

  return render_template("oppgave3A.html",
                         tittel="Oppgave 3",
                         skjema = skjema,
                         utdata = ut)

#[BILDE]


#%%Oppgave 4
"""
"""

#Vi løser denne oppgaven på samme måte som de fire foregående.

#Vi begynner med et skjema for inndataene.

class Skjema4(Form):
  x1 = FloatField("x1", [DataRequired()])
  y1 = FloatField("y1", [DataRequired()])
  x2 = FloatField("x2", [DataRequired()])
  y2 = FloatField("y2", [DataRequired()])
  etterspørsel = IntegerField("Etterspørsel (millioner fat)")
  beregn = SubmitField("Beregn!")

#Vi lager en funksjon som finner stigningstallet, en funksjon for litervolum og etterspørselen i liter.

def beregn4(x1, x2, y1, y2, etterspørsel, **kwargs):
  a = (y2 - y1)/(x2 - x1)
  fun = lambda x: a*x
  volum_fat = etterspørsel * 1e6
  volum_gallon = 24*volum_fat
  volum_liter = a*volum_gallon
  return {"stigningstall": a,
          "fun": fun,
          "volum": volum_liter}

#Vi registrerer en visningsfunksjon som henter inn data og returnerer svaret. Dersom det er data gjør vi beregningene, konverterer volumet til en tekst på standardform og tegner funksjonen sammen med inndataene. For å bruke tegnefunksjonen må vi gjøre våre <i>x</i>- og <i>y</i>-enkeltverdier om til to lister.

@app.route('/oppgave4/')
def vis4():
  skjema = Skjema4(request.args)
  if skjema.validate():
    utdata = beregn4(**skjema.data)
    utdata['standardform'] = f"{utdata['volum']:.2e}"
    d = skjema.data
    X, Y = [d['x1'], d['x2']], [d['y1'], d['y2']]
    utdata['tegning'] = tegn(utdata['fun'], X, Y)
  else:
    utdata = None
  return render_template("base.html",
                         tittel = "Oppgave 4",
                         skjema = skjema,
                         utdata = utdata)

#[BILDE]
