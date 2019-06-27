#! /usr/bin/python3
#  -*- coding: UTF-8 -*-

# pip install request
# pip install vk_api
# pip install BeautifulSoup4

import datetime
import os
import os.path

import requests
import vk_api
from vk_api import audio

from tqdm import tqdm


# Авторизация
def auth(vk_login=None, vk_password=None, vk_id=None):
    if not vk_login:
        vk_login = input('Введите телефон или email: ')
    if not vk_password:
        vk_password = input('Введите пароль: ')
    if not vk_id:
        vk_id = input('Введите id: ')
    return vk_login, vk_password, vk_id


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


def main(vk_login=None, vk_password=None, vk_id=None):
    vk_login, vk_password, vk_id = auth(vk_login=vk_login, vk_password=vk_password, vk_id=vk_id)
    vk_session = vk_api.VkApi(login=vk_login, password=vk_password, auth_handler=two_step_auth)
    try:
        vk_session.auth()
        print('Авторизация')
        vk_session.get_api()
        vk_audio = audio.VkAudio(vk_session)
        path = folder()
        os.chdir(path)

        i = vk_audio.get(owner_id=vk_id)[0]
        r = requests.get(i['url'])

        if r.status_code == 200:
            print('Успех')
            song = 0
            time_start = datetime.datetime.now()
            print('Начало загрузки', datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y'))
            print('Путь загрузки:', path)
            for i in vk_audio.get(owner_id=vk_id):
                try:
                    song += 1
                    r = requests.get(i['url'], stream=True)
                    size = int(r.headers['content-length'])
                    if r.status_code == 200:
                        with open(str(song) + '_' + i['artist'] + ' - ' + i['title'] + '.mp3', 'wb') as output_file:
                            print('Загрузка:', i['artist'] + ' - ' + i['title'])
                            for data in tqdm(iterable=r.iter_content(chunk_size=1024), total=size / 1024, unit='KB'):
                                output_file.write(data)
                except OSError:
                    print('Ошибка загрузки:', song, i['artist'] + ' - ' + i['title'])
            time_end = datetime.datetime.now()
            print('Загружено', len(next(os.walk(path))[2]), 'песен за', (time_end - time_start))
            input('Нажмите ENTER для выхода')
        else:
            print('Что-то пошло не так')
            input('Нажмите ENTER для выхода')
    except vk_api.AuthError:
        print('Неверный пароль')
        main(vk_login=vk_login, vk_id=vk_id)
    except vk_api.exceptions.Captcha:
        print('Неверный логин')
        main(vk_password=vk_password, vk_id=vk_id)
    except vk_api.exceptions.AccessDenied:
        print('У Вас нет прав для просмотра аудио пользователя')
        main(vk_login=vk_login, vk_password=vk_password)


if __name__ == '__main__':
    main()
