import requests

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        # Тут ваша логика

        # информация о состоянии облачного хранилища
        headers = {"Authorization": f"OAuth {self.token}"}
        res = requests.get("https://cloud-api.yandex.net/v1/disk", headers=headers)

        # создаем папку Тест API на яндекс-диске
        params = {"path": "Тест API"}
        res = requests.put("https://cloud-api.yandex.net/v1/disk/resources", headers=headers, params=params)

        # копируем в папку Тест API файлы
        params = {"path": "Тест API/1.txt"}
        res = requests.get("https://cloud-api.yandex.net/v1/disk/resources/upload", headers=headers, params=params)

        href = res.json()["href"]  # URL
        files = {"file": open(file_path, "r")}
        res = requests.put(href, files=files)

        print(res)
        # Функция может ничего не возвращать


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = '../HomeWorks/recipes/1.txt'
    token = 'y0_AgAAAABT8HI7AADLWwAAAADWWEnEQjlK9GeZRZS_xT3v8mt_Ho-JbgQ'
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)