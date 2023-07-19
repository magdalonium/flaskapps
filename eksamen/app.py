# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, url_for, Flask
from jinja2 import TemplateNotFound
from markupsafe import Markup
from . v2023.app import bp as bpv23

bp = Blueprint("eksamen", __name__)
bp.register_blueprint(bpv23, url_prefix="/v2023")

@bp.route('/')
def vis():
  utdata = []
  utdata.append(Markup(f"<a href='{url_for('.v2023.vis')}'>Vår 2023</a>"))
  return render_template("base.html", tittel="Eksamensoppgaver løst med Python", utdata=utdata)

app = Flask(__name__)
app.register_blueprint(bp)

