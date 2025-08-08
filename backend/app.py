import json
import os

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
    send_from_directory,
    session,
)

# Загрузка переменных окружения
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIVE_DIR = os.path.abspath(os.path.join(BASE_DIR, "../live"))

app = Flask(
    __name__,
    static_folder=LIVE_DIR,
    template_folder=LIVE_DIR,
)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")  # Для работы сессий

# Загрузка сценариев из JSON-файла
with open(
    os.path.join(BASE_DIR, "dialog_scenarios.json"),
    "r",
    encoding="utf-8",
) as f:
    dialog_data = json.load(f)

LEGAL_TOPICS = dialog_data["LEGAL_TOPICS"]
DIALOG_SCENARIOS = dialog_data["DIALOG_SCENARIOS"]
FALLBACK = dialog_data.get(
    "FALLBACK",
    (
        "Извините, я не смог распознать ваш вопрос. "
        "Могу предложить записаться на консультацию или оставить ваш телефон/email "
        "для связи с юристом."
    ),
)


@app.route("/chatbot_reset", methods=["POST"])
def chatbot_reset():
    session.clear()
    return "", 204


@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "").lower()
    dialog_state = session.get("dialog_state", {})

    # Первый шаг: выбор типа пользователя
    if not dialog_state:
        options = ["Пациент", "Врач", "Медицинское учреждение"]
        session["dialog_state"] = {"step": "choose_role"}
        return jsonify(
            {
                "response": "Здравствуйте! Выберите, кто вы:",
                "options": options,
            }
        )

    # Обработка выбора роли
    if dialog_state.get("step") == "choose_role":
        if "пациент" in user_message:
            session["dialog_state"] = {"role": "пациент", "step": "choose_topic"}
            topics = list(LEGAL_TOPICS["пациентам"].keys())
            return jsonify(
                {
                    "response": "Выберите ваш вопрос:",
                    "options": topics,
                }
            )
        elif "врач" in user_message:
            session["dialog_state"] = {"role": "врач", "step": "choose_topic"}
            topics = list(LEGAL_TOPICS.get("врачам", {}).keys())
            return jsonify(
                {
                    "response": "Выберите ваш вопрос:",
                    "options": topics,
                }
            )
        elif (
            "медицинское учреждение" in user_message
            or "учреждение" in user_message
        ):
            session["dialog_state"] = {
                "role": "медицинское учреждение",
                "step": "choose_topic",
            }
            topics = list(LEGAL_TOPICS.get("медицинским учреждениям", {}).keys())
            return jsonify(
                {
                    "response": "Выберите ваш вопрос:",
                    "options": topics,
                }
            )
        else:
            return jsonify(
                {
                    "response": "Пожалуйста, выберите одну из ролей:",
                    "options": [
                        "Пациент",
                        "Врач",
                        "Медицинское учреждение",
                    ],
                }
            )

    # Обработка выбора темы
    if dialog_state.get("step") == "choose_topic":
        role = dialog_state.get("role")
        topics = (
            LEGAL_TOPICS.get(f"{role}ам", {})
            if role != "медицинское учреждение"
            else LEGAL_TOPICS.get("медицинским учреждениям", {})
        )
        for subtopic, answer in topics.items():
            if subtopic in user_message:
                session["dialog_state"] = {
                    "last_topic": subtopic,
                    "step": 0,
                    "role": role,
                }
                scenario = DIALOG_SCENARIOS.get(subtopic)
                if scenario:
                    resp = scenario[0]
                    return jsonify(
                        {
                            "response": answer + " " + resp.get("q"),
                            "options": resp.get("options"),
                        }
                    )
                return jsonify({"response": answer})
        # Если не найдено — повторить выбор
        return jsonify(
            {
                "response": "Пожалуйста, выберите тему из списка:",
                "options": list(topics.keys()),
            }
        )

    # Если ожидается уточнение по подтеме (многошаговый сценарий с кнопками)
    if "last_topic" in dialog_state:
        last_topic = dialog_state["last_topic"]
        scenario = DIALOG_SCENARIOS.get(last_topic)
        if scenario:
            step = dialog_state.get("step", 0)
            options = scenario[step].get("options")
            # Если выбрана опция "Спасибо, не нужно" — прощаемся и закрываем чат
            if options and any(
                opt.lower() in user_message for opt in [o.lower() for o in options]
            ):
                if "спасибо, не нужно" in user_message:
                    session["dialog_state"] = {}
                    return jsonify(
                        {
                            "response": (
                                "Спасибо за обращение! Если появятся вопросы — "
                                "всегда рад помочь. Всего доброго!"
                            ),
                            "close_chat": True,
                        }
                    )
                step = min(step + 1, len(scenario) - 1)
                session["dialog_state"] = {**dialog_state, "step": step}
                resp = scenario[step]
                return jsonify(
                    {
                        "response": resp.get("a", resp.get("q")),
                        "options": resp.get("options"),
                    }
                )
            if any(
                word in user_message
                for word in ["да", "хочу", "интересует", "подробнее", "конечно"]
            ):
                step = min(step + 1, len(scenario) - 1)
                session["dialog_state"] = {**dialog_state, "step": step}
                resp = scenario[step]
                return jsonify(
                    {
                        "response": resp.get("a", resp.get("q")),
                        "options": resp.get("options"),
                    }
                )
            if "нет" in user_message:
                session["dialog_state"] = {}
                return jsonify(
                    {
                        "response": (
                            "Спасибо за обращение! Если появятся вопросы — "
                            "всегда рад помочь. Всего доброго!"
                        ),
                        "close_chat": True,
                    }
                )
            if (
                "@" in user_message
                or "тел" in user_message
                or "номер" in user_message
                or user_message.replace(" ", "").isdigit()
            ):
                session["dialog_state"] = {}
                return jsonify(
                    {
                        "response": (
                            "Если вы хотите записаться на консультацию, пожалуйста, "
                            "позвоните по телефону +7 (917) 834-50-17 или напишите в "
                            "WhatsApp/Telegram. Мы не собираем и не храним ваши контакты."
                        )
                    }
                )
            resp = scenario[step]
            session["dialog_state"] = {**dialog_state, "step": step}
            return jsonify(
                {"response": resp.get("q"), "options": resp.get("options")}
            )

    # Если пользователь оставил контакт вне сценария
    if (
        "@" in user_message
        or "тел" in user_message
        or "номер" in user_message
        or user_message.replace(" ", "").isdigit()
    ):
        session["dialog_state"] = {}
        return jsonify(
            {
                "response": (
                    "Если вы хотите записаться на консультацию, пожалуйста, "
                    "позвоните по телефону +7 (917) 834-50-17 или напишите в "
                    "WhatsApp/Telegram. Мы не собираем и не храним ваши контакты."
                )
            }
        )

    # Если не распознано
    return jsonify({"response": FALLBACK})


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


@app.route("/assets/<path:filename>")
def assets(filename):
    assets_dir = os.path.join(app.template_folder, "assets")
    return send_from_directory(assets_dir, filename)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# if __name__ == "__main__":
    # app.run(debug=False)
