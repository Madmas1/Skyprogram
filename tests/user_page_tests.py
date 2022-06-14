#===== Тесты представления userpage =====#

from dao import PageManager
from configs.config import DATA_PATH

poster_name = "leo"

page_manager = PageManager(DATA_PATH)
content = page_manager.get_data_for_user_page(poster_name)

name = content[0]["poster_name"]
pic = content[0]["pic"]
text = content[0]["content"][:50]
likes_count = str(content[0]["likes_count"])
views_count = str(content[0]["views_count"])
pk = str(content[0]["pk"])


class TestIndex:

    def test_root_status(self, test_client):
        response = test_client.get('/user/' + poster_name, follow_redirects=True)
        assert response.status_code == 200
        assert name in response.data.decode("utf-8"), "Контент страницы неверный"
        assert pk in response.data.decode("utf-8"), "Контент страницы неверный"
        assert text in response.data.decode("utf-8"), "Контент страницы неверный"
        assert likes_count in response.data.decode("utf-8"), "Контент страницы неверный"
        assert views_count in response.data.decode("utf-8"), "Контент страницы неверный"