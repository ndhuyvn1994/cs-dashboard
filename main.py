import subprocess

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


@app.route("/")
def mainpage():
    ports = [':27015', ':27016', ':27017', ':27018', ':27019']
    for p in ports:
        opening_cs = subprocess.run(['lsof', '-i', p], stdout=subprocess.PIPE)
        sv_status = 'CLOSED' if len(opening_cs.stdout) == 0 else 'ACTIVE'

        if sv_status == 'ACTIVE':
            break

    return render_template('main.html', sv_status=sv_status, port=p)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=30000, debug=True)
