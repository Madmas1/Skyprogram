# ===== Блюпринт tags view =====#
import app_logger
from flask import Blueprint, render_template, request, redirect, url_for
from configs.config import DATA_PATH, BOOKMARKS_PATH
from dao import BookmarksManager, PageManager
from utils import get_tags_from_content

# Подключаем блюпринт для tags view
tags_blueprint = Blueprint("tags_blueprint", __name__, template_folder="templates")

# Включаем логирование
logger = app_logger.get_logger(__name__)

# Загрузка данных для блюпринта
page_manager = PageManager(DATA_PATH)
bookmarks_manager = BookmarksManager(BOOKMARKS_PATH)


# ===== Роуты =====#
@tags_blueprint.route("/tags/<tag>", methods=["GET", "POST"])
def render_tags_page(tag):
    """Рендер страницы с постами по тегам"""
    bookmarks = bookmarks_manager.get_data()
    post_by_tags = page_manager.search_post_by_tag(tag)
    if request.method == "POST":
        bookmarks_manager.request_add(request.form.get("bookmark_add"))
        bookmarks_manager.request_del(request.form.get("bookmark_del"))
        return redirect(url_for("tags_blueprint.render_tags_page", tag=tag))
    elif request.method == "GET":
        logger.info(f"Open page by tag - {tag}")
        return render_template("tag.html", tag=tag, data=post_by_tags,
                               count_posts=len(post_by_tags), get_tags_from_content=get_tags_from_content,
                               bookmarks=bookmarks)
