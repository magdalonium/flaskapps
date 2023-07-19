# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, Flask
from markupsafe import Markup

if __name__ == '__main__':
    import del1
else:
    from . import del1

bp = Blueprint('matematikk1T', __name__)

del1_bp = Blueprint('del1', __name__)


@del1_bp.route('/')
def index1():
  utdata = []
  for rule in del1.app.url_map.iter_rules():
    if not (rule.arguments or rule.endpoint.split(".")[-1] =='vis'):
      utdata.append(Markup(f"<a href='{url_for('.' + rule.endpoint)}'>{rule}</a>"))
  return render_template("base.html", tittel = "Eksamen 1T vår 2020", utdata=utdata)

for rule in del1.app.url_map.iter_rules():
    del1_bp.add_url_rule(rule.rule, view_func = del1.app.view_functions[rule.endpoint])


bp.register_blueprint(del1_bp,
                       url_prefix='/del1')

app = Flask(__name__)
@bp.route('/')
def vis():
  utdata = []
  utdata.append(Markup("<h3>Del 1</h3>"))
  utdata.append(Markup(f"<a href='{url_for('.del1.vis')}'>Del 1 [{url_for('.del1.vis')}]</a>"))
  utdata.append(Markup("<h3>Del 2</h3>"))
  return render_template("base.html", tittel = "Eksamen 1T vår 2020", utdata=utdata)


app.register_blueprint(bp, url_prefix='/')
