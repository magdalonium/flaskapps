# -*- coding: utf-8 -*-
#Eksempeleksamen 1P høst 2021: Oppgave 7 - webapp

#Denne oppgaven handler om å lage et enkelt fakturasystem for takeaway. Vi skal denne gangen lage et enkelt webgrensesnitt.

#---more---
##Innhold


##Oppgavetekst

"""
«Lunsj på nett» er et firma som lager og leverer ferdige lunsjretter.
Kundene kan velge mellom tre retter:
* Dagens pasta koster 100 kroner.
* Dagens suppe koster 80 kroner.
* Dagens bagett koster 110 kroner.
«Lunsj på nett» gir 10 % rabatt til kunder som bestiller flere enn fire lunsjretter.
Levering koster 70 kroner for avstander som er kortere enn 8 km. For lengre avstander er prisen 150 kroner.
Lag et regneark som vist nedenfor. «Lunsj på nett» skal bruke regnearket for å registrere en bestilling.
Når bestillingen er registrert, skal regnearket beregne hvor mye kunden skal betale.
I de hvite cellene skal «Lunsj på nett» registrere opplysninger når de tar imot en bestilling. I de grønne cellene skal du lage formler.
[BILDE]
"""

##Biblioteker og funksjoner

#Vi begynner med å importere funksjonene vi har tenkt å bruke. Vi legger all koden inn i filen <kbd>1PH21-7.py</kbd>.

from babel.numbers import format_decimal
from flask import Flask, render_template, request
from markupsafe import Markup
from wtforms import Form, IntegerField, FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

##Modell-lag

#Vi fortsetter med modell laget som skal gjøre utregningene. Vi legger tallene fra oppgaven inn som konstanter.

RABATTSATS = 0.1
RABATTANTALL = 4
KORTLEVERING = 70
LANGLEVERING = 150
GRENSEAVSTAND = 8
PASTAPRIS = 100
SUPPEPRIS = 80
BAGETTPRIS = 110

#Vi lager så en funksjon som tar inn argumentene fra de tomme rutene og returnerer innholdet i de grønne rutene. Siden det er flere grønne ruter returnerer denne funksjonen en ordliste med alle resultatene.

def beregn(kunde, pasta, suppe, bagett, avstand):
    pastatotal = pasta*PASTAPRIS
    suppetotal = suppe*SUPPEPRIS
    bagettotal = bagett*BAGETTPRIS
    antall = pasta + suppe + bagett
    subtotal = pastatotal + suppetotal + bagettotal

    if antall > RABATTANTALL:
        rabatt = RABATTSATS*subtotal
    else:
        rabatt = 0

    if avstand < GRENSEAVSTAND:
        levering = KORTLEVERING
    else:
        levering = LANGLEVERING

    total = subtotal - rabatt + levering

    return {"pastatotal": pastatotal,
            "suppetotal": suppetotal,
            "bagettotal": bagettotal,
            "antall": antall,
            "subtotal": subtotal,
            "rabatt": rabatt,
            "levering": levering,
            "total": total}


##Visningslag


#Vi lagrer den enkle malen <kbd>1PH21-7basis.html</kbd> i undermappen <kbd>templates</kbd>. I input-koden bruker vi skjemakoden fra [flask10]. For uttataene bruker vi en if-blokk og en for-blokk til å skrive ut eventuelle utdata.

#[1PH21-7basis.html]

##Kontrollag

#Vi oppretter først appen.

app = Flask(__name__)

#Vi lager så en skjemaklasse med WTforms. For å få til dette lar vi skjemaet arve fra Form-klassen.

#Skjemaklassen vår består av tekstfelt, heltallsfelt, flyttallsfelt og innsendingsfelt. Vi gir noen begrensninger på noen av datafeltene. Vi gir også noen av datafeltene standardverdien 0 med <code>default=0</code>. Dette gjør at feltet vil bli være forhåndsutfylt med 0 i nettleseren og at dersom det ikke er fylt inn vil skjemadataverdien være 0.

class Bestillingsskjema(Form):
    kunde = StringField("Kunde", [DataRequired(), Length(3)])
    pasta = IntegerField("Pasta", [NumberRange(0)], default=0)
    suppe = IntegerField("Suppe", [NumberRange(0)], default=0)
    bagett = IntegerField("Bagett", [NumberRange(0)], default=0)
    avstand = FloatField("Avstand", [NumberRange(0)], default=0)
    bestill = SubmitField("Send bestilling")

