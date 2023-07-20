# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, Flask
from markupsafe import Markup
from importlib import import_module
from inspect import getmembers

TITTEL = "Eksamen Matematikk 1P høst 2022"
deler = []
titler = ["Del 1", "Oppgave 7"]
imports = ["del1", "oppgave7"]
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

def konverter(modul, tittel):
    navn = modul.__name__.split(".")[-1]
    bp = Blueprint(navn, __name__, template_folder='templates')
    bakgrunn = bakgrunnsbilder[navn]
    for navn, attr in getmembers(modul):
      if navn.split("_", 1)[0] == "filter":
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
    for rule in modul.app.url_map.iter_rules():
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
  utdata = []
  for modul, tittel in zip(imports, titler):
      utdata.append(Markup(f"<a href='{url_for('.' + modul + '.index')}'>{tittel}</a>"))
  return render_template("default.html", tittel = TITTEL, utdata=utdata)

app.register_blueprint(bp, url_prefix='/')


