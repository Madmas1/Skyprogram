# ===== Утилиты приложения=====#


# Метод корректировки слова по количеству.
# Только для комментариев т.к. их количество может варьироваться. Остальные данные статичны.
def comment_word_correction_by_count(count):
    if count in [11, 12, 13, 14]:
        return "Комментариев"
    elif count % 10 == 0:
        return "Комментариев"
    elif count % 10 in [2, 3, 4]:
        return "Комментария"
    elif count % 10 == 1:
        return "Комментарий"
    else:
        return "Комментариев"


# Метод получения списка тегов для поста
def get_tags_from_content(data):
    word_list = data.split(' ')
    tags_list = []
    for word in word_list:
        if '#' in word:
            tags_list.append(word[1:])
    return tags_list


# Метод конверсии в гиперссылки тегов полученных из поста.
def tags_conversion_in_content(content):
    content = content.split(' ')
    for word in content:
        if "#" in word:
            tag_index = content.index(word)
            word = word[1:]
            word = f'''<a href="/tags/{word}" class="item__tag">#{word}</a>'''
            content[tag_index] = word
    return ' '.join(content)

