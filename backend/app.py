from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

# Определяем путь к папке с html-файлами (live)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIVE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../live"))

app = Flask(__name__, static_folder=LIVE_DIR, template_folder=LIVE_DIR)
CORS(app)

about = {
    "title": "We’re a digital creative agency",
    "description": [
        "The European languages are members of the same family. Their separate existence is a myth. For science, music, sport, etc, Europe uses the same vocabulary. The languages only differ in their grammar, their pronunciation and their most common words.",
        "The European languages are members of the same family. Their separate existence is a myth. For science, music, sport, etc, Europe uses the same vocabulary."
    ]
}

team = [
    {
        "name": "Jim Stone",
        "role": "Art Director",
        "photo": "assets/images/team-1.jpg",
        "greeting": "Hi all",
        "about": "Lorem ipsum dolor sit amet, consectetur adipiscing elit lacus, a iaculis diam.",
        "social": {
            "facebook": "#",
            "twitter": "#",
            "dribbble": "#",
            "skype": "#"
        }
    },
    {
        "name": "Andy River",
        "role": "Creative director",
        "photo": "assets/images/team-2.jpg",
        "greeting": "Good day",
        "about": "Lorem ipsum dolor sit amet, consectetur adipiscing elit lacus, a iaculis diam.",
        "social": {
            "facebook": "#",
            "twitter": "#",
            "dribbble": "#",
            "skype": "#"
        }
    },
    {
        "name": "Adele Snow",
        "role": "Account manager",
        "photo": "assets/images/team-3.jpg",
        "greeting": "Hello",
        "about": "Lorem ipsum dolor sit amet, consectetur adipiscing elit lacus, a iaculis diam.",
        "social": {
            "facebook": "#",
            "twitter": "#",
            "dribbble": "#",
            "skype": "#"
        }
    },
    {
        "name": "Dylan Woods",
        "role": "Developer",
        "photo": "assets/images/team-4.jpg",
        "greeting": "Yes, it's me",
        "about": "Lorem ipsum dolor sit amet, consectetur adipiscing elit lacus, a iaculis diam.",
        "social": {
            "facebook": "#",
            "twitter": "#",
            "dribbble": "#",
            "skype": "#"
        }
    }
]

advantages = [
    {
        "icon": "icon-lightbulb",
        "title": "Ideas and concepts",
        "desc": "Careful attention to detail and clean, well structured code ensures a smooth user experience for all your visitors."
    },
    {
        "icon": "icon-bike",
        "title": "Optimised for speed",
        "desc": "Careful attention to detail and clean, well structured code ensures a smooth user experience for all your visitors."
    },
    {
        "icon": "icon-tools",
        "title": "Designs & interfaces",
        "desc": "Careful attention to detail and clean, well structured code ensures a smooth user experience for all your visitors."
    },
    {
        "icon": "icon-gears",
        "title": "Highly customizable",
        "desc": "Careful attention to detail and clean, well structured code ensures a smooth user experience for all your visitors."
    }
]

# API endpoints
@app.route("/api/about")
def get_about():
    return jsonify(about)

@app.route("/api/team")
def get_team():
    return jsonify(team)

@app.route("/api/advantages")
def get_advantages():
    return jsonify(advantages)

# Главная страница (about1.html)
@app.route("/")
def index():
    return send_from_directory(app.template_folder, "index_mp_fullscreen_flexslider.html")

# Любая страница вида /about2.html, /about3.html и т.д.
# Красивые адреса: /about1, /about2, /portfolio, и т.д.
@app.route("/<page>")
def render_pretty_page(page):
    filename = f"{page}.html"
    file_path = os.path.join(app.template_folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.template_folder, filename)
    return "Page not found", 404

# Старый маршрут с .html оставляем для обратной совместимости (по желанию)
@app.route("/<page>.html")
def render_page(page):
    filename = f"{page}.html"
    file_path = os.path.join(app.template_folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.template_folder, filename)
    return "Page not found", 404

# Отдача ассетов (css, js, images)
@app.route('/assets/<path:filename>')
def assets(filename):
    assets_dir = os.path.join(app.template_folder, 'assets')
    return send_from_directory(assets_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
