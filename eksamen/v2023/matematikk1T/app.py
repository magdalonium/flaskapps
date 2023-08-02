# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, Flask
from markupsafe import Markup
from importlib import import_module
from inspect import getmembers

TITTEL = "Eksamensoppgaver løst med Python"
UNDERTITTEL = "Matematikk 1T vår 2023"
BAKGRUNN = None

deler = []
titler = ["Del 1"]
imports = ["del1"]
innledninger = [[Markup("<p>Denne webappen løser del 1 fra <a href='https://matematikk.net/matteprat/download/file.php?id=4715'>Eksamen i Matematikk 1T våren 2023 (Fagfornyelsen)</a>. Denne webappen gjør trigonometriske beregninger, finner skjæringspunkter, løser likninger, undersøker rasjonale funksjoner og finner fjerdegradsfunksjoner.</p>")]]
moduler = []

from collections import defaultdict
bakgrunnsbilder = defaultdict(lambda: None)
bakgrunnsbilder["oppgave7"] = "bakgrunn_løping_jente.jpg"

if __name__ == '__main__':
   for x in imports:
        moduler.append(import_module(x))
else:
    for x in imports:
        moduler.append(import_module(".." + x ,__name__))

from pathlib import Path
navn = Path(__file__).parts[-2]
bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')

from collections import defaultdict
endepunkter = defaultdict(lambda: [])

def konverter(modul, tittel, innledning=None):
    navn = modul.__name__.split(".")[-1]
    bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')
    bakgrunn = bakgrunnsbilder[navn]
    for name, attr in getmembers(modul):
      if name.split("_", 1)[0] == "filter":
        bp.add_app_template_filter(attr, navn.split("_", 1)[1])
    def vis_innhold():
        utdata = []
        for rule in modul.app.url_map.iter_rules():
          if rule.endpoint.split(".")[-1] in ['show', 'vis']:
            pass
          elif not rule.arguments:
            utdata.append(Markup(f"<p><a href='{url_for('.' + rule.endpoint)}'>{rule}</a></p>"))
          elif (rule.defaults and rule.arguments.issubset(rule.defaults.keys())):
            utdata.append(Markup(f"<p><a href='{rule}'>{rule}</a></p>"))
          elif not "static" in str(rule).split("/"):
            utdata.append(rule)
        return render_template("default.html",
                               tittel = tittel,
                               innledning = innledning,
                               utdata=utdata,
                               bakgrunn=bakgrunn)
    bp.add_url_rule('/innhold', view_func = vis_innhold)

    endepunkter[navn] = [('index', '/innhold')]
    for rule in modul.app.url_map.iter_rules():
        if not (rule.arguments or rule.endpoint in ['vis', 'show']):
            endepunkter[navn].append((rule.endpoint, rule.rule))
        bp.add_url_rule(rule.rule, view_func = modul.app.view_functions[rule.endpoint])
    return bp


for modul, tittel, innledning in zip(moduler, titler, innledninger):
    bp.register_blueprint(konverter(modul, tittel, innledning),
                       url_prefix='/' + modul.__name__.split(".")[-1],
                       template_folder = "templates",
                       static_folder = "static"
                       )
app = Flask(__name__)
@bp.route('/')
def vis():
  brødtekst = [Markup(f"<h2>{UNDERTITTEL}</h2>")]
  brødtekst.append(Markup(f"<h3><a href='{url_for('.' + imports[0] + '.index')}'>{titler[0]}</a></h3>"))
  for ende, understi in endepunkter[imports[0]]:
      sti = url_for("." + imports[0] + "." + ende)
      brødtekst.append(Markup(f"<p><a href = {sti}>{understi}</a></p>"))
  brødtekst.append(Markup("<h3>Del 2</h3>"))
  for modul, tittel in zip(imports[1:], titler[1:]):
      brødtekst.append(Markup(f"<h4><a href='{url_for('.' + modul + '.index')}'>{tittel}</a></h4>"))
      for ende, understi in endepunkter[modul]:
          sti = url_for("." + modul + "." + ende)
          brødtekst.append(Markup(f"<p><a href = {sti}>{understi}</a></p>"))

  return render_template("default.html", tittel = TITTEL, brødtekst=brødtekst, bakgrunn=None)

app.register_blueprint(bp, url_prefix='/')

