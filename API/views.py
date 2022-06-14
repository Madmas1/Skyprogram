# ===== Блюпринт API view =====#

import logging
import app_logger
from flask import Blueprint, jsonify
from configs.config import DATA_PATH
from dao import PageManager

# Регистрация блюпринта API view
api_blueprint = Blueprint("api_blueprint", __name__, template_folder="templates")

# Включение логирования
logger = app_logger.get_logger(__name__)

# Загрузка данных для блюпринта
page_manager = PageManager(DATA_PATH)


# ===== Роуты =====#
@api_blueprint.route("/API/posts", methods=["GET"])
def get_api_posts():
    """Рендер API со всеми постами"""
    logging.info("API posts request")
    data = page_manager.get_data()
    return jsonify(data)

    # Альтернативный вывод JSON без jsonify и конфигов для flask
    # return json.dumps(data, ensure_ascii=False, indent=4), {"Content-Type": "application/json"}


@api_blueprint.route("/API/posts/<int:post_id>", methods=["GET"])
def get_api_posts_by_id(post_id):
    """Рендер API по номеру поста"""
    logging.info(f"API post № {post_id} request")
    data = page_manager.get_post_page_data(post_id)
    return jsonify(data)

    # Альтернативный вывод JSON без jsonify и конфигов для flask
    # return json.dumps(data, ensure_ascii=False, indent=4),
