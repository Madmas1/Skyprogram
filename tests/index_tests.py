#===== Тесты представления index =====#

from dao import PageManager
from configs.config import DATA_PATH

page_manager = PageManager(DATA_PATH)
content = page_manager.get_data()

name = content[0]["poster_name"]
likes_count = str(content[0]["likes_count"])
views_count = str(content[0]["views_count"])
text = content[0]["content"][:50]
pk = str(content[0]["pk"])


class TestIndex:

    def test_root_status(self, test_client):
        response = test_client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert name in response.data.decode("utf-8"), "Контент страницы неверный"
        assert pk in response.data.decode("utf-8"), "Контент страницы неверный"
        assert text in response.data.decode("utf-8"), "Контент страницы неверный"
        assert likes_count in response.data.decode("utf-8"), "Контент страницы неверный"
        assert views_count in response.data.decode("utf-8"), "Контент страницы неверный"