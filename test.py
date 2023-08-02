# -*- coding: utf-8 -*-
try:
    import sys
    # add your project directory to the sys.path
    project_home = "F:\\users\\magdalon\\Dropbox\\Documents\\Python\\mysite\\"
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path
except Exception:
    pass
from flask_app import app
import pytest

client = app.test_client()
responses = []
ignores = []

for rule in app.url_map.iter_rules():
    if not rule.arguments:
        res = client.get(rule.rule)
        responses.append(res)
    else:
        ignores.append(rule)

from pprint import pprint

pprint(responses)
pprint([resp.status_code for resp in responses])
errors = [resp for resp in responses if resp.status_code != 200]
for err in errors:
    print(err.request, err)

def test_ok():
    assert res.status_code == 200


def test_me():
    assert 1 == 1
"""
def test_you():
    assert 2 + 2 == 5
"""
regler = [regel for regel in app.url_map.iter_rules() if not regel.arguments]
@pytest.mark.parametrize("regel",
    regler)

def test_regel(regel):
    resp = client.get(regel.rule)
    assert resp.status_code == 200
