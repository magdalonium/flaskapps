# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, Flask
from markupsafe import Markup
from importlib import import_module
from inspect import getmembers

SIDETITTEL = "Webapper med Flask"
INNLEDNING = Markup("<p>Dette er en samling med små webapper.</p>")
BAKGRUNN = "bilder/bakgrunn/havnekran.jpg"
deler = []
titler = ["Flask del 2 HTML og CSS",
          "Flask del 3 Dynamiske webapper med GET",
          "Flask del 4 Skjemaer",
          "Flask del 5 Grafisk fremstilling",
          "Flask del 6 Lineær regresjon",
          "Flask del 7 Maler med Jinja",
          "Flask del 8 Mer om Jinja-uttrykk",
          "Flask del 9 Kontrollstrukturer i Jinja",
          "Flask del 10 Mer om skjemaer"]
imports = ["flask2", "flask3", "flask4", "flask5",
           "flask6", "flask7", "flask8", "flask9",
           "flask10"]
moduler = []

from collections import defaultdict
bakgrunnsbilder = defaultdict(lambda: None)
bakgrunnsbilder["flask2"] = "bilder/bakgrunn/maling.jpg"

if __name__ == '__main__':
   for x in imports:
        moduler.append(import_module(x))
else:
    for x in imports:
        moduler.append(import_module(".." + x ,__name__))

bp = Blueprint('flask_intro', __name__)

def konverter(modul, tittel):
    navn = modul.__name__.split(".")[-1]
    bakgrunn = bakgrunnsbilder[navn]
    bp = Blueprint(navn, __name__, template_folder='templates')
    for navn, attr in getmembers(modul):
      if navn.split("_", 1)[0] == "filter":
        bp.add_app_template_filter(attr, navn.split("_", 1)[1])
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
  innledning = [INNLEDNING,
            Markup("<h3>Innhold</h3>")]
  for modul, tittel in zip(imports, titler):
      innledning.append(Markup(f"<p><a href='{url_for('.' + modul + '.index')}'>{tittel}</a></p>"))
  return render_template("default.html", tittel = SIDETITTEL, innledning=innledning, bakgrunn = BAKGRUNN)

app.register_blueprint(bp, url_prefix='/')
