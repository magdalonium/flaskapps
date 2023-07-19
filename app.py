# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, url_for, Flask
from jinja2 import TemplateNotFound
from markupsafe import Markup

from . eksamen.app import bp as bpe
from . flask_intro.app import bp as bpi

app = Flask(__name__)
app.register_blueprint(bpe, url_prefix="/eksamen")
app.register_blueprint(bpi, url_prefix="/python_intro")


@app.route('/')
def vis():
  utdata = [Markup("<h2>Innledning</h2>"),
            Markup("Dette er en side jeg har satt sammen for å vise webapper laget med <a href='https://flask.palletsprojects.com/'>Flask</a>. Forklaringer finner du på hjemmesiden min: <a href='https://magdalon.wordpress.com/tag/flask/'>Magdalons syn på verden</a>"),
            Markup("<h2>Prosjekter</h2>"),
            Markup(f"<a href='{url_for('flask_intro.vis')}'>Introduksjon til webapper med Flask</a>"),
            Markup(f"<a href='{url_for('eksamen.vis')}'>Eksamensoppgaver</a>"),
            Markup("<h2>Registrerte stier</h2>")]
  for rule in app.url_map.iter_rules():
    if rule.endpoint.split(".")[-1] =='vis':
        pass
    elif not rule.arguments:
      utdata.append(Markup(f"<a href='{url_for(rule.endpoint)}'>{rule}</a>"))
    elif not "static" in str(rule).split("/"):
      utdata.append(rule)
  return render_template("base.html", tittel="Magdalons lekegrind", utdata=utdata)