#Vi registrerer en visningsfunksjon. Denne behandler skjemaet, utfører beregninger på skjemadataene og sender skjema og resultater til <code>render_template</code>-funksjonen sammen med malfilen.

@app.route('/basis')
def vis_basis():
    skjema = Bestillingsskjema(request.args)
    if skjema.validate():
        output = beregn(skjema.kunde.data,
                        skjema.pasta.data,
                        skjema.suppe.data,
                        skjema.bagett.data,
                        skjema.avstand.data)
    else:
        output = None
    return render_template("1PH21-7basis.html", skjema = skjema, output = output)


##Teste webapp

#Vi kan kjøre en testserver for appen vår ved å åpne et Anaconda/Python-vindu, navigere til mappen hvor appen er lagret og skrive inn:
#flask --app 1PH21-7 --debug run

#BILDE

##Avansert grensesnitt

#Vi kan bruke HTML-tabeller til å kopiere regnearket i oppgaveteksten nøyaktig.


###Visningslag

####Mal

#Vi lagrer malen <kbd>1PH21-7avansert.html<kbd> i mappen <kbd>templates</kbd>.
#Malen begynner med en <code>style</code>-blokk som styrer CSS-koden for tabellen. Deretter kommer selve tabellen. Vi styrer plasseringen av tabellcellene med attributtet <code>colspan</code>.

#Vi setter inn skjemafelt, utregninger og konstanter som variabler. For å formatere kroneverdiet lager vi bruker vi filteret <code>NOK</code> som vi skal lage senere. Vi bruker på samme måte filteret <code>pst</code> til å formatere prosenter.

#[1PH21-7avansert.html]

####Filtre

#Vi lager først prosentfilteret. Dette tar inn en verdi og returnerer en høyrerjustert tekst med <code><span style='float:right'></code>-taggen og formaterer teksten som et prosenttal uten desimaler. Vi gir tilslutt denne teksten som et argument til markupsafe-funksjonen <code>Markup</code>. Dette gjør at vi kan sette HTML-kode inn i en mal.


@app.template_filter("pst")
def filter_pct(verdi):
    return Markup(f"<span style='float:right'>{verdi:.0%}</span>")

#Valuttafilteret er litt mer komplisert. Dette skriver et vensrejustert <i>kr</i> foran verdien med <code><span style='float:left'>kr&nbsp;</span></code>. Deretter blir verdien skrevet ut høyrejustert med en <code>span</code>-tagg med <code>style:'float:right'</code>. Vi bruker babel.numbers-funksjonen <code>format_decimal</code> til å skrive desimalskilletegnet som komma.

@app.template_filter("nok")
def filter_nok(verdi):
    return Markup(f"<span style='float:left'>kr&nbsp;</span><span style='float:right'>{format_decimal(verdi, format = '0.00', locale='no')}</span>")


###Visningsfunksjon

#Før vi lager visningsfunksjonen lager vi en ordliste med konstantene vi har brukt.

konstanter = {
    'RABATTSATS' : RABATTSATS,
    'RABATTANTALL' : RABATTANTALL,
    'KORTLEVERING' : KORTLEVERING,
    'LANGLEVERING' : LANGLEVERING,
    'GRENSEAVSTAND' : GRENSEAVSTAND,
    'PASTAPRIS' : PASTAPRIS,
    'SUPPEPRIS' : SUPPEPRIS,
    'BAGETTPRIS' : BAGETTPRIS,
}

#Til slutt lager vi en ny visningsfunsksjon. Den eneste forskjellen fra den forrige funksjonen er argumentene til <code>render_template</code>. Siden output og konstanter er ordlister kan vi skrive **output og **konstanter. Dette betyr at alle (nøkkel, verdi)-par i ordlisten blir gitt som argumenter. Dette gjør at malfilen blir lettere å lese, siden vi kan skrive <code>total</code> i stedet for <code>resultat.total</code> og <code>RABATTSATS</code> i stedet for <code>konstanter.RABATTSATS</code>.

@app.route('/avansert')
def vis_avansert():
    skjema = Bestillingsskjema(request.args)
    print([(felt.name, felt.data) for felt in skjema])
    skjema.validate()
    output = beregn(skjema.kunde.data,
                    skjema.pasta.data,
                    skjema.suppe.data,
                    skjema.bagett.data,
                    skjema.avstand.data)
    return render_template("1PH21-7avansert.html",
                           skjema = skjema,
                           **output,
                           **konstanter)

#Bilde
