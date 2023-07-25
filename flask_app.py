# -*- coding: utf-8 -*-
from flask import render_template, url_for, Flask
from markupsafe import Markup

try:
    import sys
    # add your project directory to the sys.path
    project_home = "F:\\users\\magdalon\\Dropbox\\Documents\\Python\\mysite\\"
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path
except Exception:
    pass


from eksamen.app import bp as bpe
from flask_intro.app import bp as bpi
from fifa23.app import bp as bpf
app = Flask(__name__)
app.register_blueprint(bpe, url_prefix="/eksamen")
app.register_blueprint(bpi, url_prefix="/python_intro")
app.register_blueprint(bpf, url_prefix="/fifa23")

eksamenssett = [('eksamen.h2020.matematikk1P.oppgave7.index', 'Matematikk 1P høst 2020: Oppgave 7'),
                ('eksamen.h2021.matematikk1P.oppgave7.index', 'Matematikk 1P høst 2021: Oppgave 7'),
                ('eksamen.h2022.matematikk1P.del1.index', 'Matematikk 1P høst 2022: Del 1'),
                ('eksamen.h2022.matematikk1P.oppgave7.index', 'Matematikk 1P høst 2022: Oppgave 7'),
                ('eksamen.v2023.matematikk1T.del1.index', 'Matematikk 1T vår 2023: Del 1')]

@app.route('/')
def vis():
  utdata = [Markup("<h2>Innledning</h2>"),
            Markup("Dette er en side jeg har satt sammen for å vise webapper laget med <a href='https://flask.palletsprojects.com/'>Flask</a>. Forklaringer finner du på hjemmesiden min: <a href='https://magdalon.wordpress.com/tag/flask/'>Magdalons syn på verden</a>"),
            Markup("<h2>Prosjekter</h2>"),
            Markup(f"<a href='{url_for('flask_intro.vis')}'>Introduksjon til webapper med Flask</a>"),
            Markup(f"<a href='{url_for('eksamen.vis')}'>Eksamensoppgaver</a>"),
            Markup(f"<a href='{url_for('fifa23.vis_søyle')}'>VM-kalkulator</a>"),
            Markup("<h2>Eksamensoppgaver</h2>")]
  for ende, tittel in eksamenssett:
      utdata.append(Markup(f"<a href='{url_for(ende)}'>{tittel}</a>"))
  return render_template("default.html", tittel="Magdalons lekegrind", utdata=utdata, bakgrunn='bilder/bakgrunn/fremtidens_skole.jpg')

"""
  utdata.append(Markup("<h2>Registrerte stier</h2>"))
  for rule in app.url_map.iter_rules():
    if rule.endpoint.split(".")[-1] =='vis':
        pass
    elif not rule.arguments:
      utdata.append(Markup(f"<a href='{url_for(rule.endpoint)}'>{rule}</a>"))
    else:
      utdata.append(rule)
"""

"""
import pytest
client = app.test_client()
responses = []
ignores = []

for rule in app.url_map.iter_rules():
    if not rule.arguments:
        responses.append(client.get(rule.rule))
    else:
        ignores.append(rule)

errors = [resp for resp in responses if resp.status_code != 200]

@app.route('/feil')
def vis_feil():
    utdata = [Markup("<h2>Feilrapport</h2>")]
    for err in errors:
        path, status = err.request.path, err.status
        utdata.append(Markup(f"<a href='{path}'>{path}: <b>{status}</b></a>"))
    return render_template("default.html", tittel="Magdalons lekegrind", utdata=utdata, bakgrunn='bilder/bakgrunn/fremtidens_skole.jpg')
"""
