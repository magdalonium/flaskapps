# -*- coding: utf-8 -*-

from flask import render_template, Flask

app = Flask(__name__)

@app.route('/')
def vis():
    return render_template("base.html",
                           tittel = "Tittel",
                           utdata = ["Plassholdertekst"],
                           bakgrunn = "bakgrunn.jpg")
