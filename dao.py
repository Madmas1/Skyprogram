# Обработчик данных
import json
import exceptions
import app_logger
from random import shuffle

# Включаем логирование
logger = app_logger.get_logger(__name__)


class FileManager:
    """ Класс управления файлами с данными JSON"""
    def __init__(self, path):
        self.path = path

    # Метод загрузки данных из файла
    def load_data(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            logger.error(f"Can't load JSON data from {self.path}!")
            raise

    # Метод сохранения данных в файлов
    def save_data(self, data):
        try:
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except (json.JSONDecodeError, FileNotFoundError):
            logger.error(f"Can't save JSON data in {self.path}!")
            raise


class PageManager(FileManager):
    """Основной класс по подготовке данных для представлений. Наследуется от класса FileManager"""
    # Метод получения данных из файлов
    def get_data(self):
        return self.load_data()

    # Метод получения данных для страницы пользователя
    def get_data_for_user_page(self, username):
        user_page_data = []
        for elem in self.load_data():
            if elem["poster_name"] == username:
                user_page_data.append(elem)
        if user_page_data:
            return user_page_data
        else:
            logger.error(f"Can't load {username} page. User not found!")
            raise exceptions.UserNotFound

    # Метод получения для страницы с постом
    def get_post_page_data(self, post_id):
        data = ''
        for elem in self.load_data():
            if post_id == elem["pk"]:
                if elem:
                    data = elem
        if data:
            return data
        else:
            logger.error(f"Can't load post page № {post_id}. Post not exists!")
            raise exceptions.PostNotFound

    # Метод получения данных для страницы с закладками
    def get_bookmarks_page_data(self, bookmarks):
        bookmarks_data = []
        for elem in self.load_data():
            if elem["pk"] in bookmarks:
                bookmarks_data.append(elem)
        return bookmarks_data

    # Метод для получения данных для страницы с поиском
    def search_post_by_keyword(self, keyword):
        data = self.load_data()
        posts_list = []
        shuffle(data)
        for elem in data:
            if keyword in elem["content"] and len(posts_list) <= 10:
                posts_list.append(elem)
        return posts_list

    # Метод получения данных для страницы с тегами
    def search_post_by_tag(self, tag):
        posts_list = []
        for elem in self.load_data():
            if "#" + tag in elem["content"]:
                posts_list.append(elem)
        return posts_list


class BookmarksManager(FileManager):
    """Класс для обработки данных для закладок. Наследуется от класса FileManager"""

    # Метод получения данных из файлов
    def get_data(self):
        return self.load_data()

    # Метод обрабатывающий добавление поста на страницу с закладками
    def request_add(self, request):
        if request:
            new_data = self.load_data()
            new_data.append(int(request))
            self.save_data(new_data)
            logger.info(f"Add post №{request} in bookmarks")

    # Метод обрабатывающий удаление поста на страницу с закладками
    def request_del(self, request):
        if request:
            new_data = self.load_data()
            new_data.remove(int(request))
            self.save_data(new_data)
            logger.info(f"Remove post №{request} in bookmarks")


class CommentsManager(FileManager):
    """Класс для обработки данных пользовательских комментариев. Наследуется от класса FileManager"""

    # Метод получения данных из файлов
    def get_comments_data(self):
        return self.load_data()

    # Метод подготавливающий список с количеством комментариев в посте
    def count_comments(self, data):
        comments_count_list = []
        count = 0
        for elem in data:
            for comment in self.load_data():
                if comment['post_id'] == elem['pk']:
                    count += 1
            comments_count_list.append({"post_id": elem["pk"], "count": count})
            count = 0
        return comments_count_list

    # Метод получения комментариев для поста
    def get_comments(self, post_id):
        comments = []
        for elem in self.load_data():
            if elem["post_id"] == post_id:
                comments.append({"commenter_name": elem["commenter_name"], "comment": elem["comment"]})
        return comments

    # Метод сохраняющий комментарий пользователя
    def form_a_comment(self, commenter_name, comment, post_id):
        if commenter_name and comment:
            comments = self.load_data()
            pk = len(comments) + 1
            comments.append({
                "post_id": post_id,
                "commenter_name": commenter_name,
                "comment": comment,
                "pk": pk
            })
            self.save_data(comments)