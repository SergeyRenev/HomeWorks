from config2 import user_token, comm_token, index, line
import vk_api
import requests
import datetime
import json
import logging
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from database import *


class VKBot:
    def __init__(self):
        print('Bot was created')
        self.vk = vk_api.VkApi(token=comm_token)  # авторизация сообщества
        self.longpoll = VkLongPoll(self.vk)  # работа с сообщениями
        self.data_users_old = get_data_users()

    def write_msg(self, user_id, message):
        # метод для отправки сообщении
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7)})

    def get_all_fields(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'sex,bdate,city',
                  'v': '5.131'}
        self.repl = requests.get(url, params=params)

    def name(self, user_id):
        # получение имени пользователя, который написал боту
        response = self.repl.json()
        try:
            information_dict = response['response']
        except:
            logging.error("Не удалось выполнить запрос. Неверно указан токен или id пользователя")
        else:
            for i in information_dict:
                for key, value in i.items():
                    first_name = i.get('first_name')
                    return first_name

    def get_sex(self, user_id):
        # получение пола пользователя, потом меняет на противоположный
        response = self.repl.json()
        try:
            information_list = response['response']
        except:
            logging.error("Не удалось выполнить запрос. Неверно указан токен или id пользователя")
        else:
            for i in information_list:
                if i.get('sex') == 2:
                    find_sex = 1
                    return find_sex
                elif i.get('sex') == 1:
                    find_sex = 2
                    return find_sex

    def get_age_low(self, user_id):
        # получение возраста пользователя для нижней границы поиска
        response = self.repl.json()
        try:
            information_list = response['response']
        except:
            logging.error("Не удалось выполнить запрос. Неверно указан токен или id пользователя")
        else:
            for i in information_list:
                date = i.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
            elif len(date_list) == 2 or date not in information_list:
                self.write_msg(user_id, 'Введите нижний порог возраста (min - 16): ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age

    def get_age_high(self, user_id):
        # получение возраста пользователя для верхней границы поиска
        response = self.repl.json()
        try:
            information_list = response['response']
        except:
            logging.error("Не удалось выполнить запрос. Неверно указан токен или id пользователя")
        else:
            for i in information_list:
                date = i.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
            elif len(date_list) == 2 or date not in information_list:
                self.write_msg(user_id, 'Введите верхний порог возраста (max - 65): ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age

    def cities(self, user_id, city_name):
        # получение ID города пользователя по названию
        url = url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': user_token,
                  'country_id': 1,
                  'q': f'{city_name}',
                  'need_all': 0,
                  'count': 1000,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            list_cities = information_list['items']
        except:
            logging.error("Не удалось выполнить запрос. Неверно указан токен или название города")
        else:
            for i in list_cities:
                found_city_name = i.get('title')
                if found_city_name == city_name:
                    found_city_id = i.get('id')
                    return int(found_city_id)

    def find_city(self, user_id):
        # получение информации о городе пользователя
        response = self.repl.json()
        try:
            information_dict = response['response']
        except:
            logging.error("Не удалось выполнить запрос. Неверно указан токен или id пользователя")
        else:
            for i in information_dict:
                if 'city' in i:
                    city = i.get('city')
                    id = str(city.get('id'))
                    return id
                elif 'city' not in i:
                    self.write_msg(user_id, 'Введите название вашего города: ')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city_name = event.text
                            id_city = self.cities(user_id, city_name)
                            if id_city != '' or id_city != None:
                                return str(id_city)
                            else:
                                break

    def find_user(self, user_id):
        # поиск человека по полученным данным
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': user_token,
                  'v': '5.131',
                  'sex': self.get_sex(user_id),
                  'age_from': self.get_age_low(user_id),
                  'age_to': self.get_age_high(user_id),
                  'city': self.find_city(user_id),
                  'fields': 'is_closed, id, first_name, last_name',
                  'status': '1' or '6',
                  'count': 500}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        self.data_users = []
        try:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
        except:
            logging.error("Не удалось выполнить запрос. Неверно указан токен или id пользователя")
        else:
            for person_dict in list_1:
                if person_dict.get('is_closed') == False:
                    first_name = person_dict.get('first_name')
                    last_name = person_dict.get('last_name')
                    vk_id = str(person_dict.get('id'))
                    vk_link = 'vk.com/id' + str(person_dict.get('id'))
                    self.data_users.append((first_name, last_name, vk_id, vk_link))
                else:
                    continue
            return f'Поиск завершён'

    def get_photos_id(self, user_id):
        # получение ID фотографии в обратном порядке
        url = 'https://api.vk.com/method/photos.getAll'
        params = {
                  'access_token': user_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.131'}
        resp = requests.get(url, params=params)
        dict_photos = dict()
        resp_json = resp.json()
        try:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
        except:
            logging.error("Не удалось выполнить запрос. Неверно указан токен или id пользователя")
        else:
            for i in list_1:
                photo_id = str(i.get('id'))
                i_likes = i.get('likes')
                if i_likes.get('count'):
                    likes = i_likes.get('count')
                    dict_photos[likes] = photo_id
            list_of_ids = sorted(dict_photos.items(), reverse=True)
            return list_of_ids

    def get_photo(self, user_id, num_photo):
        # получение номера num_photo фотографии user_id
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == num_photo:
                return i[1]
        return None

    def send_photo(self, user_id, message, index, num_photo):
        # отправка фотографии по номеру (num_photo)
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(index)}_{self.get_photo(self.person_id(index), num_photo)}',
                                         'random_id': 0})

    def send_photo_and_insert_in_table(self, user_id, message, count, num_photo):
        # вывод количества (count) анкет с номером фото (num_photo) и их запись в таблицу users
        count_old = len(self.data_users_old)
        count_new = count_old + count
        if count_new >= len(line) or count_new >= len(self.data_users):
            self.write_msg(user_id, f'Достигнут лимит по количеству анкет')
        else:
            for i in range(count_old, count_new):
                is_same = self.data_users_old.count(self.data_users[i])
                if is_same == 0: # если анкета не была просмотрена ранее
                    self.send_photo(user_id, message, i, num_photo)
                    a = self.data_users[i][0]
                    b = self.data_users[i][1]
                    c = self.data_users[i][2]
                    d = self.data_users[i][3]
                    insert_data_users(a,b,c,d)

    def find_persons(self, user_id, index):
        self.write_msg(user_id, self.found_person_info(index))
        res = insert_data_seen_users(str(self.person_id(index)), index) #index
        if res != -1:
            num_photo = 1
            if self.get_photo(self.person_id(index), num_photo) != None:
                self.send_photo(user_id, 'Фото номер 1', index, num_photo)
            else:
                self.write_msg(user_id, f'Больше фотографий нет')
            num_photo = 2
            if self.get_photo(self.person_id(index), num_photo) != None:
                self.send_photo(user_id, 'Фото номер 2', index, num_photo)
            else:
                self.write_msg(user_id, f'Больше фотографий нет')
            num_photo = 3
            if self.get_photo(self.person_id(index), num_photo) != None:
                self.send_photo(user_id, 'Фото номер 3', index, num_photo)
            else:
                self.write_msg(user_id, f'Больше фотографий нет')
        else:
            self.write_msg(user_id, f'Пара была найдена ранее, нажмите кнопку "Вперед"')

    def found_person_info(self, index):
        # вывод информации о найденном пользователе по index
        if index >= len(self.data_users):
            logging.error("Значение Index выходит за допустмый диапазон")
        else:
            tuple_person = self.data_users[index]
            list_person = []
            for i in tuple_person:
                list_person.append(i)
            return f'{list_person[0]} {list_person[1]}, ссылка - {list_person[3]}'

    def person_id(self, index):
        # вывод ID найденного пользователя по индексу
        if index >= len(self.data_users):
            logging.error("Значение Index выходит за допустмый диапазон")
        else:
            tuple_person = self.data_users[index]
            list_person = []
            for i in tuple_person:
                list_person.append(i)
            return str(list_person[2])

