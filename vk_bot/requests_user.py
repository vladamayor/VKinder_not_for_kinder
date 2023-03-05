#from bot import get_info
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import requests
from vk_api import VkUpload 
from vk_api import VkApi
import vk_api
from db.db_VKtinder import adding_data_candidates
from pprint import pprint


#data = get_info()
#print(data)
# data = {'user_id': 787161190, 'age_from': 30, 'age_to': 36, 'sex': 1, 'city_id': 42}
# #print(data)

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
                'count': 3,
                'has_photo': 1,
                'age_from': data['age_from'],
                'age_to': data['age_to'],
                'sex': data['sex'],
                'city_id': data['city_id'],
        }  
        req = requests.get(search_сandidates_url, params={**self.params, **candidates_params}).json()
        return req['response']['items']
        
    

    def create_archive(self, data, vk_session):
        req = self.search_сandidates(data)
        user_base = data['user_id']
        for user in req:
            if user['is_closed'] == False:
                    user_data = {}
                    base_user_host = 'https://vk.com/id'
                    candidate = [user['first_name'] , user['last_name']]
                    fio = ' '.join(candidate)
                    user_data['user'] = fio
                    user_id = user['id']
                    user_data['link'] = base_user_host + str(user_id)
                    link = base_user_host + str(user_id)
                    list_data.append(user_data)
                    user_photo = self.get_photo(data, vk_session)
                    user_data['photos'] = user_photo
                    adding_data_candidates(user_id, fio, link, user_photo, user_base)
            
        return fio, link



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
                'count': 5,
            }
            req = requests.get(get_photo_url, params={**self.params, **get_photos_params}).json()
            #pprint(req)
            
        d_ph={}
        l_s_photo = []

        if 'response' in req.keys():     
            for photos in req['response']['items']:
                image_url = photos['sizes'][-1]['url']
                image = requests.get(image_url, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]
                print(photo)
                d_ph[photos['likes']['count']] ='photo{}_{}'.format(photo['owner_id'], photo['id'])
                if len(req['response']['items']) > 3 :
                    sort_d_ph = dict(sorted(d_ph.items(), key=lambda x: x[0])[len(d_ph):len(d_ph)-4:-1])
                    l_s_photo = list(sort_d_ph.values())
                else:
                    l_s_photo = d_ph.values()

        else:
            pass

        return ','.join(l_s_photo)



# users = VKUser(token)
# pprint(users.create_archive(data, vk_session))
# print(list_data)
