import vk_api
import requests
from random import randrange
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token=os.getenv('access_token_community'))

longpoll = VkLongPoll(vk_session)

def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

list_data = []


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                user_id = event.user_id
                text = event.text.lower()

                if text == 'привет' or text == 'здравствуйте' or text == 'здравствуй':
                    write_msg(user_id, f'Приветик! Показать что я умею?')

                elif text == 'да' or text == 'давай':
                    write_msg(user_id, 'Могу показать тех, кто тебе подходит. \n\
                            Напиши через пробел: \n 1. Возраст \n 2. Пол (муж/жен) \n 3. Город')

                elif text.split()[1] == 'жен' or 'муж':
                    data = text.split()
                    write_msg(user_id, 'Отлично! Уже ищу подходящих собеседников!')
                    list_data.append(data)
                    
                elif text == 'пока' or text == 'нет':
                    write_msg(user_id, f'До скорого, приходи еще!')

                else:
                    write_msg(user_id, 'Не понял, повторите еще раз, пожалуйста')
    except:
        pass

        
print(list_data)