from flask import Flask, render_template, abort, send_from_directory
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIVE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../live"))

app = Flask(__name__, static_folder=LIVE_DIR, template_folder=LIVE_DIR)

@app.route("/")
def index():
    return render_template("index_mp_fullscreen_flexslider.html")

@app.route("/<page>")
def render_pretty_page(page):
    filename = f"{page}.html"
    file_path = os.path.join(app.template_folder, filename)
    if os.path.exists(file_path):
        return render_template(filename)
    return abort(404)

@app.route("/<page>.html")
def render_page(page):
    filename = f"{page}.html"
    file_path = os.path.join(app.template_folder, filename)
    if os.path.exists(file_path):
        return render_template(filename)
    return abort(404)

@app.route('/assets/<path:filename>')
def assets(filename):
    assets_dir = os.path.join(app.template_folder, 'assets')
    return send_from_directory(assets_dir, filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
