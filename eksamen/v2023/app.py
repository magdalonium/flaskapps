# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, url_for, Flask
from jinja2 import TemplateNotFound
from markupsafe import Markup
from flask import request
from importlib import import_module

TITTEL = "Eksamensoppgaver løst med Python"
UNDERTITTEL = "Vår 2023"
BAKGRUNN = "bakgrunn_eksamen.jpg"
titler = ["Matematikk 1T"]
imports = ["matematikk1T"]

moduler = []
if __name__ == '__main__':
   for x in imports:
        moduler.append(import_module(x + '.app'))
else:
    for x in imports:
        moduler.append(import_module(".." + x + '.app',__name__))

from pathlib import Path
navn = Path(__file__).parts[-2]
bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')

for modul in moduler:
    bp.register_blueprint(modul.bp, url_prefix='/' + modul.__name__.split(".")[-2])

@bp.route('/')
def vis():
  utdata = [Markup(f"<h2>{UNDERTITTEL}</h2>")]
  for navn, tittel in zip(imports, titler):
      utdata.append(Markup(f"<a href='{url_for('.' + navn + '.vis')}'>{tittel}</a>"))
  return render_template("default.html", tittel=TITTEL, utdata=utdata, bakgrunn=BAKGRUNN)

app = Flask(__name__)
app.register_blueprint(bp)
