# ===== Блюпринт index view =====#

import logging
import app_logger
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from configs.config import DATA_PATH, COMMENTS_PATH, BOOKMARKS_PATH, LOG_PATH
from utils import comment_word_correction_by_count, get_tags_from_content
from dao import PageManager, BookmarksManager, CommentsManager

# Регистрация блюпринта index view
index_blueprint = Blueprint("index_blueprint", __name__, template_folder="templates")

# Включение логирования
logger = app_logger.get_logger(__name__)

# Загрузка данных для блюпринта
page_manager = PageManager(DATA_PATH)
bookmarks_manager = BookmarksManager(BOOKMARKS_PATH)
comments_manager = CommentsManager(COMMENTS_PATH)

# ===== Роуты=====#
@index_blueprint.route("/", methods=["GET", "POST"])
def render_index_page():
    """Рендер главной страницы"""
    data = page_manager.get_data()
    bookmarks = bookmarks_manager.get_data()
    count_comments = comments_manager.count_comments(data)
    if request.method == "POST":
        bookmarks_manager.request_add(request.form.get("bookmark_add"))
        bookmarks_manager.request_del(request.form.get("bookmark_del"))
        return redirect(url_for("index_blueprint.render_index_page"))
    elif request.method == "GET":
        logger.info("Open index page")
        return render_template("index.html", data=data, count_comments=count_comments,
                               comment_word_correction_by_count=comment_word_correction_by_count,
                               get_tags_from_content=get_tags_from_content, bookmarks_count=len(bookmarks),
                               bookmarks=bookmarks)


@index_blueprint.route("/user/<poster_name>", methods=["GET", "POST"])
def render_poster_page(poster_name):
    """Рендер страницы по имени пользователя"""
    data = page_manager.get_data_for_user_page(poster_name)
    bookmarks = bookmarks_manager.get_data()
    count_comments = comments_manager.count_comments(data)
    if request.method == "POST":
        bookmarks_manager.request_add(request.form.get("bookmark_add"))
        bookmarks_manager.request_del(request.form.get("bookmark_del"))
        return redirect(url_for("index_blueprint.render_poster_page", poster_name=poster_name))
    elif request.method == "GET":
        logger.info(f"Open {poster_name} page")
        return render_template("user_page.html", data=data, count_comments=count_comments,
                               comment_word_correction_by_count=comment_word_correction_by_count,
                               poster_name=poster_name, get_tags_from_content=get_tags_from_content,
                               bookmarks_count=len(bookmarks), bookmarks=bookmarks)
