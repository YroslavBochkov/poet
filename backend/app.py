from flask import Flask, send_from_directory, abort
from flask_cors import CORS
import os

# Определяем путь к папке с html-файлами (live)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIVE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../live"))

app = Flask(__name__, static_folder=LIVE_DIR, template_folder=LIVE_DIR)
CORS(app)

# Главная страница
@app.route("/")
def index():
    return send_from_directory(app.template_folder, "index_mp_fullscreen_flexslider.html")

# Любая страница вида /about, /portfolio, /portfolio_osp_otkaza и т.д.
@app.route("/<page>")
def render_pretty_page(page):
    filename = f"{page}.html"
    file_path = os.path.join(app.template_folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.template_folder, filename)
    return abort(404)

# Старый маршрут с .html (по желанию)
@app.route("/<page>.html")
def render_page(page):
    filename = f"{page}.html"
    file_path = os.path.join(app.template_folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.template_folder, filename)
    return abort(404)

# Отдача ассетов (css, js, images)
@app.route('/assets/<path:filename>')
def assets(filename):
    assets_dir = os.path.join(app.template_folder, 'assets')
    return send_from_directory(assets_dir, filename)

# Кастомная 404 страница
@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory(app.template_folder, "404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
