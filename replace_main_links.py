import os

# Папка, где лежат все шаблоны и html-файлы
TEMPLATE_DIR = "live"

# Что ищем и на что меняем
old = "index_mp_fullscreen_flexslider.html"
new = "index.html"

for root, dirs, files in os.walk(TEMPLATE_DIR):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if old in content:
                content = content.replace(old, new)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Заменено в: {path}")
print("Готово!")
