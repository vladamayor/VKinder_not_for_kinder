#from bot import get_info
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import requests
from vk_api import VkUpload 
from vk_api import VkApi
import vk_api


#data = get_info()
#print(data)
#data = {'user_id': 787161190, 'age_from': 18, 'age_to': 26, 'sex': 2, 'city_id': 1}
#print(data)

# token = os.getenv('access_token_app')
# vk_session = vk_api.VkApi(token=os.getenv('access_token_community'))


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
    

    def create_archive(self, data, vk_session):
        req = self.search_сandidates(data)
        for item in req:
            user_data = {}
            base_user_host = 'https://vk.com/id'
            user = [item['first_name'] , item['last_name']]
            user_data['user'] = ' '.join(user)
            user_id = item['id']
            user_data['link'] = base_user_host + str(user_id)
            link = base_user_host + str(user_id)
            list_data.append(user_data)
            user_data['photos'] = self.get_photo(data, vk_session)
    
        return user, link



# Значение count временно 3, далее будет 1000

    def get_photo(self, data, vk_session):
        req = self.search_сandidates(data)
        upload = VkUpload(vk_session)
        for item in req:
            user_id = item['id']
            get_photo_url = self.url + 'photos.get'
            get_photos_params = {
                'owner_id': user_id,
                'album_id': 'profile',
                'extended': '1',
                'count': 2,
            }
            req = requests.get(get_photo_url, params={**self.params, **get_photos_params}).json()['response']
            
        d_ph={}
            
        for photos in req['items']:
            image_url = photos['sizes'][-1]['url']
            image = requests.get(image_url, stream=True)
            photo = upload.photo_messages(photos=image.raw)[0]
            d_ph[photos['likes']['count']] ='photo{}_{}'.format(photo['owner_id'], photo['id'])
            if len(req['items']) > 3 :
                sort_d_ph = dict(sorted(d_ph.items(), key=lambda x: x[0])[len(d_ph):len(d_ph)-4:-1])
                l_s_photo = list(sort_d_ph.values())
            else:
                l_s_photo = d_ph.values()

        return ','.join(l_s_photo)



# users = VKUser(token)
# print(users.get_photo(data, vk_session))
