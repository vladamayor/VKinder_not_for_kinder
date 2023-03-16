import requests
from random import randrange
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from db.db_VKtinder import issues_candidate


def write_msg(vk_session, user_id, message, keyboard=None, attachments=None):
    post = {"user_id": user_id, "message": message, "random_id": randrange(10**7)}
    if attachments != None:
        post["attachment"] = attachments
    elif keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    vk_session.method("messages.send", post)


def send_candidate(vk_session, TOKEN, data, user_id, candidate):
    keyboard = VkKeyboard(one_time=True)
    buttons = ["Нравится", "Дальше", "Избранные"]
    buttons_color = [
        VkKeyboardColor.POSITIVE,
        VkKeyboardColor.PRIMARY,
        VkKeyboardColor.SECONDARY,
    ]
    for btn, btn_color in zip(buttons, buttons_color):
        keyboard.add_button(btn, btn_color)
    keyboard.add_line()
    buttons = ["Стоп", "Новый запрос"]
    buttons_color = [VkKeyboardColor.NEGATIVE, VkKeyboardColor.PRIMARY]
    for btn, btn_color in zip(buttons, buttons_color):
        keyboard.add_button(btn, btn_color)
    id_candidate, fio, link = issues_candidate(data["user_id"])
    user_photo = candidate.find_most_popular(data, vk_session)
    write_msg(vk_session, user_id, f"{fio} \n {link}", keyboard)
    write_msg(vk_session, user_id, " ", keyboard, user_photo)
    info_candidate = (id_candidate, fio, link)
    return id_candidate, info_candidate


def search_city(city):
    BASE_HOST = "https://api.vk.com/"
    URI = "method/database.getCities"
    URL = BASE_HOST + URI
    city_params = {
        "access_token": os.getenv("access_token_app"),
        "v": "5.131",
        "q": city,
    }

    req = requests.get(URL, params=city_params).json()
    city_id = req["response"]["items"][0]["id"]
    return city_id


def collect_data(data, user_id, dict_data):
    dict_data["user_id"] = user_id
    age = int(data[0])
    dict_data["age_from"] = age - 3
    dict_data["age_to"] = age + 3
    if data[1] == "жен":
        dict_data["sex"] = 2
    else:
        dict_data["sex"] = 1
    city = data[2].title()
    dict_data["city_id"] = search_city(city)


def search_name(user_id):
    BASE_HOST = "https://api.vk.com/"
    URI = "method/users.get"
    URL = BASE_HOST + URI
    user_params = {
        "access_token": os.getenv("access_token_app"),
        "v": "5.131",
        "user_ids": user_id,
    }
    req = requests.get(URL, params=user_params).json()
    name = req["response"][0]["first_name"]
    return name
