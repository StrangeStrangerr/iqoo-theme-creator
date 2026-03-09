# iQOO/Vivo Icon Patcher (OriginOS Research)

### 🇬🇧 English Description
**Status: Experimental / Not working on latest OriginOS**

This project was an attempt to automate the process of replacing system icons on iQOO/Vivo devices (specifically iQOO Neo 10) by patching the `.itz` theme format. 

**What was done:**
* **Reverse Engineering:** Analyzed the internal structure of the `.itz` container (ZIP-based).jpg].
* **Automation:** Developed a Python script to inject custom icons into existing theme templates.
* **ADB Research:** Attempted to bypass system restrictions using `adb shell` to find hidden theme directories (`.dwd`, `.vvtheme`).
* **Intent Injection:** Tried to force the `com.bbk.theme` app to import files via Activity management (`am start`).

**Conclusion:**
On newer versions of OriginOS (Android 14/15), the `iTheme` app is heavily sandboxed. Attempts to launch import activities resulted in `Permission Denial` (requires `ACCESS_THEME` permission), and the app's data folders are restricted even from ADB `find` commands. This repository serves as a documentation of the research process.

---

### 🇷🇺 Описание на русском
**Статус: Экспериментальный / Не работает на новых версиях OriginOS**

Этот проект — попытка автоматизировать замену системных иконок на устройствах iQOO/Vivo (в частности iQOO Neo 10) через модификацию файлов тем формата `.itz`.

**Что было сделано:**
* **Реверс-инжиниринг:** Изучена внутренняя структура контейнера `.itz` (на базе ZIP).jpg].
* **Автоматизация:** Написан Python-скрипт для «инъекции» кастомных иконок в шаблоны тем.
* **Исследование через ADB:** Предприняты попытки найти скрытые директории тем (`.dwd`, `.vvtheme`) и обойти системные ограничения.
* **Работа с Intent:** Попытки принудительно запустить импорт в приложении `com.bbk.theme` через менеджер активностей (`am start`).

**Итог:**
На свежих версиях OriginOS (Android 14/15) приложение «Темы» полностью изолировано. Попытки запуска окон импорта вызывают ошибку `Permission Denial` (требуется системное разрешение `ACCESS_THEME`), а папки данных приложения скрыты даже от команд ADB `find`. Репозиторий сохранен как история исследования системы.