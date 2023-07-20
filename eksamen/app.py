# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, url_for, Flask
from jinja2 import TemplateNotFound
from markupsafe import Markup
from importlib import import_module

TITTEL = "Eksamensoppgaver løst med Python"

titler = ["Høst 2020", "Høst 2021", "Høst 2022", "Vår 2023"]
imports = ["h2020", "h2021", "h2022", "v2023"]
moduler = []

if __name__ == '__main__':
   for x in imports:
        moduler.append(import_module(x + '.app'))
else:
    for x in imports:
        moduler.append(import_module(".." + x + '.app',__name__))

navn = __file__.split("\\")[-2]
bp = Blueprint(navn, __name__, template_folder='templates', static_folder = 'static')

for modul in moduler:
    bp.register_blueprint(modul.bp, url_prefix='/' + modul.__name__.split(".")[-2])

@bp.route('/')
def vis():
  utdata = []
  for navn, tittel in zip(imports, titler):
      utdata.append(Markup(f"<a href='{url_for('.' + navn + '.vis')}'>{tittel}</a>"))
  return render_template("default.html", tittel=TITTEL, utdata=utdata, bakgrunn="bakgrunn_eksamen.jpg")

app = Flask(__name__)
app.register_blueprint(bp)


