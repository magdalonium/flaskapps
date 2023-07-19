# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, url_for, Flask
from jinja2 import TemplateNotFound
from markupsafe import Markup
from . matematikk1T.app import bp as bp1T
from flask import request
bp = Blueprint("v2023", __name__)
bp.register_blueprint(bp1T, url_prefix="/1T")

@bp.route('/')
def vis():
  utdata = []
  utdata.append(Markup(f"<a href='{url_for('.matematikk1T.vis')}'>Matematikk 1T</a>"))
  return render_template("base.html", tittel="Eksamensoppgaver løst med Python - " + bp.name, utdata=utdata)

app = Flask(__name__)
app.register_blueprint(bp)
