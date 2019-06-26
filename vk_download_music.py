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

vk_file = 'vk_config.v2.json'

vk_login = input('Введите номер телефона: ')  # Номер телефона указанный в настройках профиля ВК
vk_password = input('Введите пароль: ')  # Пароль ВК
vk_id = input('Введите id: ')  # id ВК
path = os.path.expanduser(r'~\Downloads') + r'\music_vk'  # Путь где будет создана папка music_vk
print('Путь загрузки', path)

if not os.path.exists(path):
    os.makedirs(path)


# Если включена функция подтверждения входа
def auth_handler():
    code = input('Введите код подтверждения входа: ')
    remember_device = False
    return code, remember_device


def main():
    vk_session = vk_api.VkApi(login=vk_login, password=vk_password, auth_handler=auth_handler)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk_session.get_api()
    vk_audio = audio.VkAudio(vk_session)
    os.chdir(path)

    i = vk_audio.get(owner_id=vk_id)[0]
    r = requests.get(i['url'])
    if r.status_code == 200:
        try:
            with open(i['artist'] + ' - ' + i['title'] + '.mp3', 'wb') as output_file:
                output_file.write(r.content)
        except OSError:
            with open(i['artist'] + ' - ' + i['title'] + '.mp3', 'wb') as output_file:
                output_file.write(r.content)
    a = 0
    time_start = datetime.datetime.now()
    print('Начало загрузки', datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y'))
    for i in vk_audio.get(owner_id=vk_id):
        try:
            a += 1
            r = requests.get(i['url'])
            if r.status_code == 200:
                with open(i['artist'] + ' - ' + i['title'] + '.mp3', 'wb') as output_file:
                    output_file.write(r.content)
        except OSError:
            print('Ошибка загрузки: песня №', a, i['artist'] + ' - ' + i['title'])
    time_end = datetime.datetime.now()
    print('Загружено', len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]),
          'песен за', (time_end - time_start))


if __name__ == '__main__':
    main()
