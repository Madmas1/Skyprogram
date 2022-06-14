#===== Блюпринт post view =====#
import app_logger
from flask import Blueprint, render_template, request, redirect, url_for
from configs.config import DATA_PATH, COMMENTS_PATH, BOOKMARKS_PATH
from dao import CommentsManager, BookmarksManager, PageManager
from utils import comment_word_correction_by_count, get_tags_from_content
from utils import tags_conversion_in_content

# Подключаем блюпринт для post view
post_blueprint = Blueprint("post_blueprint", __name__, template_folder="templates")

# Включаем логирование
logger = app_logger.get_logger(__name__)

# Загрузка данных для блюпринта
page_manager = PageManager(DATA_PATH)
bookmarks_manager = BookmarksManager(BOOKMARKS_PATH)
comments_manager = CommentsManager(COMMENTS_PATH)


#===== Роуты ====#
@post_blueprint.route("/post/<int:post_id>", methods=["GET", "POST"])
def render_post_page(post_id):
    """Рендер страницы с постом"""
    post_page_data = page_manager.get_post_page_data(post_id)
    bookmarks = bookmarks_manager.get_data()
    comments_data = comments_manager.get_comments_data()
    if request.method == "POST":
        bookmarks_manager.request_add(request.form.get("bookmark_add"))
        bookmarks_manager.request_del(request.form.get("bookmark_del"))
        comments_manager.form_a_comment(request.form.get("commenter_name"), request.form.get("comment"), post_id)
        return redirect(url_for("post_blueprint.render_post_page", post_id=post_id))
    elif request.method == "GET":
        logger.info(f"Open post page №{post_id}")
        comments = comments_manager.get_comments(post_id)
        content = tags_conversion_in_content(post_page_data["content"])
        return render_template("post.html", user=post_page_data, content=content, count_comments=len(comments),
                               comment_word_correction_by_count=comment_word_correction_by_count(len(comments)),
                               comments=comments, bookmarks=bookmarks)
