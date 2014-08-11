__author__ = 'ehonlia'

import inspect
from flask import Flask, url_for, render_template

from app.semantic_adapter import semantic_adapter
from app.semantic_adapter_citypulse import semantic_adapter_citypulse

app = Flask(__name__)
app.register_blueprint(semantic_adapter)
app.register_blueprint(semantic_adapter_citypulse, url_prefix='/citypulse')


@app.route('/')
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # not static and not site_map
        if rule.endpoint not in ['static', inspect.stack()[0][3]] and rule.endpoint.find('citypulse') == -1:
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template('index.html', links=links)