# кнопки в вк
def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


keyboard = {
    "one_time": False,
    "buttons": [
        [get_button('Начать поиск', 'primary')],
        [get_button('Вперёд', 'secondary')]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

def sender(user_id: object, bot: object, text: object) -> object:
    bot.vk.method('messages.send', {'user_id': user_id,
                                    'message': text,
                                    'random_id': 0,
                                    'keyboard': keyboard})

# интерактивный режим с ботом
def Bot(bot, index):
    for event in bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()
            user_id = str(event.user_id)
            msg = event.text.lower()
            sender(user_id, bot, msg.lower())
            if request == 'начать поиск':
                creating_database()
                bot.write_msg(user_id, f'Привет, {bot.name(user_id)}')
                bot.find_user(user_id)
                bot.write_msg(event.user_id, f'Нашёл для тебя пару, жми на кнопку "Вперёд"')

            elif request == 'вперёд':
                for i in line:
                    index += 1
                    bot.find_persons(user_id, index)
                    break
            else:
                bot.write_msg(event.user_id, 'Твоё сообщение непонятно')




bot = VKBot()
creating_database()
user_id = 4765632
bot.write_msg(user_id, 'Привет')
bot.get_all_fields( user_id)
name = bot.name(user_id)
print(name)
sex = bot.get_sex(user_id)
print(sex)
age = bot.get_age_low(user_id)
print(age)
city = bot.cities(user_id, 'Москва')
print(city)
info_city = bot.find_city(user_id)
print(info_city)
find = bot.find_user(user_id)
print(find)
photos_id = bot.get_photos_id(270758211)
print(photos_id)
bot.send_photo_and_insert_in_table(user_id, 'Hello!', 10, 1)
Bot(bot, index)
print('Finish')