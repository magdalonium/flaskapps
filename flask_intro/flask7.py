# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

@app.route('/')
def show():
    return "Dette er en testserver."


from flask import render_template

@app.route('/hello')
def show_hello():
    return render_template("hello.html")


@app.route('/personlig/<person>')
def show_personlig(person):
    return render_template("personlig.html", navn=person)


navn = 'Loke'
personer = ['Loke', 'Line', 'Quoc']
biler = {'Loke' : 'Tesla', 'Line' : 'Volkswagen', 'Quoc' : 'BMW'}

@app.route('/biler')
def show_biler():
    return render_template("biler.html", navn=navn, personer=personer, biler=biler)


dataURI = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDADIiJSwlHzIsKSw4NTI7S31RS0VFS5ltc1p9tZ++u7Kfr6zI4f/zyNT/16yv+v/9////////wfD/////////////2wBDATU4OEtCS5NRUZP/zq/O////////////////////////////////////////////////////////////////////wAARCAAYAEADAREAAhEBAxEB/8QAGQAAAgMBAAAAAAAAAAAAAAAAAQMAAgQF/8QAJRABAAIBBAEEAgMAAAAAAAAAAQIRAAMSITEEEyJBgTORUWFx/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AOgM52xQDrjvAV5Xv0vfKUALlTQfeBm0HThMNHXkL0Lw/swN5qgA8yT4MCS1OEOJV8mBz9Z05yfW8iSx7p4j+jA1aD6Wj7ZMzstsfvAas4UyRHvjrAkC9KhpLMClQntlqFc2X1gUj4viwVObKrddH9YDoHvuujAEuNV+bLwFS8XxdSr+Cq3Vf+4F5RgQl6ZR2p1eAzU/HX80YBYyJLCuexwJCO2O1bwCRidAfWBSctswbI12GAJT3yiwFR7+MBjGK2g/WAJR3FdF84E2rK5VR0YH/9k="

@app.route('/bilde')
def show_bilde():
    return render_template("bilde.html", bildeadresse=dataURI)


@app.route('/blokktest')
def show_blokktest():
    return render_template("blokktest.html")


