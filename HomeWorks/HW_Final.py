import requests

import time
from tqdm import tqdm

import json

class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

   def photos_get(self):
       url = 'https://api.vk.com/method/photos.get'
       owner_id = 4765632
       album_id = 'profile'
       rev = 0
       extended = 1
       feed_type = 'photo'
       photo_sizes = 1
       count = 5 # 5 фоток
       params = {'owner_id': owner_id, 'album_id': album_id, 'rev': rev, 'extended': extended, 'feed_type': feed_type, 'photo_sizes': photo_sizes, 'count': count}
       response = requests.get(url, params={**self.params, **params})
       return response.json()


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, url_photos = {}):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        # Тут ваша логика

        # информация о состоянии облачного хранилища
        headers = {"Authorization": f"OAuth {self.token}"}
        res = requests.get("https://cloud-api.yandex.net/v1/disk", headers=headers)

        # создаем папку Тест API на яндекс-диске
        params = {"path": "Тест API"}
        res = requests.put("https://cloud-api.yandex.net/v1/disk/resources", headers=headers, params=params)

        # копируем в папку Тест API фотки из ВК
        for key, val in tqdm(url_photos.items()): # tqdm - прогресс бар
            params = {"path": f"Тест API/{val}", 'url': key}
            res = requests.post("https://cloud-api.yandex.net/v1/disk/resources/upload", headers=headers, params=params)

        print(res)
        # Функция может ничего не возвращать

def get_url_photos(photos_info):
    url_photos = {}
    for item in photos_info['response']['items']:
        index = len(item['sizes']) - 1         # последний индекс с max размером фото
        name_photo = item['likes']['count']    # имя фото
        if name_photo in url_photos.values():  # смотрим, есть ли имя в списке. Если есть - прибавляем к имени дату
            name_photo = f"{name_photo} {item['date']}"
        url_photos[item['sizes'][index]['url']] = f"{name_photo}.jpg"
    return url_photos

def save_json_file(photos_info):
    json_file = []
    for item in photos_info['response']['items']:
        index = len(item['sizes']) - 1         # последний индекс с max размером фото
        name_photo = item['likes']['count']    # имя фото
        if name_photo in url_photos.values():  # смотрим, есть ли имя в списке. Если есть - прибавляем к имени дату
            name_photo = f"{name_photo} {item['date']}"
        json_file.append({"file_name": f"{name_photo}.jpg", "size": item['sizes'][index]['type']})
    # print(json_file)
    with open('data.json', 'w') as f:
        json.dump(json_file, f)


if __name__ == '__main__':
    access_token = ''
    user_id = '4765632'
    vk = VK(access_token, user_id)
    print(vk.users_info())
    photos_info = vk.photos_get()
    url_photos = get_url_photos(photos_info)
    save_json_file(photos_info)

    # Получить путь к загружаемому файлу и токен от пользователя
    token = ''
    uploader = YaUploader(token)
    result = uploader.upload(url_photos)




