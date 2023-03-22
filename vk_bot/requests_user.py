from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
import requests
from vk_api import VkUpload
from db.db_VKtinder import adding_data_candidates
from db.db_VKtinder import issues_id_candidate


class VKUser:
    URL = "https://api.vk.com/method/"

    def __init__(self, token):
        self.params = {"access_token": token, "v": "5.131"}

    def find_users(self, data):
        user_url = self.URL + "users.search"
        user_params = {
            "count": 1000,
            "has_photo": 1,
            "age_from": data["age_from"],
            "age_to": data["age_to"],
            "sex": data["sex"],
            "city_id": data["city_id"],
        }
        req = requests.get(user_url, params={**self.params, **user_params})
        if req.status_code != 200:
            print("Ошибка при поиске пользователей", req.json())
        else:
            return req.json()["response"]["items"]

    def findandsave_users(self, data):
        req = self.find_users(data)
        user_base = data["user_id"]
        for user in req:
            if user["is_closed"] == False:
                base_user_host = "https://vk.com/id"
                candidate = [user["first_name"], user["last_name"]]
                fio = " ".join(candidate)
                user_id = user["id"]
                link = base_user_host + str(user_id)
                adding_data_candidates(user_id, fio, link, user_base)


    def get_photo(self, data):
        user_id = data["user_id"]
        id_candidate = issues_id_candidate(user_id)
        photo_url = self.URL + "photos.get"
        photos_params = {
            "owner_id": id_candidate,
            "album_id": "profile",
            "extended": "1",
            "count": 50,
        }
        req = requests.get(photo_url, params={**self.params, **photos_params}).json()

        return req

    def find_most_popular(self, data, vk_session, photo_count=3):
        upload = VkUpload(vk_session)
        req = self.get_photo(data)
        l_s_photo = []

        photos = [
            (photo["likes"]["count"], photo["sizes"][-1]["url"])
            for photo in req["response"]["items"]
        ]
        if req["response"]["count"] > photo_count:
            top_photos = sorted(photos)[
                len(photos) : len(photos) - (photo_count + 1) : -1
            ]
        else:
            top_photos = photos
        for url in top_photos:
            image = requests.get(url[1], stream=True)
            att_photo = upload.photo_messages(photos=[image.raw])[0]
            attachment = "photo{}_{}".format(att_photo["owner_id"], att_photo["id"])
            l_s_photo.append(attachment)

        return ",".join(l_s_photo)
