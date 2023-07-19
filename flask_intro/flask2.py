# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."


heiverden_html="""
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Hei verden!</title>
  </head>
  <body>
    <h1>Hei verden</h1>
    <p>Dette er <b>HTML</b>-versjonen.</p>
  </body>
<html>
"""

@app.route('/html')
def show_html():
    return heiverden_html


heiverden_css = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Hei verden!</title>
    <style>
body {
    width:95%;
    font-family: 'Lucida Grande', Helvetica, Arial, sans-serif;
    background-color: #ffeeee;
}
h1{
    font-family: Georgia, serif;
    font-weight: bold;
}
p {
    margin: 0.5em;
}
    </style>
  </head>
  <body>
    <h1>Hei verden</h1>
    <p>Dette er <b>HTML</b> og <b>CSS</b>-versjonen</p>

  </body>
<html>
"""

@app.route('/css')
def show_css():
    return heiverden_css


heiverden_cssfil = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Hei verden!</title>
    <link rel="stylesheet" href="static/default.css" type="text/css">
  </head>
  <body>
    <h1>Hei verden</h1>
    <p>Dette er <b>HTML</b> og <b>CSS</b>-versjonen</p>

  </body>
<html>
"""

@app.route('/cssfil')
def show_cssfil():
    return heiverden_cssfil