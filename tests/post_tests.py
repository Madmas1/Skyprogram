#===== Тесты представления post =====#

from dao import PageManager
from configs.config import DATA_PATH

post_id = 1

page_manager = PageManager(DATA_PATH)
content = page_manager.get_post_page_data(post_id)

name = content["poster_name"].capitalize()
poster_avatar = content["poster_avatar"]
text = content["content"]
views_count = str(content["views_count"])
pk = str(content["pk"])


class TestIndex:

    def test_root_status(self, test_client):
        response = test_client.get('/post/' + str(post_id), follow_redirects=True)
        assert response.status_code == 200
        assert name in response.data.decode("utf-8"), "Контент страницы неверный"
        assert poster_avatar in response.data.decode("utf-8"), "Контент страницы неверный"
        assert text in response.data.decode("utf-8"), "Контент страницы неверный"
        assert pk in response.data.decode("utf-8"), "Контент страницы неверный"
        assert views_count in response.data.decode("utf-8"), "Контент страницы неверный"