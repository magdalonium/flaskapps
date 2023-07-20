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

navn = __file__.split("\\")[-2]
bp = Blueprint(navn, __name__)

from collections import defaultdict
endepunkter = defaultdict(lambda: [])

def konverter(modul, tittel):
    navn = modul.__name__.split(".")[-1]
    bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')
    bakgrunn = bakgrunnsbilder[navn]
    for name, attr in getmembers(modul):
      if name.split("_", 1)[0] == "filter":
        bp.add_app_template_filter(attr, navn.split("_", 1)[1])
    def index():
        utdata = []
        for rule in modul.app.url_map.iter_rules():
          if rule.endpoint.split(".")[-1] in ['show', 'vis']:
            pass
          elif not rule.arguments:
            utdata.append(Markup(f"<a href='{url_for('.' + rule.endpoint)}'>{rule}</a>"))
          elif (rule.defaults and rule.arguments.issubset(rule.defaults.keys())):
            utdata.append(Markup(f"<a href='{rule}'>{rule}</a>"))
          elif not "static" in str(rule).split("/"):
            utdata.append(rule)
        return render_template("default.html", tittel = tittel, utdata=utdata, bakgrunn=bakgrunn)
    bp.add_url_rule('/innhold', view_func = index)

    endepunkter[navn] = [('index', '/innhold')]
    for rule in modul.app.url_map.iter_rules():
        if not (rule.arguments or rule.endpoint in ['vis', 'show']):
            endepunkter[navn].append((rule.endpoint, rule.rule))
        bp.add_url_rule(rule.rule, view_func = modul.app.view_functions[rule.endpoint])
    return bp


for modul, tittel in zip(moduler, titler):
    bp.register_blueprint(konverter(modul, tittel),
                       url_prefix='/' + modul.__name__.split(".")[-1],
                       template_folder = "templates",
                       static_folder = "static"
                       )
app = Flask(__name__)
@bp.route('/')
def vis():
  utdata = [Markup(f"<h2>{UNDERTITTEL}</h2>")]
  utdata.append(Markup(f"<h3><a href='{url_for('.' + imports[0] + '.index')}'>{titler[0]}</a></h3>"))
  for ende, understi in endepunkter[imports[0]]:
      sti = url_for("." + imports[0] + "." + ende)
      utdata.append(Markup(f"<a href = {sti}>{understi}</a>"))
  utdata.append(Markup("<h3>Del 2</h3>"))
  for modul, tittel in zip(imports[1:], titler[1:]):
      utdata.append(Markup(f"<h4><a href='{url_for('.' + modul + '.index')}'>{tittel}</a></h4>"))
      for ende, understi in endepunkter[modul]:
          sti = url_for("." + modul + "." + ende)
          utdata.append(Markup(f"<a href = {sti}>{understi}</a>"))

  return render_template("default.html", tittel = TITTEL, utdata=utdata, bakgrunn=None)

app.register_blueprint(bp, url_prefix='/')

