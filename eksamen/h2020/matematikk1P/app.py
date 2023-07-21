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

def konverter(modul, tittel):
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
                       url_prefix='/' + modul.__name__.split(".")[-1]
                       )
app = Flask(__name__)
@bp.route('/')
def vis():
  utdata = [Markup(f"<h2>{UNDERTITTEL}</h2>")]
  for modul, tittel in zip(imports, titler):
      utdata.append(Markup(f"<a href='{url_for('.' + modul + '.index')}'>{tittel}</a>"))
  utdata.append(Markup("<h2>Registrerte stier</h2>"))
  for rule in app.url_map.iter_rules():
    if rule.endpoint.split(".")[-1] =='vis':
        pass
    elif not rule.arguments:
      utdata.append(Markup(f"<a href='{rule}'>{rule}</a>"))
    elif not "static" in str(rule).split("/"):
      utdata.append(rule)
  return render_template("default.html", tittel = TITTEL, utdata=utdata)

app.register_blueprint(bp, url_prefix='/')


