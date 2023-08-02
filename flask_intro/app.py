# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, Flask
from markupsafe import Markup
from importlib import import_module
from inspect import getmembers

SIDETITTEL = "Webapper med Flask"
INNLEDNING = Markup("<p>Dette er en samling med små webapper som introduserer oss til <a href='https://www.python.org/'>Python</a>-biblioteket <a href='https://flask.palletsprojects.com/en/2.3.x/'>Flask</a>. Forklaringer ligger på </p>")
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
innledninger = [[Markup("<p>Denne webappen viser hvordan vi kan styre utseendet til nettsider med HTML og CSS. Forklaringen ligger på <a href='https://magdalon.wordpress.com/2023/04/16/flask-2-html-og-css/'>Flask 2: HTML og CSS - Magdalons syn på verden</a>.</p>")],
                [Markup("<p>Denne webappen viser hvordan vi kan svare på brukerinput. Forklaringen ligger på <a href='https://magdalon.wordpress.com/2023/04/17/flask-3-dynamiske-webapper/'>Flask 3: Dynamiske webapper - Magdalons syn på verden</a>.</p>")],
                [Markup("<p>Denne webappen viser hvordan vi kan bruke HTML-skjemaer til å ta i mot brukerinput. Forklaringen ligger på <a href='https://magdalon.wordpress.com/2023/04/18/flask-4-html-skjemaer/'>Flask 4: HTML-skjemaer - Magdalons syn på verden</a>.</p>")],
                [Markup("<p>Denne webappen viser hvordan vi kan vise biler og grafer på nett. Til slutt kommer det et eksempel om andregradslikninger. <a href='https://magdalon.wordpress.com/2023/04/19/flask-5-grafisk-framstilling/'>Flask 5: Grafisk framstilling - Magdalons syn på verden</a>.</p>")],
                [Markup("<p>Denne webappen utfører lineær regresjon. Forklaringen ligger på <a href='https://magdalon.wordpress.com/2023/04/20/flask-6-lineaer-regresjon/'>Flask 6: Lineær regresjon - Magdalons syn på verden</a>.</p>")],
                [Markup("<p>Denne webappen viser eksempler på <i>template</i>-språket <a href='https://palletsprojects.com/p/jinja/'>Jinja</a>. Forklaringen ligger på <a href='https://magdalon.wordpress.com/2023/04/21/flask-7-maler-med-jinja/'>Flask 7: Maler med Jinja - Magdalons syn på verden</a>.</p>")],
                [Markup("Denne webappen viser mer avanserte eksempler på <i>template</i>-språket <a href='https://palletsprojects.com/p/jinja/'>Jinja</a>. Forklaringen ligger på <a href='https://magdalon.wordpress.com/2023/04/22/flask-8-mer-om-jinja-uttrykk/'>Flask 8: Mer om Jinja-uttrykk - Magdalons syn på verden</a>.</p>")],
                [Markup("<p>Denne webappen viser eksempler på <code>for</code>-løkker og <code>if</code>-setninger i <a href='https://palletsprojects.com/p/jinja/'>Jinja</a>. Forklaringen ligger på <a href='https://magdalon.wordpress.com/2023/04/23/flask-9-kontrollstrukturer-i-jinja/'>Flask 9: Kontrollstrukturer i Jinja - Magdalons syn på verden</a>.</p>")],
                [Markup("<p>Denne webappen viser hvordan vi kan bruke <a href='https://wtforms.readthedocs.io/en/3.0.x/'>WTForms</a> til å lage og behandle skjemaer. Forklaringen ligger på <a href='https://magdalon.wordpress.com/2023/04/24/flask-10-mer-om-skjemaer/'>Flask 10: Mer om skjemaer - Magdalons syn på verden</a>.</p>")],
                ]
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

def konverter(modul, tittel, innledning=None):
    navn = modul.__name__.split(".")[-1]
    bakgrunn = bakgrunnsbilder[navn]
    bp = Blueprint(navn, __name__, template_folder='templates')
    for navn, attr in getmembers(modul):
      if navn.split("_", 1)[0] == "filter":
        bp.add_app_template_filter(attr, navn.split("_", 1)[1])
    def index():
        stier = []
        for rule in modul.app.url_map.iter_rules():
          if rule.endpoint.split(".")[-1] =='show':
            pass
          elif not rule.arguments:
            stier.append(Markup(f"<p><a href='{url_for('.' + rule.endpoint)}'>{rule}</a></p>"))
          elif (rule.defaults and rule.arguments.issubset(rule.defaults.keys())):
            stier.append(Markup(f"<p><a href='{rule}'>{rule}</a></p>"))
          elif not "static" in str(rule).split("/"):
            stier.append(Markup(f"<p>{rule}</p>"))
        return render_template("default.html",
                               tittel = SIDETITTEL,
                               undertittel= tittel,
                               innledning=innledning,
                               stier=stier,
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
  innledning = [INNLEDNING,
            Markup("<h3>Innhold</h3>")]
  for modul, tittel in zip(imports, titler):
      innledning.append(Markup(f"<p><a href='{url_for('.' + modul + '.index')}'>{tittel}</a></p>"))
  return render_template("default.html", tittel = SIDETITTEL, innledning=innledning, bakgrunn = BAKGRUNN)

app.register_blueprint(bp, url_prefix='/')
