# -*- coding: utf-8 -*-

#Vi kan bruke tankegangen fra skjemaer til å generere et enkelt HTML-dokument med vilkårlige elementer.

from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."

from markupsafe import Markup

class Element():
    pass

class Bilde(Element):
    mal = "<img src='{URI}'>"
    def __init__(self, URI):
        self.URI = URI
    def __str__(self):
        return Markup(self.mal.format(URI = self.URI))
        
class Avsnitt(Element):
    mal = "<img src='{URI}'>"
    def __init__(self, innhold):
        self.innhold = innhold
    def __str__(self):
        return Markup(self.mal.format(innhold = self.innhold))
    
class Overskrift(Element):
    mal = "<h{{nivå}}>{{innhold}}</h{{nivå}}>"
    def __init__(self, nivå, innhold):
        self.nivå = nivå
        self.innhold = innhold
    def __str__(self):
        return Markup(self.mal.format(nivå = self.nivå, innhold=self.innhold))
