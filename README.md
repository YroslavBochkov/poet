# Адвокат Садиков А.А. — Юридическая помощь пациентам и врачам

Веб-проект для адвокатского кабинета Садикова Алексея Анатольевича. Сайт предоставляет информацию об услугах, портфолио дел, контактные данные, а также содержит интерактивный юридический чат-бот для первичных консультаций.

[![Netlify Status](https://api.netlify.com/api/v1/badges/c2669144-3378-4eaf-a5da-44301a916167/deploy-status)](https://app.netlify.com/projects/melodic-semolina-db5a49/deploys)

## Структура проекта

- `live/` — фронтенд (HTML-шаблоны, стили, скрипты, изображения)
- `backend/` — серверная часть на Python (Flask)
- `.env` — переменные окружения (секреты, SMTP и др.)
- `.gitignore` — исключения для git

## Основные возможности

- Современный адаптивный сайт с разделами:
  - О нас
  - Услуги для пациентов, врачей, мед. учреждений
  - Портфолио (примеры дел)
  - Контакты с картой и формой связи
- Интерактивный чат-бот для юридических консультаций (на Flask, сценарии в `backend/dialog_scenarios.json`)
- Фильтрация портфолио по категориям
- Анимации, слайдеры, плавная навигация

## Быстрый старт (локально)

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repo_url>
   cd poet
   ```


## Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
Установите зависимости:


pip install -r requirements.txt
Настройте переменные окружения:
```


```bash
cd backend
python app.py
```

## Откройте сайт:

Перейдите в браузере по адресу  http://127.0.0.1:5000

Работает на Flask, сценарии — в JSON.

Виджет подключается через {% include "chatbot_widget.html" %}.

Для сброса состояния чата используется /chatbot_reset.

## Развёртывание

Для продакшена рекомендуется запускать через WSGI (gunicorn, uwsgi) и использовать nginx для отдачи статики.


## Стек технологий

<a href="https://www.python.org/"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="32" alt="Python"/></a>
<a href="https://flask.palletsprojects.com/"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" height="32" alt="Flask"/></a>
<a href="https://developer.mozilla.org/docs/Web/HTML"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height="32" alt="HTML5"/></a>
<a href="https://developer.mozilla.org/docs/Web/CSS"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" height="32" alt="CSS3"/></a>
<a href="https://developer.mozilla.org/docs/Web/JavaScript"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" height="32" alt="JavaScript"/></a>
<a href="https://getbootstrap.com/"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" height="32" alt="Bootstrap"/></a>
<a href="https://jquery.com/"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jquery/jquery-original.svg" height="32" alt="jQuery"/></a>
<a href="https://git-scm.com/"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" height="32" alt="Git"/></a>


Не забудьте защитить .env и другие чувствительные файлы.

**Автор:** [Ярослав Бочков](https://github.com/YroslavBochkov)