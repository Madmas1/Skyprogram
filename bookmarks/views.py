# ===== Блюпринт bookmarks view =====#
import app_logger
from flask import Blueprint, render_template, request, redirect, url_for
from configs.config import DATA_PATH, BOOKMARKS_PATH, COMMENTS_PATH
from dao import CommentsManager, BookmarksManager, PageManager
from utils import comment_word_correction_by_count, get_tags_from_content

# Подключаем блюпринт для bookmarks view
bookmarks_blueprint = Blueprint("bookmarks_blueprint", __name__, template_folder="templates")

# Включаем логирование
logger = app_logger.get_logger(__name__)

# Загрузка данных для блюпринта
page_manager = PageManager(DATA_PATH)
bookmarks_manager = BookmarksManager(BOOKMARKS_PATH)
comments_manager = CommentsManager(COMMENTS_PATH)


# ===== Роуты =====#
@bookmarks_blueprint.route("/bookmarks", methods=["GET", "POST"])
def render_bookmarks_page():
    """Рендер страницы с закладками"""
    bookmarks = bookmarks_manager.get_data()
    data = page_manager.get_bookmarks_page_data(bookmarks)
    count_comments = comments_manager.count_comments(data)
    if request.method == "POST":
        bookmarks_manager.request_add(request.form.get("bookmark_add"))
        bookmarks_manager.request_del(request.form.get("bookmark_del"))
        return redirect(url_for("bookmarks_blueprint.render_bookmarks_page"))
    elif request.method == "GET":
        logger.info("Open bookmarks page")
        return render_template("bookmarks.html", data=data, bookmarks=bookmarks,
                               comment_word_correction_by_count=comment_word_correction_by_count,
                               count_comments=count_comments,
                               get_tags_from_content=get_tags_from_content)
