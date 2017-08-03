import requests
import time
import json

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.65'
VK_API = 'https://api.vk.com/method/'

user_name = 'tim_leary'
user_id = 5030613
token = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'

params = {
    'access_token': token,
    'v': VERSION,
    'user_id': user_id,
    'extended': 1,
}

def get_members(group_id):
    params['group_id'] = group_id
    return requests.get(VK_API + 'groups.getMembers', params).json()['response']['items']

def get_group_without_friends():
    list_friends = requests.get(VK_API + 'friends.get', params).json()['response']['items']
    groups = requests.get(VK_API + 'groups.get', params).json()['response']['items']
    without_friends_group = []
    for group in groups:
        list_members = get_members(group['id'])
        if len(set(list_friends) & set(list_members)) == 0:
            without_friends_group.append({'name': group['name'], 'gid': group['id'],
            'members_count': len(list_members)})
        print('-', end='', flush=True)
        time.sleep(1)
    return without_friends_group

def write_file(dict_group):
    with open('vk_groups.json', 'w') as f:
        json.dump(dict_group, f, indent=2, ensure_ascii=False)
        print('ok')

write_file(get_group_without_friends())


