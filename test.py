# -*- coding: utf-8 -*-
from flask_app import app
import pytest

client = app.test_client()
responses = []
ignores = []

for rule in app.url_map.iter_rules():
    if not rule.arguments:
        responses.append(client.get(rule.rule))
    else:
        ignores.append(rule)

from pprint import pprint

pprint(responses)
pprint([resp.status_code for resp in responses])
errors = [resp for resp in responses if resp.status_code != 200]
for err in errors:
    print(err.request, err)
