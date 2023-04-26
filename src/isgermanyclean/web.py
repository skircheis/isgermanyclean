from flask import Flask, request, render_template, send_from_directory
from flask_assets import Environment, Bundle
from pandas import Timestamp
from pathlib import Path

from .report import load_report
from .utils import get_data_dir, get_db


data_dir = get_data_dir()
static_dir = data_dir / ".webstatic"

app = Flask(__name__)
assets = Environment(app)
assets.url = "assets"
assets.directory = str(static_dir)
css = Bundle("style.sass", filters="sass", output="style.css")
assets.register("css", css)

images = Bundle("npyesplease.png")
assets.register("images", images)


def log_visit():
    from time import time

    ts = int(time())
    ip = request.access_route[0] or request.remote_addr
    referrer = request.headers.get("Referer")
    ua = request.headers.get("User-Agent")

    with get_db() as db:
        cur = db.cursor()
        cur.execute(
            "INSERT INTO visits (timestamp, ip, referrer, user_agent) VALUES(?, ?, ?, ?)",
            (ts, ip, referrer, ua),
        )


def get_unique_hits():
    with get_db() as db:
        cur = db.cursor()
        cur.execute(
            "SELECT COUNT(DISTINCT ip) as unique_hits, MIN(timestamp) as earliest FROM visits"
        )
        row = cur.fetchone()
        if row is None:
            from time import time
            row = (0, time())
        from datetime import datetime
        dt = datetime.fromtimestamp(row[1])
        return (row[0], dt.strftime("%Y-%m-%d"))


@app.route("/")
def index():
    log_visit()
    unique_hits = get_unique_hits()
    report = load_report("report.json")
    report["plot_fname"] = "/assets/" + report["plot_fname"]
    today = Timestamp.today().floor("1D").tz_localize("Europe/Brussels")
    report["from_today"] = Timestamp(report["date"]).day_of_year == today.day_of_year
    return render_template("index.html", report=report, unique_hits=unique_hits)


@app.route("/assets/<path:path>")
def send_static(path):
    return send_from_directory(str(get_data_dir() / ".webstatic"), path)


@app.route("/favicon.ico")
def send_favicon():
    return send_from_directory(str(get_data_dir() / ".webstatic"), "favicon.ico")


def launch_server(opts):
    app.run(host=opts.host, port=opts.port, debug=opts.debug)
