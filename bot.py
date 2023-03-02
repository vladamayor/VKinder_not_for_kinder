import vk_api
import requests
from random import randrange
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

vk_session = vk_api.VkApi(token=os.getenv('access_token_community'))

longpoll = VkLongPoll(vk_session)

def write_msg(user_id, message, keyboard=None):
    post = {'user_id': user_id, 
            'message': message,
            'random_id': randrange(10 ** 7)
    }
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post

    vk_session.method('messages.send', post)



dict_data = {}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        user_id = event.user_id
        text = event.text.lower()

        if text == 'привет' or text == 'здравствуйте' or text == 'здравствуй':
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Старт', VkKeyboardColor.POSITIVE)
            write_msg(user_id, f'Приветик! Показать что я умею? Жми на "Старт"', keyboard)

        elif text == 'старт':
            write_msg(user_id, 'Могу показать тех, кто тебе подходит. \n\
                    Напиши через пробел: \n 1. Возраст \n 2. Пол (муж/жен) \n 3. Город', keyboard)


        elif text.split()[1] == 'жен' or 'муж':
            data = text.split()
            data[2].title()
            dict_data['id'] = user_id
            dict_data['params'] = data

            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Поехали!', VkKeyboardColor.POSITIVE)
            write_msg(user_id, 'Отлично! Уже ищу подходящих собеседников! Если готов, жми "Поехали!"', keyboard)
            break

print(dict_data)

dict_data
            


            
            
# elif text == 'выход':
#     write_msg(user_id, 'Пока, приходи еще!')
#     break

# buttons = ['Поехали!', 'Выход']
# buttons_color = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE] 
# for btn, btn_color in zip(buttons, buttons_color):
#     keyboard.add_button(btn, btn_color)