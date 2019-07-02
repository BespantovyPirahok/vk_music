#! /usr/bin/python3
#  -*- coding: UTF-8 -*-

# pip install request
# pip install vk_api
# pip install BeautifulSoup4
# pip install tqdm

import datetime
import time
import os
import os.path

import requests
import vk_api
from vk_api import audio

import getpass
from tqdm import tqdm


# Авторизация
def auth(vk_login=None, vk_password=None):
    if not vk_login:
        vk_login = input('Введите телефон или email: ')
    if not vk_password:
        # vk_password = getpass.getpass('Введите пароль: ')
        vk_password = input('Введите пароль: ')
    return vk_login, vk_password


# Если включена функция подтверждения входа
def two_step_auth():
    code = input('Введите код подтверждения входа: ')
    remember_device = False
    return code, remember_device


def folder():
    path = os.path.expanduser(r'~\Downloads') + r'\music_vk'

    if not os.path.exists(path):
        os.makedirs(path)
    return path


def main(vk_login=None, vk_password=None):
    vk_login, vk_password = auth(vk_login=vk_login, vk_password=vk_password)
    vk_session = vk_api.VkApi(login=vk_login, password=vk_password, auth_handler=two_step_auth)

    vk_session.auth()
    print('Авторизация')
    vk = vk_session.get_api()
    vk_audio = audio.VkAudio(vk_session)

    try:
        print('Успех')

        def download(v_id):
            path = folder()
            os.chdir(path)
            song = 0
            time_start = datetime.datetime.now()
            print('Начало загрузки', datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y'))
            print('Путь загрузки:', path)
            for i in vk_audio.get(owner_id=v_id):
                try:
                    song += 1
                    r = requests.get(i['url'], stream=True)
                    size = int(r.headers['Content-Length'])
                    if r.status_code == 200:
                        with open(str(song) + '_' + i['artist'] + ' - ' + i['title'] + '.mp3', 'wb') as file:
                            print('Загрузка:', i['artist'] + ' - ' + i['title'])
                            time.sleep(0.5)
                            for data in tqdm(iterable=r.iter_content(chunk_size=1024), total=size / 1024, unit='KB',
                                             leave=True):
                                file.write(data)
                except OSError:
                    print('Ошибка загрузки:', song, i['artist'] + ' - ' + i['title'])
            time_end = datetime.datetime.now()
            print('Загружено', len(next(os.walk(path))[2]), 'песен за', (time_end - time_start))
            input('Нажмите ENTER для выхода')

        def own_music():
            v_id = vk.users.get()[0]['id']
            print('Анализ музыки', vk.users.get()[0]['first_name'] + ' ' + vk.users.get()[0]['last_name'])
            download(v_id)

        def friends_music(v_id):
            v_id_f = vk.users.get(user_ids=v_id)
            print('Анализ музыки', v_id_f[0]['first_name'] + ' ' + v_id_f[0]['last_name'])
            download(v_id)

        question = input('Загрузить свою музыку?\ny/n: ')

        if question == 'y':
            own_music()

        elif question == 'n':
            question_1 = input('1 Выбрать друга\n2 Ввести id\nСделайте выбор: ')

            if question_1 == '1':
                number_of_friends = vk.friends.get(order='name')
                print('Друзей:', number_of_friends['count'])
                dictionary_friends = {}

                for num in range(0, int(number_of_friends['count'])):
                    user = vk.friends.get(fields='first_name,last_name')['items'][num]
                    print(num, user['first_name'], user['last_name'])
                    k = str(num)
                    dictionary_friends[k] = user['id']
                b = input('Введите номер друга: ')
                friends_music(v_id=dictionary_friends[b])

            elif question_1 == '2':
                try:

                    friends_music(v_id=input('Введите id: '))
                except vk_api.exceptions.AccessDenied:
                    print('У Вас нет прав для просмотра аудио пользователя')
                    friends_music(v_id=input('Введите id: '))

    except vk_api.AuthError:
        print('Неверный пароль')
        main(vk_login=vk_login)

    except vk_api.exceptions.Captcha:
        print('Неверный логин')
        main(vk_password=vk_password)


if __name__ == '__main__':
    main()
