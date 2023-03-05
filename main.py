import vk_api
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_bot.bot_function import write_msg, collect_data, search_name
from vk_bot.requests_user import VKUser
from vk_api import VkUpload 
import requests
from vk_bot.bot import get_info


data = get_info()
token = os.getenv('access_token_app')
users = VKUser(token)
vk_session = vk_api.VkApi(token=os.getenv('access_token_community'))
longpoll = VkLongPoll(vk_session)


answer_show = ['поехали!']


def show_info():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            text = event.text.lower()
            name = search_name(user_id)

            if text in answer_show:

                if text == 'поехали!':
                    keyboard = VkKeyboard()
                    buttons = ['Нравится', 'Дальше']
                    buttons_color = [VkKeyboardColor.POSITIVE, VkKeyboardColor.PRIMARY] 
                    for btn, btn_color in zip(buttons, buttons_color):
                        keyboard.add_button(btn, btn_color)
                    attachments = users.get_photo(data, vk_session)
                    user, link = users.create_archive(data, vk_session)
                    fio = ' '.join(user)
                    write_msg(vk_session, user_id, f'{fio} \n {link}', keyboard)
                    write_msg(vk_session, user_id, ' ', keyboard, attachments)
                    break  
    return print('ok')



show_info()

