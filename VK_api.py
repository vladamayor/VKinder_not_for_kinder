import vk_api
from new import requests_user


class Vk_api:
    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token,'v': self.version}
        self.path = 'https://api.vk.com/method/'

    def get_users_info(self, user_id):#Формирует запрос на получение информации о пользователе
        method = 'users.get'
        url = self.path + method
        params = {'user_ids': user_id, 'fields': 'bdate,sex,city','v': '5.131'}
        result = requests.get(url, params={**self.params, **params})
        return result.json()

    def get_info_result(self,city,sex,age_to, age_from=18, count=1000):#формирует список ID подходящих по критериям ... персонажей
        method = 'users.search'
        url = self.path + method
        params = {'v': '5.131',
                  'fields': 'bdate,sex,city',
                  'city': city,
                  'count': count,
                  'sex': sex,
                  'age_to': age_to,
                  'age_from': age_from
                  }
        result = requests.get(url, params={**self.params, **params})
        # pprint(result.json()['response']['items'])
        if 'response' in result.json():
            inf_user = result.json()['response']['items']
            list_id = [users_id['id'] for users_id in inf_user]
            # pprint(result.json())
            return list_id

    def get_photo(self, owner_id):#Поиск 3,2,1 самых "залайканных" фото и формирование списка фотографий.
        dict_photo = {}
        method = 'photos.get'
        url = self.path + method

        params = {'album_id': 'profile',
                  'extended': 1,
                  'rev': 0,
                  'owner_id': owner_id,
                  'v': '5.131'}
        result = requests.get(url, params={**self.params, **params})
        if 'response' in result.json().keys() and len(result.json()['response']['items']) > 0 and 'error' not in result.json().keys():
            for photos in result.json()['response']['items']:
                dict_photo[photos['likes']['count'], photos['id']] = f"photo{photos['owner_id']}_{photos['id']}"

            list_send_photo = []
            if len(dict_photo) >= 3:
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 2]])
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 3]])

           # elif 1 < len(dict_photo) <= 2:
                #list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])
                #list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 2]])

           # elif 0 < len(dict_photo) <= 1:
               # list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])

            print(','.join(list_send_photo))
        #print(*list_send_photo)
            return ','.join(list_send_photo)

        elif 'response' in result.json().keys() and len(result.json()['response']['items']) == 0:
            # print SOMETHING
            return SOMETHING

        elif 'error' in result.json().keys():
            return SOMETHING


