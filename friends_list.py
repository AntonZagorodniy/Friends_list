from pprint import pprint
from urllib.parse import urlencode
import json

import requests

try:
    with open('config.json', encoding='utf-8-sig') as f:
        data = json.load(f)
except FileNotFoundError:
    print('Файл не найден')

AUTHORIZE_URL = data[0]['AUTHORIZE_URL']
APP_ID = data[1]['APP_ID']
VERSION = data[2]['VERSION']
TOKEN = data[3]['TOKEN']

# Словарь с ключами
auth_data = {
    'client_id': APP_ID,  # ID приложения
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'mobile',
    'scope': 'status',
    'response_type': 'token',
    'v': VERSION
}

# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

params = {
    'access_token': TOKEN,
    'v': VERSION
}

response = requests.get('https://api.vk.com/method/friends.get', params)
# print(response.json()['response']['items'][0])
users_list = set(response.json()['response']['items'])
user_friends_list = []
for i, user in enumerate(users_list):
    params = {
        'access_token': TOKEN,
        'v': VERSION,
        'user_id': user
    }
    user_friends_response = requests.get('https://api.vk.com/method/friends.get', params)
    # print(user_friends_response.json()['response']['items'][2])
    user_friends_list = set(user_friends_response.json()['response']['items'])
    # print(user_friends_list)
    # d = set.intersection(user_friends_list)
    users_list.intersection_update(user_friends_list)
    print(users_list)
# response = requests.get('https://api.vk.com/method/friends.get', params)
# pprint(response.text)

