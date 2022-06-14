#===== Модуль тестирования модуля DAO =====#

import pytest
import exceptions

from configs.config import DATA_PATH, COMMENTS_PATH
from dao import PageManager, CommentsManager


# Фикстуры классов
@pytest.fixture()
def dao_page_manager():
    page_manager = PageManager(DATA_PATH)
    return page_manager


@pytest.fixture()
def dao_comments():
    comments_manager = CommentsManager(COMMENTS_PATH)
    return comments_manager


# Тестирование класса PageManger

posts_keys = {
    'content',
    'likes_count',
     'pic',
    'pk',
    'poster_avatar',
    'poster_name',
    'views_count'
                  }


class TestPageManager:

    def test_get_all(self, dao_page_manager):
        data = dao_page_manager.get_data()
        assert type(data) == list, "возвращается не список"
        assert len(data) > 0, "возвращается пустой список"
        assert set(data[0].keys()) == posts_keys, "неверный список ключей"

    def test_get_by_id(self, dao_page_manager):
        data = dao_page_manager.get_post_page_data(1)
        assert(data["pk"] == 1), "возвращается неправильный пост"
        assert set(data.keys()) == posts_keys, "неверный список ключей"

    def test_get_bookmarks(self, dao_page_manager):

        data = dao_page_manager.get_bookmarks_page_data([1])
        assert type(data) == list, "возвращается не список"
        assert len(data) > 0, "возвращается пустой список"
        assert set(data[0].keys()) == posts_keys, "неверный список ключей"

    def test_search_posts_by_keyword(self, dao_page_manager):

        data = dao_page_manager.search_post_by_keyword("еда")
        assert type(data) == list, "возвращается не список"
        assert len(data) > 0, "возвращается пустой список"
        assert set(data[0].keys()) == posts_keys, "неверный список ключей"

    def test_get_data_for_user_page_user_nof_found(self, dao_page_manager):
        with pytest.raises(exceptions.UserNotFound):
            dao_page_manager.get_data_for_user_page("mike")

    def test_get_post_page_data(self, dao_page_manager):
        with pytest.raises(exceptions.PostNotFound):
            dao_page_manager.get_post_page_data(-40)
        with pytest.raises(exceptions.PostNotFound):
            dao_page_manager.get_post_page_data("40")
        with pytest.raises(exceptions.PostNotFound):
            dao_page_manager.get_post_page_data("str")


# Тестирование класса CommentsManager
comments_keys = {
    "post_id",
    "commenter_name",
    "comment",
    "pk",
  }


class TestCommentsManager:

    def test_get_all(self, dao_comments):
        data = dao_comments.get_comments_data()
        assert type(data) == list, "возвращается не список"
        assert len(data) > 0, "возвращается пустой список"
        assert set(data[0].keys()) == comments_keys, "неверный список ключей"

    def test_get_comment(self, dao_comments):
        data = dao_comments.get_comments(1)
        assert type(data) == list, "возвращается не список"
        assert len(data) > 0, "возвращается пустой список"
        assert set(data[0].keys()) == {"commenter_name", "comment"}, "неверный список ключей"






