from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
import requests
from vk_api import VkUpload
from db.db_VKtinder import adding_data_candidates
from db.db_VKtinder import issues_candidate


class VKUser:
    url = "https://api.vk.com/method/"

    def __init__(self, token):
        self.params = {"access_token": token, "v": "5.131"}

    def search_сandidates(self, data):
        search_сandidates_url = self.url + "users.search"
        candidates_params = {
            "count": 1000,
            "has_photo": 1,
            "age_from": data["age_from"],
            "age_to": data["age_to"],
            "sex": data["sex"],
            "city_id": data["city_id"],
        }
        req = requests.get(
            search_сandidates_url, params={**self.params, **candidates_params}
        ).json()
        return req["response"]["items"]

    def create_archive(self, data):
        req = self.search_сandidates(data)
        user_base = data["user_id"]
        for user in req:
            if user["is_closed"] == False:
                user_data = {}
                base_user_host = "https://vk.com/id"
                candidate = [user["first_name"], user["last_name"]]
                fio = " ".join(candidate)
                user_data["user"] = fio
                user_id = user["id"]
                user_data["link"] = base_user_host + str(user_id)
                link = base_user_host + str(user_id)
                adding_data_candidates(user_id, fio, link, user_base)

        return print("База создана")

    def get_candidate(self, data):
        user_id = data["user_id"]
        id_candidate = issues_candidate(user_id)
        get_candidate = self.url + "users.get"
        get_candidate_params = {"user_ids": id_candidate}

    def get_photo(self, data, vk_session):
        upload = VkUpload(vk_session)
        user_id = data["user_id"]
        id_candidate, fio, link = issues_candidate(user_id)
        get_photo_url = self.url + "photos.get"
        get_photos_params = {
            "owner_id": id_candidate,
            "album_id": "profile",
            "extended": "1",
            "count": 50,
        }
        req = requests.get(
            get_photo_url, params={**self.params, **get_photos_params}
        ).json()

        d_ph = {}
        l_s_photo = []

        if "response" in req.keys():
            if req["response"]["count"] == 0:
                l_s_photo.append("")
            else:
                for photos in req["response"]["items"]:
                    image_url = photos["sizes"][-1]["url"]
                    image = requests.get(image_url, stream=True)
                    photo = upload.photo_messages(photos=[image.raw])[0]
                    d_ph[photos["likes"]["count"]] = "photo{}_{}".format(
                        photo["owner_id"], photo["id"]
                    )
                    if req["response"]["count"] > 3:
                        sort_d_ph = dict(
                            sorted(d_ph.items(), key=lambda x: x[0])[
                                len(d_ph) : len(d_ph) - 4 : -1
                            ]
                        )
                        l_s_photo = list(sort_d_ph.values())

                    elif req["response"]["count"] <= 3:
                        l_s_photo = d_ph.values()

        else:
            pass

        return fio, link, ",".join(l_s_photo), id_candidate
