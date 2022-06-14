# ===== Классы обработчиков исключений  ===== #


from werkzeug.exceptions import NotFound


# Обработка исключения если пост не был найден
class PostNotFound(NotFound):
    pass


# Обработка исключения если пользователь не был найден
class UserNotFound(NotFound):
    pass
