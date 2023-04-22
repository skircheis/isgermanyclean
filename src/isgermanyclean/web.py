from flask import Flask, render_template, send_from_directory
from flask_assets import Environment, Bundle
from pandas import Timestamp
from pathlib import Path

from .report import load_report
from .utils import get_data_dir, today


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

@app.route("/")
def index():
    report = load_report("report.json")
    report["plot_fname"] = "/assets/" + report["plot_fname"]
    print(today)
    print(Timestamp(report["date"]))
    report["from_today"] = Timestamp(report["date"]).day_of_year == today.day_of_year
    return render_template("index.html", report=report)

@app.route("/assets/<path:path>")
def send_static(path):
    return send_from_directory(str(get_data_dir() / ".webstatic"), path)

@app.route("/favicon.ico")
def send_favicon():
    return send_from_directory(str(get_data_dir() / ".webstatic"), "favicon.ico")

def launch_server(opts):
    app.run(host=opts.host, port=opts.port, debug=opts.debug)
