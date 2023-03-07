import vk_api
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_bot.bot_function import write_msg, send_candidate
from vk_bot.requests_user import VKUser
from vk_api import VkUpload 
import requests
from vk_bot.bot import get_info
from db.db_VKtinder import deleted_candidate, adding_data_favorites



data = get_info()
token = os.getenv('access_token_app')
vk_session = vk_api.VkApi(token=os.getenv('access_token_community'))
longpoll = VkLongPoll(vk_session)
candidate = VKUser(token)


answer_show = ['поехали!', 'дальше', 'нравится']

candidate_id_list = []

def show_info():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            text = event.text.lower()
            

            if text in answer_show:

                if text == 'поехали!':
                    candidate.create_archive(data, vk_session)
                    candidate_id = send_candidate(vk_session, token, data, user_id, candidate)
                    candidate_id_list.append(candidate_id)
                    

                if text == 'дальше':
                    deleted_candidate(candidate_id_list.pop())
                    candidate_id = send_candidate(vk_session, token, data, user_id, candidate)

                    candidate_id_list.append(candidate_id)
                    
                if text == 'нравится':
                    fio, link, user_photo, candidate_id = candidate.get_photo(data, vk_session)
                    adding_data_favorites(candidate_id_list[0], fio, link, user_photo, user_id )
                    deleted_candidate(candidate_id_list.pop())
                    candidate_id = send_candidate(vk_session, token, data, user_id, candidate)
                    candidate_id_list.append(candidate_id)
                    break


    return print('ok')



show_info()

