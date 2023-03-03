from vk_bot.bot import get_info
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import requests
from pprint import pprint


data = {'user_id': 787161190, 'age_from': 18, 'age_to': 26, 'sex': 1, 'city_id': 1}
#print(data)

token = os.getenv('access_token_app')
list_data = []

class VKUser():
    url = 'https://api.vk.com/method/'
    def __init__(self,token):
        self.params = {
            'access_token': token,
            'v': '5.131'
        }
        
# Значение count временно 1, далее будет 1000

    def search_сandidates(self, data):
        search_сandidates_url = self.url + 'users.search'
        candidates_params = {
                'count': 1,
                'has_photo': 1,
                'age_from': data['age_from'],
                'age_to': data['age_to'],
                'sex': data['sex'],
                'city_id': data['city_id']
        }  
        req = requests.get(search_сandidates_url, params={**self.params, **candidates_params}).json()
        return req['response']['items']
    

    def create_archive(self, data):
        req = self.search_сandidates(data)
        for item in req:
            user_data = {}
            base_user_host = 'https://vk.com/id'
            user = [item['first_name'] , item['last_name']]
            user_data['user'] = ' '.join(user)
            user_id = item['id']
            user_data['link'] = base_user_host + str(user_id)
            list_data.append(user_data)


# Значение count временно 3, далее будет 1000

    def get_photo(self, data):
        req = self.search_сandidates(data)
        for item in req:
            user_id = item['id']
            get_photo_url = self.url + 'photos.get'
            get_photos_params = {
                'owner_id': user_id,
                'album_id': 'profile',
                'extended': '1',
                'count': 3,
            }
            req = requests.get(get_photo_url, params={**self.params, **get_photos_params}).json()['response']
            pprint(req)







users = VKUser(token)
print(users.get_photo(data))
#print(list_data)