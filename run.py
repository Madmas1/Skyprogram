# ===== Run модуль приложения =====#

import json
import exceptions
import app_logger

from flask import Flask, send_from_directory, render_template

import sys

from index.views import index_blueprint
from post.views import post_blueprint
from search.views import search_blueprint
from tags.views import tags_blueprint
from bookmarks.views import bookmarks_blueprint
from API.views import api_blueprint

# Подключение фреймворка приложения
app = Flask(__name__)

# Конфигурирование JSON для приложения
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Включаем логгирование
logger = app_logger.get_logger(__name__)

# Регистрация блюпринтов представлений
app.register_blueprint(index_blueprint)
app.register_blueprint(post_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(tags_blueprint)
app.register_blueprint(bookmarks_blueprint)
app.register_blueprint(api_blueprint)

# Роуты на выгрузку статического контента
@app.route("/img/<path:path>")
def static_img_dir(path):
    return send_from_directory("static/img", path)

@app.route("/css/<path:path>")
def static_css_dir(path):
    return send_from_directory("static/css", path)

# Обработкчики ошибок
@app.errorhandler(404)
def code_404(error):
    logger.error("Trying to open a page that does not exist")
    return render_template("404.html"), 404

@app.errorhandler(500)
def code_500(error):
    logger.error("The server was unable to process the request")
    return render_template("404.html", data="Внутряння ошибка сервера"), 500


@app.errorhandler(FileNotFoundError)
def file_nof_found_error_handler(error):
    return render_template("404.html", data='Отсуствует JSON файл c данными'), 400

@app.errorhandler(json.JSONDecodeError)
def load_json_file_error_handler(error):
    return render_template("404.html", data='Не удалось JSON файл c данными'), 500

@app.errorhandler(exceptions.PostNotFound)
def post_error_handler(error):
    return render_template("404.html", data='Пост не найден'), 500

@app.errorhandler(exceptions.UserNotFound)
def post_error_handler(error):
    return render_template("404.html", data='Страницы с таким пользователем не сущестует'), 500


if __name__ == '__main__':
    app.run()


