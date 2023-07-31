# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, Flask
from markupsafe import Markup
from importlib import import_module
from inspect import getmembers

TITTEL = "Eksamensoppgaver løst med Python"
UNDERTITTEL = "Matematikk 1P høst 2022"
BAKGRUNN = None
deler = []
titler = ["Del 1", "Oppgave 7"]
imports = ["del1", "oppgave7"]
innledninger = [[Markup("<p>Denne webappen løser del 1 fra <a href='https://matematikk.net/matteprat/download/file.php?id=4538'>Eksamen i Matematikk 1P høsten 2022 (Fagfornyelsen)</a>. Denne webappen gjør prosentregning, arealberegninger, regresjon og undersøker proporsjonale størrelser. </p>"),
                 Markup("<p>Jeg har også laget en forklaring på hvordan jeg laget webappen: <a href='https://magdalon.wordpress.com/2023/05/06/eksamen-i-matematikk-1plk20-host-2022-del-1-webapp/'>Eksamen i Matematikk 1P(LK20) høst 2022: Del 1 – webapp - Magdalons syn på verden</a></p>")],
                [Markup("<p>Denne webappen løser oppgave 7 fra <a href='https://matematikk.net/matteprat/download/file.php?id=4538'>Eksempeleksamen i Matematikk 1P høsten 2021 (Fagfornyelsen)</a>. Oppgaven handler om å lage et enkelt fakturasystem for takeaway.  Jeg har laget en webapp med den samme funksjonaliteten som regnearket i oppgaveteksten.</p>"),
                                 Markup("<p>Jeg har også laget en forklaring på hvordan jeg laget webappen: <a href='https://magdalon.wordpress.com/2023/04/25/eksamen-1p-var-2022-oppgave-7-webapp/'>Eksamen 1P høst 2022: Oppgave 7 – webapp - Magdalons syn på verden</a></p>")]]
moduler = []
from collections import defaultdict
bakgrunnsbilder = defaultdict(lambda: None)
bakgrunnsbilder["oppgave7"] = "bilder/bakgrunn/kantine.jpg"
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

