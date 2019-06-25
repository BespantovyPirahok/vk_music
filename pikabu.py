import vk_api  # pip install vk_api
from vk_api import audio
import requests  # pip install request 
from time import time
import os

# pip install BeautifulSoup4

vk_file = 'vk_config.v2.json'
REQUEST_STATUS_CODE = 200

vk_login = '___'  # Номер телефона указанный в настройках профиля ВК
vk_password = '___'  # Пароль ВК
vk_id = '____'  # Ваш id ВК (зайдя в "Моя музыка" в адресной строке браузера будет что-то вроде https://vk.com/audios1362067; 1362067 - id)
path = r'C:\Users\Violet\Downloads\vk\\' + 'music_vk'  # Путь, где будет создана папка music_vk

if not os.path.exists(path):
    os.makedirs(path)

vk_session = vk_api.VkApi(login=vk_login, password=vk_password)
vk_session.auth()
vk = vk_session.get_api()
vk_audio = audio.VkAudio(vk_session)

os.chdir(path)


i = vk_audio.get(owner_id=vk_id)[85]
r = requests.get(i['url'])
if r.status_code == REQUEST_STATUS_CODE:
    try:
        with open(i['artist'] + '_' + i['title'] + '.mp3', 'wb') as output_file:
            output_file.write(r.content)
    except OSError:
        with open(i['artist'] + '_' + i['title'] + '.mp3', 'wb') as output_file:
            output_file.write(r.content)
a = 0
time_start = time()
for i in vk_audio.get(owner_id=vk_id):
    try:
        a += 1
        r = requests.get(i['url'])
        if r.status_code == REQUEST_STATUS_CODE:
            with open(i['artist'] + '_' + i['title'] + '.mp3', 'wb') as output_file:
                output_file.write(r.content)
    except OSError:
        print(a)
time_finish = time()
print('Time seconds:', time_finish - time_start)
