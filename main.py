import subprocess

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


@app.route("/")
def mainpage():
    opening_cs = subprocess.run(['lsof', '-i', ':27015'], stdout=subprocess.PIPE)
    sv_status = 'CLOSED' if len(opening_cs.stdout) == 0 else 'ACTIVE'

    return render_template('main.html', sv_status=sv_status)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=30000, debug=True)
