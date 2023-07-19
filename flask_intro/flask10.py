# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."


from wtforms import Form, StringField

class EnkeltSkjema(Form):
    innhold = StringField('Innhold')


from flask import request, render_template

@app.route('/enkeltskjema')
def vis_enkeltskjema():
    skjema = EnkeltSkjema(request.args)
    beskjed = skjema.innhold.data
    return render_template('enkeltskjema.html', beskjed=beskjed, skjema=skjema)


from wtforms.validators import InputRequired, Length

class ValidertSkjema(Form):
    innhold = StringField('Innhold', [InputRequired(), Length(5, 10)])


@app.route('/validertskjema')
def vis_validertskjema():
    skjema = ValidertSkjema(request.args)
    if skjema.validate():
        beskjed = "Godkjent"
    else:
        beskjed = skjema.errors
    return render_template('validertskjema.html', beskjed=beskjed, skjema=skjema)


from wtforms import SubmitField

class AutomatiskSkjema(Form):
    innhold = StringField('content', [InputRequired(), Length(5, 10)])
    sendinn = SubmitField('Send inn')


@app.route('/automatiskskjema')
def vis_automatiskskjema():
    skjema = AutomatiskSkjema(request.args)
    beskjed = [skjema.validate(), skjema.innhold.data]
    return render_template('automatiskskjema.html', beskjed=beskjed, skjema=skjema)


from wtforms import BooleanField, DateField, DateTimeField, FloatField, IntegerField, RadioField, SelectField, SubmitField

class FeltTest(Form):
    boolean = BooleanField()
    date = DateField()
    datetime = DateTimeField()
    floatf = FloatField()
    integer = IntegerField()
    radio = RadioField(choices=["Rød", "Hvit",  "blå"])
    select = SelectField(choices= [(1, "Ole"), (2, "Dole"), (3, "Doffen")])
    string = StringField()
    submit = SubmitField()


@app.route('/felttest')
def vis_felttest():
    skjema = FeltTest(request.args)
    skjema.validate()
    beskjed = [(felt.label.text, felt.data) for felt in skjema]
    return render_template('automatiskskjema.html', beskjed=beskjed, skjema=skjema)


from wtforms.validators import NumberRange

class Løpeskjema(Form):
    avstand = FloatField("Avstand (km)", [InputRequired(), NumberRange(0)])
    tid = DateTimeField("Tid (t:mm:ss)", [InputRequired()], format='%H:%M:%S')
    energi = IntegerField("Energi (kCal)")
    sendinn = SubmitField("Beregn!")


from datetime import datetime
from time import gmtime, strftime

@app.route('/løpekalkulator')
def vis_løpekalkulator():
    skjema = Løpeskjema(request.args)
    if skjema.validate():
        beskjed = {}
        sekunder = (skjema.tid.data - datetime(1900, 1, 1)).total_seconds()
        desimaltimer = sekunder/3600
        beskjed['Hastighet'] = skjema.avstand.data/desimaltimer
        beskjed['Tempo'] = strftime("%M:%S", gmtime(sekunder/skjema.avstand.data))
        beskjed['Kalorier per time'] = skjema.energi.data/desimaltimer
    else:
        beskjed={}
    return render_template("automatiskskjema.html", skjema = skjema , beskjed = beskjed)


tall = 42

class Tallskjema(Form):
    tall = IntegerField("Hviket tall tenker jeg på?", [InputRequired(), NumberRange(1, 100)])
    sendinn = SubmitField("Gjett")


@app.route('/gjett')
def vis_gjett():
    skjema = Tallskjema(request.args)
    if skjema.validate():
        if skjema.tall.data == tall:
            beskjed = f"{skjema.tall.data} er riktig."
        else:
            beskjed = f"{skjema.tall.data} er feil."
    else:
        beskjed = "Du har ikke gjettet noe enda."
    return render_template('automatiskskjema.html', beskjed=beskjed, skjema=skjema)


class Gioppskjema(Tallskjema):
    tall = IntegerField("Hviket tall tenker jeg på?", [NumberRange(1, 100)])
    sendinn = SubmitField("Gjett")
    giopp = SubmitField("Gi opp")


@app.route('/giopp')
def vis_giopp():
    skjema = Gioppskjema(request.args)
    skjema.validate()
    beskjed = [(field.name, field.data) for field in skjema]
    if skjema.sendinn.data:
        if skjema.tall.data == tall:
            beskjed.append(f"{skjema.tall.data} er riktig.")
        else:
            beskjed.append(f"{skjema.tall.data} er feil.")
    elif skjema.giopp.data:
        beskjed.append(f"Du klarte ikke å gjette at tallet var {tall}.")
    else:
        beskjed.append("Du har ikke gjettet noe enda.")
    return render_template('automatiskskjema.html', beskjed=beskjed, skjema=skjema)


@app.route('/hint')
def vis_hint():
    skjema = Tallskjema(request.args)
    skjema.validate()
    beskjed = [(felt.name, felt.data) for felt in skjema]
    if skjema.sendinn.data:
        if skjema.tall.data == tall:
            beskjed.append(f"{skjema.tall.data} er riktig.")
        elif skjema.tall.data > tall:
            beskjed.append(f"{skjema.tall.data} er for høyt.")
        else:
            beskjed.append(f"{skjema.tall.data} er for lavt")
    else:
        beskjed.append("Du har ikke gjettet noe enda.")
    return render_template('automatiskskjema.html', beskjed=beskjed, skjema=skjema)