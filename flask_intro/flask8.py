###---del8---
from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."


from flask import render_template

@app.route('/eksempel/<eksempelnavn>')
def show_eksempel(eksempelnavn):
    return render_template(f"{eksempelnavn}.html")


from time import gmtime, strftime

@app.template_filter("klokkeslett")
def filter_klokkeslett(s):
    if s >= 3600:
        return strftime("%H:%M:%S", gmtime(s))
    else:
        return strftime("%M:%S", gmtime(s))


from babel.numbers import format_decimal

@app.template_filter("desimaltall") #OBS
def filter_desimaltall(tall):
    return format_decimal(tall, locale='no')


løpedata = [{"tid": 3122, "avstand": 8.11, "kommentar": "Sammen med Kristine"},
            {"tid": 3969, "avstand": 9.99},
            {"tid": 3123, "avstand": 8.55}]


@app.route('/løpelogg')
def show_løpelogg():
    return render_template("løpelogg.html", løpedata = løpedata)

#Tillegg

from markupsafe import Markup
from flask import url_for

@app.route('/eksempel/indeks')
def vis_indeks():
    utdata = [
        Markup(f"<a href='{url_for('.show_eksempel', eksempelnavn='blokktest')}'>blokktest.html</a>"),
        Markup(f"<a href='{url_for('.show_eksempel', eksempelnavn='iftest')}'>iftest.html</a>"),
        Markup(f"<a href='{url_for('.show_eksempel', eksempelnavn='filtertest')}'>filtertest.html</a>"),
        Markup(f"<a href='{url_for('.show_eksempel', eksempelnavn='klokketest')}'>klokketest.html</a>"),
        Markup(f"<a href='{url_for('.show_eksempel', eksempelnavn='talltest')}'>talltest.html</a>"),
        Markup(f"<a href='{url_for('.show_eksempel', eksempelnavn='mattetest')}'>mattetest.html</a>"),
        ]
    return render_template("default.html", tittel = "Flask del 8: Mer om Jinja-uttrykk", utdata=utdata)
