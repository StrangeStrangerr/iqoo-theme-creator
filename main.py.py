import zipfile
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

# --- НАСТРОЙКИ ---
XML_FILE = "appfilter.xml"         # Файл с картой иконок
ICONS_DIR = "icons_png"            # Папка, где лежат все 1000+ иконок из APK
OUTPUT_DIR = "ready_for_iqoo"      # Сюда скрипт сложит готовые иконки

# Создаем выходную папку, если ее нет, или очищаем старую
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)

def get_installed_packages():
    print("[1/3] Опрашиваю телефон через ADB...")
    try:
        # Команда ADB для получения списка пакетов
        result = subprocess.run(["adb", "shell", "pm", "list", "packages"],
                                capture_output=True, text=True, check=True)
        # Очищаем вывод: "package:com.whatsapp" -> "com.whatsapp"
        packages = [line.replace("package:", "").strip() for line in result.stdout.split('\n') if line]
        print(f"  -> Найдено {len(packages)} установленных приложений.")
        return packages
    except FileNotFoundError:
        print("ОШИБКА: Файл adb.exe не найден в папке со скриптом!")
        return []
    except subprocess.CalledProcessError:
        print("ОШИБКА: Телефон не подключен или не разрешена отладка по USB!")
        return []

def match_and_copy_icons(installed_packages):
    print("[2/3] Читаю appfilter.xml и ищу совпадения...")
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    matched_count = 0

    for item in root.findall('item'):
        component = item.get('component')
        drawable = item.get('drawable')

        if component and drawable:
            # Достаем имя пакета. Пример: ComponentInfo{com.vkontakte.android/com.vk.Main} -> com.vkontakte.android
            try:
                pkg_name = component.split('{')[1].split('/')[0]
            except IndexError:
                continue

            # Если это приложение есть на твоем телефоне
            if pkg_name in installed_packages:
                source_image = os.path.join(ICONS_DIR, f"{drawable}.png")
                # Для Vivo/iQOO иконки должны называться как имя пакета (com.vkontakte.android.png)
                dest_image = os.path.join(OUTPUT_DIR, f"{pkg_name}.png")

                if os.path.exists(source_image):
                    shutil.copy(source_image, dest_image)
                    matched_count += 1

    print(f"  -> Успешно подобрано {matched_count} иконок для твоих приложений.")

# Запуск
packages = get_installed_packages()
if packages:
    match_and_copy_icons(packages)
    print(f"[3/3] ГОТОВО! Забирай иконки из папки '{OUTPUT_DIR}'")

def update_theme_with_icons(template_path, icons_src):
    # .itz — это обычный zip. Открываем его для добавления файлов.
    with zipfile.ZipFile(template_path, 'a') as archive:
        for icon_file in os.listdir(icons_src):
            full_path = os.path.join(icons_src, icon_file)
            # Внутри темы иконки обычно лежат в папке icons/ и без расширения .png
            internal_name = f"icons/{icon_file.replace('.png', '')}"
            archive.write(full_path, internal_name)
    print("Иконки успешно интегрированы в template.itz!")

# Вызывай эту функцию после того, как папка ready_for_iqoo будет готова
update_theme_with_icons('template.itz', 'ready_for_iqoo')
