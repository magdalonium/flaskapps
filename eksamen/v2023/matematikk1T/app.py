# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, Flask
from markupsafe import Markup
from importlib import import_module
from inspect import getmembers
from pathlib import Path
from collections import defaultdict

TITTEL = "Eksamensoppgaver løst med Python"
UNDERTITTEL = "Matematikk 1T vår 2023"
INNLEDNING = [Markup("<p>Denne webappen løser <a href='https://matematikk.net/matteprat/download/file.php?id=4715'>Eksamen i Matematikk 1T våren 2023 (Fagfornyelsen)</a>.")]
BAKGRUNN = None

deler = {"del1" : {"tittel": "Del 1",
                   "innledning": [Markup("<p>Denne webappen løser del 1 fra <a href='https://matematikk.net/matteprat/download/file.php?id=4715'>Eksamen i Matematikk 1T våren 2023 (Fagfornyelsen)</a>. Denne webappen gjør trigonometriske beregninger, finner skjæringspunkter, løser likninger, undersøker rasjonale funksjoner og finner fjerdegradsfunksjoner.</p>")],
                   "bakgrunn": None}}

navn = Path(__file__).parts[-2]
bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')
bp.tittel = TITTEL
bp.undertittel = UNDERTITTEL
bp.innledning = INNLEDNING
bp.bakgrunn = BAKGRUNN

def importer(imports):
    moduler = {}
    if __name__ == '__main__':
        for x in imports:
            moduler[x] = import_module(x)
    else:
        for x in imports:
            moduler[x] = import_module(".." + x ,__name__)
    return moduler

moduler = importer(deler.keys())

endepunkter = defaultdict(lambda: [])

def konverter(modul):
    navn = modul.__name__.split(".")[-1]
    bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')
    for k, v in deler[navn].items():
        setattr(bp, k, v)
    for name, attr in getmembers(modul):
      if name.split("_", 1)[0] == "filter":
        bp.add_app_template_filter(attr, name.split("_", 1)[1])
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
                               tittel = bp.tittel,
                               innledning = bp.innledning,
                               utdata=utdata,
                               bakgrunn=bp.bakgrunn)
    bp.add_url_rule('/innhold', view_func = vis_innhold)
    endepunkter[navn] = [('vis_innhold', '/innhold')]
    bp.endepunkter = []
    for rule in modul.app.url_map.iter_rules():
        if not (rule.arguments or rule.endpoint in ['vis', 'show']):
            endepunkter[navn].append((rule.endpoint, rule.rule))
        bp.add_url_rule(rule.rule, view_func = modul.app.view_functions[rule.endpoint])
        bp.endepunkter.append((rule.endpoint, rule.rule))
    return bp

bp.blueprints = {}
for navn, modul in moduler.items():
    blue = konverter(modul)
    bp.register_blueprint(blue,
                          url_prefix='/' + navn,
                          template_folder = "templates",
                          static_folder = "static"
                          )
    bp.blueprints[navn]= blue

bp.endepunkter = endepunkter
app = Flask(__name__)
@bp.route('/')
def vis():
  brødtekst = []
  if 'del1' in bp.blueprints:
      brødtekst.append(Markup(f"<h3><a href='{url_for('.del1.vis_innhold')}'>{bp.blueprints['del1'].tittel}</a></h3>"))
      for element in bp.blueprints['del1'].innledning:
          brødtekst.append(element)
      for ende, understi in bp.endepunkter['del1']:
          sti = url_for(".del1." + ende)
          brødtekst.append(Markup(f"<p><a href = {sti}>{understi}</a></p>"))
  rest = set(bp.blueprints).difference({'del1'})
  if rest:
      brødtekst.append(Markup("<h3>Del 2</h3>"))
      for navn in list(bp.blueprints.keys())[1:]:
          brødtekst.append(Markup(f"<h4><a href='{url_for('.' + navn + '.vis_innhold')}'>{moduler[navn].tittel}</a></h4>"))
          for ende, understi in bp.endepunkter[navn]:
              sti = url_for("." + navn + "." + ende)
              brødtekst.append(Markup(f"<p><a href = {sti}>{understi}</a></p>"))
  return render_template("default.html",
                         tittel = TITTEL,
                         undertittel = UNDERTITTEL,
                         innledning = INNLEDNING,
                         brødtekst=brødtekst,
                         bakgrunn=None)

app.register_blueprint(bp, url_prefix='/')
