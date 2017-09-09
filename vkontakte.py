import requests
import time
import json

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.65'
VK_API = 'https://api.vk.com/method/'

user_name = 'tim_leary'
user_id = None
token = None

params = {
    'access_token': token,
    'v': VERSION,
    'user_id': user_id,
    }


def get_members(group_id):
    params['group_id'] = group_id
    return requests.get(VK_API + 'groups.getMembers', params).json()['response']['items']


def get_user_groups(id, extended):
    params['user_id'] = id
    params['extended'] = extended
    return requests.get(VK_API + 'groups.get', params).json()['response']['items']


def get_group_without_friends():
    list_friends = requests.get(VK_API + 'friends.get', params).json()['response']['items']
    time.sleep(1)
    list_friends_groups = []
    for friend in list_friends:
        try:
            list_friends_groups.extend(get_user_groups(friend, 0))
        except KeyError:
            pass
        print('- . ', end='', flush = True)
        time.sleep(1)
    without_friends_group = list(set(get_user_groups(user_id, 0)) - set(list_friends_groups))
    return without_friends_group


def get_group_data():
    list_groups = get_group_without_friends()
    list_out = []
    for group in list_groups:
        group_id = group
        params1 = {
            'access_token': token,
            'v': VERSION,
            'group_id': str(group_id),
        }
        group_info = requests.get(VK_API + 'groups.getById', params1).json()['response']
        list_out.append({'name': group_info[0]['name'], 'gid': group_info[0]['id'],
                         'members_count': len(get_members(group))})
    return list_out


def write_file(dict_group):
    with open('vk_groups.json', 'w') as f:
        json.dump(dict_group, f, indent=2, ensure_ascii=False)
        print('ok')

write_file(get_group_data())





