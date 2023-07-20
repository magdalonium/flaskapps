# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, Flask
from markupsafe import Markup
from importlib import import_module
from inspect import getmembers
import sys
# add your project directory to the sys.path
project_home = "F:\\users\\magdalon\\Dropbox\\Documents\\Python\\mysite\\"
if project_home not in sys.path:
    sys.path = [project_home] + sys.path


deler = []
titler = ["Oppgave 7"]
imports = ["oppgave7"]
moduler = []
from collections import defaultdict
bakgrunnsbilder = defaultdict(lambda: None)
bakgrunnsbilder["oppgave7"] = "bakgrunn_fiskebåt.jpg"
if __name__ == '__main__':
   for x in imports:
        moduler.append(import_module(x))
else:
    for x in imports:
        moduler.append(import_module(".." + x ,__name__))

navn = __file__.split("\\")[-2]
bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')

def konverter(modul, tittel):
    print(__name__)
    navn = modul.__name__.split(".")[-1]
    bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')
    bakgrunn = bakgrunnsbilder[navn]
    for name, attr in getmembers(modul):
      if name.split("_", 1)[0] == "filter":
        bp.add_app_template_filter(attr, name.split("_", 1)[1])
    def index():
        print(navn + '.static')
        print(url_for('static', filename='default.css'))
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
  utdata = []
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
  return render_template("default.html", tittel = "Webapper med Flask", utdata=utdata)

app.register_blueprint(bp, url_prefix='/')


