# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:30:12 2023

@author: magdalon
"""

from flask_app import app
from werkzeug.serving import run_simple
if __name__ == '__main__':
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=False, use_evalex=True)
