# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 19:54:18 2023

@author: magdalon
"""

#Eksamen 1P høst 2020: Oppgave 7 - webapp

#Denne oppgaven handler om å regne ut provisjon for videresalg av fisk. Vi velger å lage en webapp med den samme funksjonaliteten som regnearket vi er bedt om å lage.

#---more---

##Oppgavetekst
"""
En salgsavdeling i et firma kjøper fisk og selger den videre.
Prisen de kjøper fisken for, kaller vi kostpris, og prisen de selger den for, kaller vi salgspris.
Salgsavdelingen får provisjon av differansen mellom kostpris og salgspris.
Provisjonen er avhengig av hvor stor differansen mellom kostpris og salgspris er.
Se tabellen nedenfor.
[TABELL]
Salgsavdelingen fikk solgt et parti på 1000 kg fisk for 80 kroner per kilo. Kostprisen var 65 kroner per kilogram.
a) Vis at provisjonen for dette salget ble 1200 kroner.
b) Lag et regneark som vist nedenfor som firmaet kan bruke for å registrere provisjon til salgsavdelingen. I de grønne cellene skal du legge inn formler.
[BILDE]
For å motivere salgsavdelingen til å oppnå høyest mulig salgspris endres satsene for provisjon. Lav sats settes til 4 % og høy sats til 10 %.
c) Bruk regnearket du laget i oppgave b), til å bestemme samlet provisjon med de nye satsene.
"""

##Biblioteker og funksjoner

#Vi begynner med å importere funksjonene vi har tenkt å bruke. Vi lagrer all koden i filen <kbd>1PH20-7.py</kbd>.

from babel.numbers import format_percent, format_decimal
from flask import Flask, render_template, request
from markupsafe import Markup
from werkzeug.datastructures import ImmutableMultiDict
from wtforms import (Form, FieldList, StringField,
                     SubmitField, FormField, IntegerField,
                     FloatField, DecimalField)
from wtforms.validators import NumberRange

##Oppsett

#Vi setter opp appen og standardmalen.

###App

#Vi legger inn følgende kode for å definere appen vår.

app = Flask(__name__)

@app.route('/')
def vis():
    return "Dette er en testserver"

#Vi kan nå sette opp en server til webappen vår ved å åpne et Anaconda-vindu, navigere til arbeidsmappen vår og skrive inn:

#flask --app 1PH20-7 --debug run

###Mal

#Vi lager en enkel mal med plass til skjemaene våre på samme måte som tidligere [TODO]. Vi lagrer denne som <kbd>1Pv20_base.html</kbd> i mappen <kbd>templates</kbd>. Denne malen inneholder tre blokker vi vil endre. Alle undermaler som utvider denne malen kan legge inn tekst i <code>head</code>-blokken, som legger til topptekst, <code>title</code>-blokken, som legger til en sidetittel og <code>content</code>-blokken som legger til innhold.

#[1Pv20_base.html]

#Denne malen bruker stilarket <kbd>provisjonskalkulator.css</kbd> som vi lagrer i undermappen <kbd>static</kbd>.

#[provisjonskalkulator.css]


#%%


##Input

#Vi begynner med å lage input-delen av regnearket.

###Skjemaklasse

#Vi lager først en skjemaklasse med WTForms [TODO]. Denne klassen har to felt, et <code>FieldList</code>-felt og et innsendingsfelt. <code>FieldList</code> er ikke et felt, men en liste med felt. Vi setter listefelttypen til <code>FormField</code>. <code>FormField</code> gjør et skjema til et felt, dette gjør at vi kan sette inn underskjemaer.

#Skjemaet vi setter inn er definert med klassen <code>Selskapsskjema</code>. Dette skjemaet består av et tekstfelt (<code>StringField</code>), heltallsfelt (<code>IntegerField</code>) og to flyttallsfelt (<code>FloatField</code>). Tallfeltene får begrensingen <code>NumberRange(0)</code> som betyr at verdien må være større enn eller lik 0.

#Hver rad i skjemaet blir en ny oppføring i kunde-listen. Siden det er fem rader som er fylt ut i skjemaet, gjør vi plass til fem rader med argumentet <code>min_entries=5</code>.

class Selskapsskjema(Form):
    navn = StringField("Kunde")
    mengde = IntegerField("Antall kilogram", [NumberRange(0)])
    kostpris = FloatField("Kostpris per kilogram", [NumberRange(0)])
    salgspris = FloatField("Salgspris per kilogram", [NumberRange(0)])

class Provisjonsskjema(Form):
    kunder = FieldList(FormField(Selskapsskjema), min_entries=5)
    beregn = SubmitField("Beregn!")

if __name__ == '__main__':
    ####Skjema-objektet

    #Før vi går videre kan vi utforske <code>Provisjonsskjema</code>-klassen.

    #Vi simulerer imputdata med klassen ImmutableMultiDict fra biblioteket werkzeug.datastructures.

    test = ImmutableMultiDict([('kunder-0-navn', 'Sørfisk'), ('kunder-0-mengde', '2000'), ('kunder-0-kostpris', '80.60'), ('kunder-0-salgspris', '88.10'), ('kunder-1-navn', 'Nordfisk'), ('kunder-1-mengde', '500'), ('kunder-1-kostpris', '97.90'), ('kunder-1-salgspris', '115.70')])
    #Vi oppretter et provisjonsskjema-objekt med testadataene.
    skjema = Provisjonsskjema(test)
    print(skjema)
    #<__main__.Provisjonsskjema object at 0x000002571DC7C790>
    #Kundedataene sitter i <code>kunder</code>-attributtet.Vi kan skrive ut kundedataene med dette objektet sitt   <code>data</code>-attributt.
    print(skjema.kunder.data)
    #{'navn': 'Sørfisk', 'mengde': 2000, 'kostpris': 80.6, 'salgspris': 88.1} {'navn': 'Nordfisk', 'mengde':   500, 'kostpris': 97.9, 'salgspris': 115.7} {'navn': '', 'mengde': None, 'kostpris': None, 'salgspris': None} {'navn': '', 'mengde': None, 'kostpris': None, 'salgspris': None} {'navn': '', 'mengde': None, 'kostpris': None, 'salgspris': None}

    #Vi kan også hente ut enkelte underskjemaer.

    print(skjema.kunder[0].data)
    #{'navn': 'Sørfisk', 'mengde': 2000, 'kostpris': 80.6, 'salgspris': 88.1}
    #Dette blir en ordliste med feltene i underskjemaet.

    #Vi kan selvsagt også hente ut enkeltfelter.
    print(skjema.kunder[0].navn.data)
    #Sørfisk

    #Vi kan også generere html-kode for skjemaet og/eller inputfeltene.

    print(skjema.kunder)
    #<ul id="kunder"><li><label for="kunder-0">Kunder-0</label> <table id="kunder-0"><tr><th><label for="kunder-0-navn">Kunde</label></th><td><input id="kunder-0-navn" name="kunder-0-navn" type="text" value="Sørfisk"></td></tr><tr><th><label for="kunder-0-mengde">Antall kilogram</label></th><td><input id="kunder-0-mengde" name="kunder-0-mengde" type="text" value="2000"></td></tr><tr><th><label for="kunder-0-kostpris">Kostpris per kilogram</label></th><td><input id="kunder-0-kostpris" name="kunder-0-kostpris" type="text" value="80.60"></td></tr><tr><th><label for="kunder-0-salgspris">Salgspris per kilogram</label></th><td><input id="kunder-0-salgspris" name="kunder-0-salgspris" type="text" value="88.10"></td></tr></table></li><li><label for="kunder-1">Kunder-1</label> <table id="kunder-1"><tr><th><label for="kunder-1-navn">Kunde</label></th><td><input id="kunder-1-navn" name="kunder-1-navn" type="text" value="Nordfisk"></td></tr><tr><th><label for="kunder-1-mengde">Antall kilogram</label></th><td><input id="kunder-1-mengde" name="kunder-1-mengde" type="text" value="500"></td></tr><tr><th><label for="kunder-1-kostpris">Kostpris per kilogram</label></th><td><input id="kunder-1-kostpris" name="kunder-1-kostpris" type="text" value="97.90"></td></tr><tr><th><label for="kunder-1-salgspris">Salgspris per kilogram</label></th><td><input id="kunder-1-salgspris" name="kunder-1-salgspris" type="text" value="115.70"></td></tr></table></li><li><label for="kunder-2">Kunder-2</label> <table id="kunder-2"><tr><th><label for="kunder-2-navn">Kunde</label></th><td><input id="kunder-2-navn" name="kunder-2-navn" type="text" value=""></td></tr><tr><th><label for="kunder-2-mengde">Antall kilogram</label></th><td><input id="kunder-2-mengde" name="kunder-2-mengde" type="text" value=""></td></tr><tr><th><label for="kunder-2-kostpris">Kostpris per kilogram</label></th><td><input id="kunder-2-kostpris" name="kunder-2-kostpris" type="text" value=""></td></tr><tr><th><label for="kunder-2-salgspris">Salgspris per kilogram</label></th><td><input id="kunder-2-salgspris" name="kunder-2-salgspris" type="text" value=""></td></tr></table></li><li><label for="kunder-3">Kunder-3</label> <table id="kunder-3"><tr><th><label for="kunder-3-navn">Kunde</label></th><td><input id="kunder-3-navn" name="kunder-3-navn" type="text" value=""></td></tr><tr><th><label for="kunder-3-mengde">Antall kilogram</label></th><td><input id="kunder-3-mengde" name="kunder-3-mengde" type="text" value=""></td></tr><tr><th><label for="kunder-3-kostpris">Kostpris per kilogram</label></th><td><input id="kunder-3-kostpris" name="kunder-3-kostpris" type="text" value=""></td></tr><tr><th><label for="kunder-3-salgspris">Salgspris per kilogram</label></th><td><input id="kunder-3-salgspris" name="kunder-3-salgspris" type="text" value=""></td></tr></table></li><li><label for="kunder-4">Kunder-4</label> <table id="kunder-4"><tr><th><label for="kunder-4-navn">Kunde</label></th><td><input id="kunder-4-navn" name="kunder-4-navn" type="text" value=""></td></tr><tr><th><label for="kunder-4-mengde">Antall kilogram</label></th><td><input id="kunder-4-mengde" name="kunder-4-mengde" type="text" value=""></td></tr><tr><th><label for="kunder-4-kostpris">Kostpris per kilogram</label></th><td><input id="kunder-4-kostpris" name="kunder-4-kostpris" type="text" value=""></td></tr><tr><th><label for="kunder-4-salgspris">Salgspris per kilogram</label></th><td><input id="kunder-4-salgspris" name="kunder-4-salgspris" type="text" value=""></td></tr></table></li></ul>
    print(skjema.kunder[0])
#<table id="kunder-0"><tr><th><label for="kunder-0-navn">Kunde</label></th><td><input id="kunder-0-navn" name="kunder-0-navn" type="text" value="Sørfisk"></td></tr><tr><th><label for="kunder-0-mengde">Antall kilogram</label></th><td><input id="kunder-0-mengde" name="kunder-0-mengde" type="text" value="2000"></td></tr><tr><th><label for="kunder-0-kostpris">Kostpris per kilogram</label></th><td><input id="kunder-0-kostpris" name="kunder-0-kostpris" type="text" value="80.60"></td></tr><tr><th><label for="kunder-0-salgspris">Salgspris per kilogram</label></th><td><input id="kunder-0-salgspris" name="kunder-0-salgspris" type="text" value="88.10"></td></tr></table>

    print(skjema.kunder[0].navn)
#<input id="kunder-0-navn" name="kunder-0-navn" type="text" value="Sørfisk">

#Vi ser at input-elementene får en id som er satt sammen av skjemafeltnavnet, oppføringsnummeret og feltnavnet.

###Mal

#Vi bruker attributtene til skjemaobjektet til å lage en mal som viser skjemaet. Vi lager en for-løkke som skriver ut skjemaet rad for rad. Legg merke til at vi itererer over radnummer. Legg også merke til at vi skriver  <code>skjema.kunder|length</code> for å finne antall rader.
#I tillegg til skjemaet legger vi inn plass for å skrive ut en liste med utdata.
#Den første linjen <code>{% extends "1Pv20_base.html" %}</code> sier at malen utvider malen <kbd>1Pv20_base.html</kbd> vi laget tidligere. Vi setter inn tekst i blokkene <code>title</code> og <code>content</code>.

#[1Pv20_input.html]

###Visningsfunksjon

#Vi lager en visningsfunksjon som bruker eventuelle skjemadata fra <code>request.args</code> til å lage et skjemaobjekt som vi sender til <code>render_template</code>-funksjonen. Vi legger også til utdata, i dette tilfellet er det innholdet i <code>request.args</code> og <code>skjema.data</code>.

@app.route('/input')
def vis_input():
    skjema = Provisjonsskjema(request.args)
    utdata = [repr(request.args), skjema.data]
    return render_template("1Pv20_input.html", skjema=skjema, utdata=utdata)


#%%


##Output

#Vi går nå over til å gjøre de nødvendige beregningene for å svare på oppgaven.

###Beregningsfunksjon

#Vi begynner med å legge inn tallene fra oppgaveteksten.

GRENSE = 10/100
satser = {"lav" : 5/100,
          "høy" : 8/100}

#Vi kan nå lage en beregningsfunksjon. Denne tar inn mengde, kostpris og salgspris som obligatoriske argumenter. I tillegg har vi et frivillig argument satser som vi setter til satsene vi fikk oppgitt. Vi kan senere endre dette argumentet for å svare på deloppgave (c). I tillegg har vi argumentet <code>**kwargs</code>. Dette betyr at alle andre argumenter vi gir til funksjonen blir lagt til i ordlisten kwargs. Dette gjør at vi ikke får feilmeldinger når vi oppgir ekstra argumenter.
#Funksjonen returnerer en ordliste med verdier til de fire kolonnene i oppgaven. Dette gjør at det er lett å sette disse inn i HTML-malene våre.

def provisjon(mengde, kostpris, salgspris, satser = satser, **kwargs):
    prisdifferanse = salgspris - kostpris
    prosent = prisdifferanse/kostpris
    if prosent >= GRENSE:
        sats = satser['høy']
    else:
        sats = satser['lav']
    provisjon = sats*prisdifferanse*mengde
    return {"differanse": prisdifferanse,
            "prosent" : prosent,
            "sats" : sats,
            "provisjon" : provisjon}

###Visningsfunksjon
#Vi lager en ny visningsfunksjon. Den eneste forskjellen er at vi nå returnerer beregningene. Vi går gjennom inndata kunde for kunde, dersom mengde, kostpris og salgspris er riktig fyllt ut regner vi ut provisjonen og setter legger resultatet til utdata-listen. Dersom dette ikke er tilfelle legger vi til <code>None</code>. Vi gir provisjons-funksjonen argumentet <code>**kunde.data</code> Dette gjør at alle nøkkel-verdi-par i denne ordlisten blir navngitte argumenter til funksjonen. Til slutt bruker  utdatalisten til å regne ut summen av provisjonen og legger summen til utdatalisten.

@app.route('/output')
def vis_output():
    skjema = Provisjonsskjema(request.args)
    utdata = []
    for kunde in skjema.kunder:
        if kunde.validate(skjema):
            utdata.append(provisjon(**kunde.data) )
        else:
            utdata.append(None)
    total = sum([data['provisjon'] for data in utdata if data])
    utdata.append({'Sum': total})
    return render_template("1Pv20_input.html", skjema=skjema, utdata=utdata)


#%%


##Outputtabell

#Vi fortsetter med å endre output-formatet til en tabell.

###Mal

#Vi endrer malen slik at vi skriver ut outputdataene på samme rad som inputtdataene dersom de finnes. Dersom det ikke er output til en rad skriver vi ut fire tomme celler.
#Vi legger også til en rad nederst som viser summen. Siden de første 6 cellene skal være tomme setter vi inn en celle som er 6-celler lang med argumentet <code>colspan='6'</code>. Vi lagrer den nye malen som <kbd>1Pv20_tabell.html</kbd> i undermappen <kbd>templates</kbd>.

#[1Pv20_tabell.html]

###Visningsfunksjon

#Vi lager en ny visningsfunksjon som er tilnærmet lik den forrige. Den eneste forskjellen er at vi sender totalprovisjonen som et eget argument til malen.

@app.route('/tabell')
def vis_tabell():
    skjema = Provisjonsskjema(request.args)
    utdata = []
    for kunde in skjema.kunder:
        if kunde.validate(skjema):
            utdata.append(provisjon(**kunde.data) )
        else:
            utdata.append(None),
    total = sum([data['provisjon'] for data in utdata if data])
    return render_template("1Pv20_tabell.html", skjema=skjema, utdata=utdata, total=total)

#Vi kan nå svare på oppgave 7b.

#%%


##Variable satser

#Vi kan legge inn felter for verdiene til provisjonssatsene.

###Skjemaklasse

#Vi begynner med å lage en ny skjemaklasse. Siden alle firmadata skal være like trenger vi bare å lage en ny hovedskjema-klasse. Vi velger å la de to nye feltene være heltallsfelter med standardverdier (<code>default</code>). Hvis vi ønsker finkontroll over provisjonssatsene kan vi endre felttypene til <code>FloatField</code>.

class Variabeltskjema(Form):
    lav = IntegerField('Lav sats', [NumberRange(0)], default = 5)
    høy = IntegerField('Høy sats', [NumberRange(0)], default = 8)
    kunder = FieldList(FormField(Selskapsskjema), min_entries=5)
    beregn = SubmitField("Beregn!")

###Mal

#Vi legger de to nye feltene i en tabell på toppen av siden. Vi lagrer den nye malen som <kbd>1Pv20_variabel.html</kbd> i undermappen <kbd>templates</kbd>.

#[1Pv20_variabel.html]

###Visningsfunksjon

#Vi lager en ny visningsfunksjon som henter ut satsene fra skjemaet og sender dem som et ekstra argument til <code>provisjon</code>.

@app.route('/variabel')
def vis_variabel():
    skjema = Variabeltskjema(request.args)
    satser = {"lav": skjema.lav.data/100,
              "høy": skjema.høy.data/100}
    utdata = []
    for kunde in skjema.kunder:
        if kunde.validate(skjema):
            utdata.append(provisjon(**kunde.data, satser = satser) )
        else:
            utdata.append(None)

    total = sum([data['provisjon'] for data in utdata if data])
    return render_template("1Pv20_variabel.html", skjema=skjema, utdata = utdata, total = total)

#Vi kan nå svare på oppgave 7c


#%%


##Legg til/fjern kolonner

#Selv om vi har svart på oppgaven kan vi fortsatt gjøre forbedringer. Det første vi vil gjøre er å legge inn muligheten til å legge inn eller ta bort rader fra skjemaet.


###Skjema

###Vi lager et nytt hovedskjema med de to nye knappene <code>leggtil</code> og <code>fjern</code>.

class MultiradSkjema(Form):
    lav = IntegerField('Lav sats', [NumberRange(0)], default = 5)
    høy = IntegerField('Høy sats', [NumberRange(0)], default = 8)
    kunder = FieldList(FormField(Selskapsskjema), min_entries=5)
    beregn = SubmitField("Beregn!")
    leggtil = SubmitField("Legg til rad")
    fjern = SubmitField("Fjern rad")


###Mal

#Vi skriver om malen slik at alle eventuelle knapper i skjemaet blir skrevet ut nederst på siden med en for-blokk. Vi lagrer den nye malen som <kbd>1Pv20_multirad.html</kbd> i undermappen <kbd>templates</kbd>.

#[1Pv20_multirad.html]


###Visningsfunksjon

#Vi legger til en if-elif-blokk som tester om noen av de nye knappene har blitt trykket. Dersom dette er tilfellet vil vi enten legge til en rad i kundefeltet med <code>append_entry</code>-metoden eller ta vekk den nederste raden med <code>pop_entry</code>-metoden. Legg merke til at dette virker bare for ekstra rader. Hvis vi vil ta vekk noen av de opprinnelige 5 må vi gjøre det litt mer avansert.

@app.route('/multirad')
def vis_multirad():
    skjema = MultiradSkjema(request.args)

    if skjema.leggtil.data:
        skjema.kunder.append_entry()
    elif skjema.fjern.data:
        skjema.kunder.pop_entry()

    satser = {"lav": skjema.lav.data/100,
              "høy": skjema.høy.data/100}

    utdata = []
    for kunde in skjema.kunder:
        if kunde.validate(skjema):
            utdata.append(provisjon(**kunde.data, satser = satser) )
        else:
            utdata.append(None)

    total = sum([data['provisjon'] for data in utdata if data])
    return render_template("1Pv20_multirad.html", skjema=skjema, utdata = utdata, total = total)


#%%


##Formater celler

#Det neste vi kan gjøre er å endre på formateringen til tabellen.

###Filtre

#Vi begynner med å legge inn filtre som viser tall som prosent eller kroner. Begge filtrene bruker funksjoner fra biblioteket <code>babel.numbers</code>. Dette er et bibliotek som hjelper oss med å skrive ut tallene i riktig tallformat, denne gangen norsk.

#Filteret <code>pst</code> viser tall som prosent. Vi bruker funksjonen <code>format_percent</code> til å formatere tallet. Argumentet <code>format=u'0.0%'</code> gir oss en desimal og prosenttegnet, mens argumentet <code>locale='nb'</code> gjør at vi får komma som desimalskilletegn og mellomrom som tusenskilletegn.

@app.template_filter("pst")
def filter_pst(x): #OBS
    return format_percent(x, format=u'0.0%', locale='nb')

#Valuttafilteret er litt mer komplisert. Dette skriver et vensrejustert <i>kr</i> foran verdien med <code><span style='float:left'>kr&nbsp;</span></code>. Deretter blir verdien skrevet ut høyrejustert med en <code>span</code>-tagg med <code>style:'float:right'</code>. Vi bruker babel.numbers-funksjonen <code>format_decimal</code> med argumentene <code>format='0.00'</code> og <code>locale='nb'</code> til å få to siffer etter desimalskilletegnet og komma som desimalskilletegn.

@app.template_filter("nok")
def filter_nok(verdi):
    return Markup(f"<span style='float:left'>kr&nbsp;</span><span style='float:right'>{format_decimal(verdi, format='0.00', locale='nb')}</span>")

###Mal

#Vi lager så en mal som bruker disse filtrene til å vise tallene på riktig måte. Vi legger også til CSS-kode og HTML-code som gjør at innputrutene blir grønne og at tekstjusteringen blir likere oppgaven.
#For å få grønne tabellceller legger vi til koden <code>.beregning { background: #7cbf9d }</code> - inne i en <code>style</code>-blokk inne i <code>head</code>-blokken. <code>head</code>-blokken la vi inn i toppteksten i malen <kbd>1Pv20_base.html</kbd>, så denne blokken kommer i toppteksten til nettsiden vår. Vi lar output-tabellcellene få det ekstra argumentet <code>class=beregning</code> slik at nettleseren vet at disse cellene skal vises med <kbd>beregning</kbd>-stilen.
#Vi lagrer den nye malen som <kbd>1Pv20_tabell.html</kbd> i undermappen <kbd>templates</kbd>.

#[1Pv20_formatert.html]


###Visningsfunksjon

#Vi lager en ny visningsfunksjon med den nye malen.

@app.route('/formatert')
def vis_formatert():
    skjema = MultiradSkjema(request.args)

    if skjema.leggtil.data:
        skjema.kunder.append_entry()
    elif skjema.fjern.data:
        skjema.kunder.pop_entry()

    satser = {"lav": skjema.lav.data/100,
              "høy": skjema.høy.data/100}

    utdata = []
    for kunde in skjema.kunder:
        if kunde.validate(skjema):
            utdata.append(provisjon(**kunde.data, satser=satser))
        else:
            utdata.append(None)
    total = sum([data['provisjon'] for data in utdata if data])
    return render_template("1Pv20_formatert.html", skjema=skjema, utdata = utdata, total = total)


##Komma som desimalskilletegn

#Den vanskeligste formateringen vi skal gjøre er å endre desimalskilletegnet i <code>input</code>-elementene til komma (<kbd>,</kbd>).

###Skjema

#Vi gjør endringer i selskapsskjemaet vårt. Vi bruker først <code>class Meta: locales = ['nb']</code> til å sette skjemalokaliseringen til norsk bokmål.
#Vi endrer så felttypen til mengde- og kostprisfeltene til <code>DecimalField</code>. Dette er et felt for desimaltall. Vi gir konstruktørene de ekstra argumentet <code>use_locale=True</code> som sier at vi skal gjøre lokale tilpasninger. Vi gir også argumentet <code>filters= [lambda x: float(x) if x else x]</code>. Dette legger inn en liste med filtre, i dette tilfellet er det et filter som regner om desimaltallet til et flyttal. Vi gjør denne omregningen fordi resten av programmet vårt regner med flyttall. Flyttall(<code>float</code>) og desimaltall(<code>decimal.Decimal</code>) viser det samme, men siden det er to forskjellige datatyper må vi konvertere.

class EndeligSelskapsskjema(Form):
    class Meta:
        locales = ['nb']
    navn = StringField("Kunde")
    mengde = IntegerField("Antall kilogram", [NumberRange(0)])
    kostpris = DecimalField("Kostpris per kilogram", [NumberRange(0)], filters= [lambda x: float(x) if x else x], use_locale=True)
    salgspris = DecimalField("Salgspris per kilogram", [NumberRange(0)], filters= [lambda x: float(x) if x else x], use_locale=True)

class EndeligProvisjonsskjema(Form):
    lav = IntegerField('Lav sats', [NumberRange(0)], default = 5)
    høy = IntegerField('Høy sats', [NumberRange(0)], default = 8)
    kunder = FieldList(FormField(EndeligSelskapsskjema), min_entries=5)
    beregn = SubmitField("Beregn!")
    leggtil = SubmitField("Legg til rad")
    fjern = SubmitField("Fjern rad")


###Visningsfunksjon

#Vi endrer visningsfunksjonen vår til å bruke den nye skjemaklassen.

@app.route('/avansert')
def vis_avansert():
    skjema = EndeligProvisjonsskjema(request.args)
    satser = {"lav": skjema.lav.data/100,
              "høy": skjema.høy.data/100}
    if skjema.leggtil.data:
        skjema.kunder.append_entry()
    elif skjema.fjern.data:
        skjema.kunder.pop_entry()
    utdata = []
    for kunde in skjema.kunder:
        if kunde.validate(skjema):
            utdata.append(provisjon(**kunde.data, satser = satser) )
        else:
            utdata.append(None)

    total = sum([data['provisjon'] for data in utdata if data])
    return render_template("1Pv20_formatert.html", skjema=skjema, utdata=utdata, total=total)


##Eksempeldata

#Til slutt legger vi til knapper som automatisk legger inn tallene fra oppgaven. I tillegg legger vi til en knapp som nullstiller skjemaet.

###Skjema

#Vi trenger nå bare å legge til tre nye <code>SubmitField</code>-objekter; <code>nulstill</code>, <code>xa</code> og <code>xb</code>.

class UtfyltProvisjonsskjema(Form):
  lav = IntegerField('Lav sats', [NumberRange(0)], default = 5)
  høy = IntegerField('Høy sats', [NumberRange(0)], default = 8)
  kunder = FieldList(FormField(EndeligSelskapsskjema), min_entries=5)
  beregn = SubmitField("Beregn!")
  leggtil = SubmitField("Legg til rad")
  fjern = SubmitField("Fjern rad")
  nulstill = SubmitField("Nullstill")
  xa = SubmitField("Oppgave 7b")
  xb = SubmitField("Oppgave 7c")

#Siden malen vår automatisk legger til inputelementer for <code>SubmitField</code>-objekter trenger vi ikke å lage en ny mal.

##Visningsfunksjon

#Vi legger inn to ImmutableMultiDict-objekter som reprereserer oppgavedataene.

data_a = ImmutableMultiDict([('lav', '5'), ('høy', '8'), ('kunder-0-navn', 'Sørfisk'), ('kunder-0-mengde', '2000'), ('kunder-0-kostpris', '80,60'), ('kunder-0-salgspris', '88,10'), ('kunder-1-navn', 'Nordfisk'), ('kunder-1-mengde', '500'), ('kunder-1-kostpris', '97,90'), ('kunder-1-salgspris', '115,70'), ('kunder-2-navn', 'Østfisk'), ('kunder-2-mengde', '3400'), ('kunder-2-kostpris', '89,00'), ('kunder-2-salgspris', '95,50'), ('kunder-3-navn', 'Vestfisk'), ('kunder-3-mengde', '1000'), ('kunder-3-kostpris', '65,00'), ('kunder-3-salgspris', '80,00'), ('kunder-4-navn', 'Havfisk'), ('kunder-4-mengde', '1200'), ('kunder-4-kostpris', '105,00'), ('kunder-4-salgspris', '115,50'), ('beregn', 'Beregn!')])

data_b = ImmutableMultiDict([('lav', '4'), ('høy', '10'), ('kunder-0-navn', 'Sørfisk'), ('kunder-0-mengde', '2000'), ('kunder-0-kostpris', '80,60'), ('kunder-0-salgspris', '88,10'), ('kunder-1-navn', 'Nordfisk'), ('kunder-1-mengde', '500'), ('kunder-1-kostpris', '97,90'), ('kunder-1-salgspris', '115,70'), ('kunder-2-navn', 'Østfisk'), ('kunder-2-mengde', '3400'), ('kunder-2-kostpris', '89,00'), ('kunder-2-salgspris', '95,50'), ('kunder-3-navn', 'Vestfisk'), ('kunder-3-mengde', '1000'), ('kunder-3-kostpris', '65,00'), ('kunder-3-salgspris', '80,00'), ('kunder-4-navn', 'Havfisk'), ('kunder-4-mengde', '1200'), ('kunder-4-kostpris', '105,00'), ('kunder-4-salgspris', '115,50'), ('beregn', 'Beregn!')])

#Vi kan nå registrere en visningsfunksjon. Hvis <i>Nullstill</i> er trykket erstatter vi det utfylte skjemaet med et tomt skjema. Hvis <i>Oppgave 7a</i> eller <i>Oppgave 7b</i> er trykket blir skjemaet erstattet av et skjema med de forhåndsutfylte dataene.

@app.route('/utfylt')
def vis_utfylt():
  skjema = UtfyltProvisjonsskjema(request.args)
  if skjema.leggtil.data:
    skjema.kunder.append_entry()
  elif skjema.fjern.data:
    skjema.kunder.pop_entry()
  elif skjema.nulstill.data:
    skjema=UtfyltProvisjonsskjema()
  elif skjema.xa.data:
    skjema = UtfyltProvisjonsskjema(formdata=data_a)
  elif skjema.xb.data:
    skjema = UtfyltProvisjonsskjema(formdata=data_b)

  satser = {"lav": skjema.lav.data/100,
            "høy": skjema.høy.data/100}
  utdata = []
  for kunde in skjema.kunder:
    if kunde.validate(skjema):
      utdata.append(provisjon(**kunde.data, satser = satser) )
    else:
      utdata.append(None)

  total = sum([data['provisjon'] for data in utdata if data])
  return render_template("1Pv20_avansertskjema.html", skjema=skjema, utdata=utdata, total=total)
