import os
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape

SRC_DIR = os.path.join(os.path.dirname(__file__), "live")
DST_DIR = os.path.join(os.path.dirname(__file__), "live_build")


def build_static_site():
    # 1. Очистить/создать папку назначения
    if os.path.exists(DST_DIR):
        shutil.rmtree(DST_DIR)
    os.makedirs(DST_DIR, exist_ok=True)

    # 2. Копировать ассеты (assets/) как есть
    assets_src = os.path.join(SRC_DIR, "assets")
    assets_dst = os.path.join(DST_DIR, "assets")
    if os.path.exists(assets_src):
        shutil.copytree(assets_src, assets_dst)

    # 3. Настроить Jinja2
    env = Environment(
        loader=FileSystemLoader(SRC_DIR),
        autoescape=select_autoescape(['html', 'xml'])
    )

    # 4. Список "partials" (блоки, которые не рендерим как страницы)
    partials = {
        "header.html", "footer.html", "scripts.html", "head.html",
        "portfolio_card.html", "portfolio_cards_block.html", "chatbot_widget.html"
    }

    # 5. Для главной страницы — передаём список карточек портфолио
    portfolio_cards = [
        {
            "category": "patients",
            "url": "portfolio_patient_compensation.html",
            "image": "assets/images/work-1.jpg",
            "alt": "Дело пациента",
            "title": "Взыскание компенсации за некачественное лечение",
            "descr": "Пациентам"
        },
        {
            "category": "institutions",
            "url": "portfolio_osp_otkaza.html",
            "image": "assets/images/work-2.jpg",
            "alt": "Дело с мед. учреждением",
            "title": "Оспаривание отказа в предоставлении медицинской помощи",
            "descr": "Мед. учреждения"
        },
        {
            "category": "doctors",
            "url": "portfolio_doctor_defense.html",
            "image": "assets/images/work-3.jpg",
            "alt": "Дело врача",
            "title": "Защита врача при дисциплинарном разбирательстве",
            "descr": "Врачам"
        },
        {
            "category": "patients",
            "url": "portfolio_patient_moral.html",
            "image": "assets/images/work-4.jpg",
            "alt": "Дело пациента",
            "title": "Взыскание морального вреда",
            "descr": "Пациентам"
        },
        {
            "category": "institutions",
            "url": "portfolio_soprovod_s_chstnoi.html",
            "image": "assets/images/work-5.jpg",
            "alt": "Дело с мед. учреждением",
            "title": "Сопровождение спора с частной клиникой",
            "descr": "Мед. учреждения"
        },
        {
            "category": "doctors",
            "url": "portfolio_doctor_consult.html",
            "image": "assets/images/work-6.jpg",
            "alt": "Дело врача",
            "title": "Консультация врача по вопросам медицинского права",
            "descr": "Врачам"
        }
    ]

    # 6. Найти все .html файлы (кроме ассетов и partials)
    for root, dirs, files in os.walk(SRC_DIR):
        rel_root = os.path.relpath(root, SRC_DIR)
        for file in files:
            if file.endswith(".html") and file not in partials:
                src_path = os.path.join(root, file)
                rel_path = os.path.join(rel_root, file) if rel_root != "." else file
                dst_path = os.path.join(DST_DIR, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                # Рендерим шаблон
                template_path = os.path.relpath(src_path, SRC_DIR)
                template = env.get_template(template_path)
                # Для главной страницы — передаём карточки портфолио
                if file == "index_mp_fullscreen_flexslider.html":
                    rendered = template.render(portfolio_cards=portfolio_cards)
                else:
                    rendered = template.render()
                with open(dst_path, "w", encoding="utf-8") as f:
                    f.write(rendered)
    # Переименовать index_mp_fullscreen_flexslider.html в index.html
    src_index = os.path.join(DST_DIR, "index_mp_fullscreen_flexslider.html")
    dst_index = os.path.join(DST_DIR, "index.html")
    if os.path.exists(src_index):
        os.replace(src_index, dst_index)
    print(f"Статический сайт собран в папке: {DST_DIR}")


if __name__ == "__main__":
    build_static_site()
