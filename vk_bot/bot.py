import vk_api
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_bot.bot_function import write_msg, collect_data, search_name




vk_session = vk_api.VkApi(token=os.getenv('access_token_community'))
longpoll = VkLongPoll(vk_session)


answer = ['привет', 'старт']

dict_data = {}
def get_info():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            text = event.text.lower()
            name = search_name(user_id)

            if text in answer or text.split()[1] == 'жен' or 'муж':

                if text == 'привет':
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Старт', VkKeyboardColor.POSITIVE)
                    write_msg(vk_session, user_id, f'Приветик, {name}! Показать что я умею? Жми на "Старт"', keyboard)

                elif text == 'старт':
                    write_msg(vk_session, user_id, 'Могу показать тех, кто тебе подходит. \n\
                            Напиши через пробел: \n 1. Возраст \n 2. Пол (муж/жен) \n 3. Город')


                elif text.split()[1] == 'жен' or 'муж':
                    data = text.split()
                    collect_data(data, user_id, dict_data)

                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Поехали!', VkKeyboardColor.POSITIVE)
                    write_msg(vk_session, user_id, 'Отлично! Уже ищу подходящих собеседников! Если готов, жми "Поехали!"', keyboard)
                    break

            else:
                write_msg(vk_session, user_id, 'По-инопланетному пока не умею.. но я учусь')
    return dict_data


  





            
            
# elif text == 'выход':
#     write_msg(user_id, 'Пока, приходи еще!')
#     break

# buttons = ['Поехали!', 'Выход']
# buttons_color = [VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE] 
# for btn, btn_color in zip(buttons, buttons_color):
#     keyboard.add_button(btn, btn_color)