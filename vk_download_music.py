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

vk_file = 'vk_config.v2.json'

vk_login = input('Введите номер телефона: ')  # Номер телефона указанный в настройках профиля ВК
vk_password = input('Введите пароль: ')  # Пароль ВК
vk_id = input('Введите id: ')  # id ВК
path = os.path.expanduser(r'~\Downloads') + r'\music_vk'  # Путь где будет создана папка music_vk
print('Путь загрузки', path)

# Если папки нет - создаём
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
    print(r)  # <Response [200]>

        if r.status_code == 200:
        try:
            song = 0
            time_start = datetime.datetime.now()
            print('Начало загрузки', datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y'))
            for i in vk_audio.get(owner_id=vk_id):
                try:
                    song += 1
                    r = requests.get(i['url'], stream=True)
                    size = int(r.headers['content-length'])
                    if r.status_code == 200:
                        with open(str(song) + '_' + i['artist'] + ' - ' + i['title'] + '.mp3', 'wb') as output_file:
                            print('Загрузка:', i['artist'] + ' - ' + i['title'])
                            for data in tqdm(iterable=r.iter_content(chunk_size=1024), total=size/1024, unit='KB'):
                                output_file.write(data)
                except OSError:
                    print('Ошибка загрузки:', song, i['artist'] + ' - ' + i['title'])
            time_end = datetime.datetime.now()
            print('Загружено', len(next(os.walk(path))[2]), 'песен за', (time_end - time_start))
            input('Нажмите ENTER для выхода')
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return


if __name__ == '__main__':
    main()
