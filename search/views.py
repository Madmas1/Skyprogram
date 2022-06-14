#===== Блюпринт search view =====#

import app_logger
from flask import Blueprint, render_template, request, redirect, url_for
from configs.config import DATA_PATH, BOOKMARKS_PATH
from dao import CommentsManager, BookmarksManager, PageManager
from utils import comment_word_correction_by_count, get_tags_from_content

# Подключаем блюпринт для search view
search_blueprint = Blueprint("search_blueprint", __name__, template_folder="templates")

# Включаем логирование
logger = app_logger.get_logger(__name__)

# Загрузка данных для блюпринта
page_manager = PageManager(DATA_PATH)
bookmarks_manager = BookmarksManager(BOOKMARKS_PATH)

#===== Роуты ====#
@search_blueprint.route("/search", methods=["GET", "POST"])
def search_render_page():
    """Рендер страницы поиска постов"""
    keyword = request.args.get('s', '')
    data = page_manager.search_post_by_keyword(keyword)
    bookmarks = bookmarks_manager.get_data()
    if request.method == "POST":
        bookmarks_manager.request_add(request.form.get("bookmark_add"))
        bookmarks_manager.request_del(request.form.get("bookmark_del"))
        return render_template("search.html", data=data, count_posts=len(data),
                               get_tags_from_content=get_tags_from_content, bookmarks=bookmarks, keyword=keyword)
    elif request.method == "GET":
        if keyword:
            logger.info(f"Search by keyword {keyword}")
            return render_template("search.html", data=data, count_posts=len(data),
                                   get_tags_from_content=get_tags_from_content, bookmarks=bookmarks, keyword=keyword)
        else:
            logger.info(f"Open search page")
            return render_template("search.html")