from flask import Flask, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import render_template

import subprocess

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/")
def mainpage():
    opening_cs = subprocess.run(['lsof', '-i', ':27015'], stdout=subprocess.PIPE)
    sv_status = 'CLOSED' if len(opening_cs.stdout) == 0 else 'ACTIVE'

    return render_template('main.html', sv_status=sv_status)
