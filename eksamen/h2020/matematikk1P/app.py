# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, Flask
from markupsafe import Markup
from importlib import import_module
from inspect import getmembers

TITTEL = "Eksamensoppgaver løst med Python"
UNDERTITTEL = "Matematikk 1P høst 2020"
BAKGRUNN = None

deler = []
titler = ["Oppgave 7"]
imports = ["oppgave7"]
innledninger = [[Markup("<p>Denne webappen løser oppgave 7 fra <a href='https://matematikk.net/matteprat/download/file.php?id=3290'>Eksamen i Matematikk 1P høsten 2020 (Kunnskapsløftet)</a>. Oppgaven handler om å regne ut provisjon for videresalg av fisk. Jeg har laget en webapp med den samme funksjonaliteten som regnearket i oppgaveteksten.</p>"),
                 Markup("<p>Jeg har også laget en forklaring på hvordan jeg laget webappen: <a href='https://magdalon.wordpress.com/2023/05/05/eksamen-1p-host-2020-oppgave-7-webapp/'>Eksamen 1P høst 2020: Oppgave 7 – webapp - Magdalons syn på verden</a></p>")]
                ]
moduler = []
from collections import defaultdict
bakgrunnsbilder = defaultdict(lambda: None)
bakgrunnsbilder["oppgave7"] = "bilder/bakgrunn/fiskebåt.jpg"
if __name__ == '__main__':
   for x in imports:
        moduler.append(import_module(x))
else:
    for x in imports:
        moduler.append(import_module(".." + x ,__name__))

from pathlib import Path
navn = Path(__file__).parts[-2]
bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')

def konverter(modul, tittel, innledning=None):
    navn = modul.__name__.split(".")[-1]
    bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')
    bakgrunn = bakgrunnsbilder[navn]
    for name, attr in getmembers(modul):
      if name.split("_", 1)[0] == "filter":
        bp.add_app_template_filter(attr, name.split("_", 1)[1])
    def index():
        utdata = []
        for rule in modul.app.url_map.iter_rules():
          if rule.endpoint.split(".")[-1] =='show':
            pass
          elif not rule.arguments:
            utdata.append(Markup(f"<p><a href='{url_for('.' + rule.endpoint)}'>{rule}</a></p>"))
          elif (rule.defaults and rule.arguments.issubset(rule.defaults.keys())):
            utdata.append(Markup(f"<p><a href='{rule}'>{rule}</a></p>"))
          elif not "static" in str(rule).split("/"):
            utdata.append(rule)
        return render_template("default.html",
                               tittel=tittel,
                               innledning=innledning,
                               utdata=utdata,
                               bakgrunn=bakgrunn)
    bp.add_url_rule('/innhold', view_func = index)
    for rule in modul.app.url_map.iter_rules():
        bp.add_url_rule(rule.rule, view_func = modul.app.view_functions[rule.endpoint])
    return bp


for modul, tittel, innledning in zip(moduler, titler, innledninger):
    bp.register_blueprint(konverter(modul, tittel, innledning),
                       url_prefix='/' + modul.__name__.split(".")[-1]
                       )
app = Flask(__name__)
@bp.route('/')
def vis():
  utdata = [Markup(f"<h2>{UNDERTITTEL}</h2>")]
  for modul, tittel in zip(imports, titler):
      utdata.append(Markup(f"<p><a href='{url_for('.' + modul + '.index')}'>{tittel}</a></p>"))
  utdata.append(Markup("<h2>Registrerte stier</h2>"))
  for rule in app.url_map.iter_rules():
    if rule.endpoint.split(".")[-1] =='vis':
        pass
    elif not rule.arguments:
      utdata.append(Markup(f"<p><a href='{rule}'>{rule}</a></p>"))
    elif not "static" in str(rule).split("/"):
      utdata.append(rule)
  return render_template("default.html", tittel = TITTEL, utdata=utdata)

app.register_blueprint(bp, url_prefix='/')


