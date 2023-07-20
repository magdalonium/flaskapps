# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:30:05 2023

@author: magopda
"""

#Eksamen 1P vår 2022: Oppgave 7 - webapp

#Denne oppgaven handler om å svare på forskjellige påstander om løping og Cooper-testen.  Vi kan tenke oss at vi i stedet for skal lage et lite program som kan svare på de samme påstandene for mange løpeturer. Denne gangen skal vi sette opp en server som kjører en webapp som svarer på oppgaven. Vi gjør dette ved hjelp av Python-biblioteket [Flask].


#---more---

##Oppgavetekst

"""
Sofie løper på en tredemølle. Etter tre minutter står det i displayet at
hun har
• brukt 32 kilokalorier (kcal) energi
• løpt 0,38 km
Sofie gjør seg noen tanker mens hun løper:

I Cooper-testen løper man i 12 minutter.
Jeg har løpt 380 m på 3 minutter. Hvor langt kommer jeg på 12 minutter?

Hvor mange kilokalorier bruker jeg per kilometer jeg løper?

Hvor mange kilokalorier bruker jeg dersom jeg løper i én time?

Jeg vil øke farten. Jeg har hørt at jenter må løpe minst 2200 m på 12 minutter for å få en god karakter på Cooper-testen.
Hvilken fart må jeg velge?

Etter løpingen spiser Sofie en melkesjokolade som veier 60 g. På etiketten står det at 100 g sjokolade inneholder 550 kcal. Sofie spør seg selv:

Er det flere kalorier i sjokoladen enn jeg brukte da jeg løp på tredemøllen?

Gjør beregninger og vurderinger, og lag en oversikt som gir Sofie mest mulig informasjon om sammenhengene hun er opptatt av.
"""

##Struktur

#Vi lager webappen i tre lag:
#*et <b>modell-lag</b> som gjør utregningen
#*et <b>kontroll-lag</b> som tar i mot beskjeder fra brukeren og sender dem til modellen og sender resultatene det andre veien
#*et <b>visningslag-lag</b> som viser resultatene til brukeren og sender brukerdata til kontrollaget.

##Biblioteker og funksjoner

#Vi begynner med å importere bibliotekene og funksjonene vi har tenkt å bruke.

from time import strftime, gmtime
from datetime import datetime

from flask import Flask, request, render_template
from wtforms import Form, DateTimeField, FloatField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

##Modell-lag

#Vi begynner med å legge inn verdiene fra oppgaveteksten. Vi velger å jobbe med kilometer og sekunder som enheter.

cooper_tid = 12*60
cooper_mål = 2.2
energitetthet_sjokolade = 550/100
vekt_sjokolade = 60
energi_sjokolade = energitetthet_sjokolade*vekt_sjokolade

#Vi lager en funksjon som svarer på påstandene i oppgaven. Når vi skal regne ut tempo (minutter/km) regner vi først ut sekunder/km før vi regner om til minutter og formaterer som minutter:sekunder med funksjonene gmtime og strftime fra biblioteket time.

def analyser(distanse = 0.38, sekunder = 180, energi = 32, **kwargs):
    påstander = {}

    #utledede data
    desimaltimer = sekunder/3600
    hastighet = distanse/desimaltimer
    tempo = sekunder/distanse

    påstander["tempo"] = strftime("%M:%S", gmtime(sekunder/distanse))
    påstander["hastighet"] = hastighet
    påstander["cooper_distanse"] = cooper_tid/tempo

    påstander["energi_per_km"] = energi/distanse

    påstander["energi_per_time"] = energi/desimaltimer

    påstander["cooper_tempo"] = strftime("%M:%S", gmtime(cooper_tid/cooper_mål))
    påstander["cooper_hastighet"] = 3600*cooper_mål/cooper_tid

    påstander["kalorioverskudd"] = energi_sjokolade > energi

    return påstander


##Presentasjons- og kontrollag

#Vi lager først selve app-objektet.

app = Flask(__name__)

###Skjema

#Vi lager en skjemaklasse. Skjemaet får fire datafelter: distanse (float), tid (datetime), energi(integer) og beregn(submit). Disse får argumentene etikett og en eventuell liste med validatorer (krav). InputRequired sier at feltet ikke kan være tomt, og NumberRange(0) sier at verdien må være større enn 0.
#Argumentet <code>format="%M:%S"</code> til DateTimeField-konstruktøren sier at tiden må skrives inn på formatet minutter:sekunder. Hvis vi vil at appen vår skal håndtere løpeturer på mer enn en time må vi endre dette argumentet til <code>format="%H:%M:%S"</code>.

class Løpeskjema(Form):
    distanse = FloatField("Distanse (km)", [InputRequired(), NumberRange(0)])
    tid = DateTimeField("tid (mm:ss)", [InputRequired()], format="%M:%S")
    energi = IntegerField("Energi (kCal)", [InputRequired(), NumberRange(0)])
    beregn = SubmitField("Beregn!")

###Mal

#Vi lagrer så en mal <kbd>1PH22-7.html</kbd> i undermappen <kbd>templates</kbd> som viser input og output. Denne består av enkel HTML-kode uten CSS-stiler. Koden i output-delen for å håndtere skjema er hentet fra [flask10].

#I analyse-delen skriver vi ut verdiene i påstander.objektet. For noen av verdiene bruker vi filteret <code>round</code> til å runde av. <code>round</code> runder av til nærmeste hele tall, mens <code>round(2)</code> runder av til nærmeste hundredel.

#[1PH22-7]

###Visningsfunksjon

#Vi lager og registrerer en visningsfunksjon. Denne henter argumentene fra forespørselen og setter dem inn i skjemaet med Løpeskjema(request.args). Dersom skjemaet er riktig fyllt ut gjør vi beregninger: Vi regner først tiden om fra datetime til sekunder, før vi sender distanse, sekunder og energi til analyser-funksjonen.

#Til slutt returnerer vi resulatet av render_template hvor vi har gitt malfilen og de to objektene våre (skjema og påstander) som argumenter.

@app.route("/løsning")
def vis_løsning(): #OBS
    skjema = Løpeskjema(request.args)
    if skjema.validate():
        sekunder = (skjema.tid.data - datetime(1900, 1, 1)).total_seconds()
        påstander = analyser(skjema.distanse.data, sekunder, skjema.energi.data)
    else:
        påstander = None
    return render_template("1PH22-7.html",  skjema=skjema, påstander=påstander)

##Testserver

#Vi kan kjøre en testserver for appen vår ved å åpne et Anaconda/Python-vindu, navigere til mappen hvor appen er lagret og skrive inn:
#flask --app 1PH22-7 --debug run

#BILDE

##Ferdig app

#BILDER
