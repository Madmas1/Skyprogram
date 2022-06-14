#===== Модуль с подготовкой тестовых данных =====#

import run
import pytest
import unittest.mock
from dao import PageManager


@pytest.fixture()
def test_client():
    app = run.app
    return app.test_client()


@pytest.fixture
def mock_post_manager_load_data():
    PageManager.get_data = unittest.mock.Mock(return_value=[
        {
            'poster_name': 'leo',
            'poster_avatar': 'https://randus.org/avatars/w/c1819dbdffffff18.png',
            'pic': 'https://images.unsplash.com/photo-1525351326368-efbb5cb6814d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=580&q=80',
            'content': 'Ага, опять еда! Квадратная тарелка в квадратном кадре. А на тарелке, наверное, пирог! Мне было так жаль, что я не могу ее съесть. Я боялась, что они заметят, и если я не съем это, то, значит, они все подумают, что я плохая девочка... Но потом мне вспомнилось, как они на меня смотрели. Когда я была маленькой, на кухне всегда были родители, бабушка, дедушка, дядя Борис... Все вместе. И всегда одна я, потому что все остальные приходили туда лишь изредка. Мне казалось, если бы все ходили на работу, как и я, в этот свой офис, было бы совсем неинтересно.',
            'views_count': 376,
            'likes_count': 154,
            'pk': 1
        },
    ])


@pytest.fixture
def post_fields():
    return {
        'poster_name',
        'poster_avatar',
        'pic',
        'content',
        'views_count',
        'likes_count',
        'pk',
    }