import vk_api
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_bot.bot_function import write_msg, send_candidate, search_name, collect_data
from vk_bot.requests_user import VKUser
from db.db_VKtinder import (
    deleted_candidate,
    adding_data_favorites,
    adding_data_candidates,
    issues_favorite,
    adding_data_user,
    deleted_candidate_all,
)


token = os.getenv("access_token_app")
vk_session = vk_api.VkApi(token=os.getenv("access_token_community"))
longpoll = VkLongPoll(vk_session)
candidate = VKUser(token)


def get_info():
    data = {}
    candidate_id_list = []
    list_info_candidate = []
    answer_get = [
        "привет",
        "старт",
        "поехали!",
        "дальше",
        "нравится",
        "избранные",
        "стоп",
        "новый запрос",
        "назад",
    ]

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            text = event.text.lower()

            if (
                text in answer_get
                or text.count(" ") > 0
                and text.split()[1] in ["муж", "жен"]
            ):
                if text == "привет":
                    name = search_name(user_id)
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button("Старт", VkKeyboardColor.POSITIVE)
                    write_msg(
                        vk_session,
                        user_id,
                        f'Приветик, {name}! Показать что я умею? Жми на "Старт"',
                        keyboard,
                    )

                elif text == "старт":
                    adding_data_user(user_id)
                    write_msg(
                        vk_session,
                        user_id,
                        "Могу показать тех, кто тебе подходит. \n\
                            Напиши через пробел: \n 1. Возраст \n 2. Пол (муж/жен) \n 3. Город",
                    )

                elif text == "поехали!":
                    candidate.create_archive(data)
                    candidate_id, info_candidate = send_candidate(
                        vk_session, token, data, user_id, candidate
                    )
                    candidate_id_list.append(candidate_id)
                    list_info_candidate.append(info_candidate)

                elif text == "дальше":
                    deleted_candidate(candidate_id_list.pop())
                    candidate_id, first_last_name, link = list_info_candidate.pop()
                    adding_data_candidates(candidate_id, first_last_name, link, user_id)
                    candidate_id, info_candidate = send_candidate(
                        vk_session, token, data, user_id, candidate
                    )
                    candidate_id_list.append(candidate_id)
                    list_info_candidate.append(info_candidate)

                elif text == "нравится":
                    candidate_id, first_last_name, link = list_info_candidate.pop()
                    adding_data_favorites(
                        candidate_id_list[0], first_last_name, link, user_id
                    )
                    deleted_candidate(candidate_id_list.pop())
                    candidate_id, info_candidate = send_candidate(
                        vk_session, token, data, user_id, candidate
                    )
                    candidate_id_list.append(candidate_id)
                    list_info_candidate.append(info_candidate)

                elif text == "избранные":
                    result = issues_favorite(user_id)
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button("Назад", VkKeyboardColor.PRIMARY)
                    if not result:
                        write_msg(vk_session, user_id, "Список пуст", keyboard)
                    for item in result:
                        write_msg(
                            vk_session, user_id, f"{item[0]}, {item[1]}", keyboard
                        )

                elif text == "назад":
                    send_candidate(vk_session, token, data, user_id, candidate)

                elif text == "новый запрос":
                    candidate_id_list.clear()
                    list_info_candidate.clear()
                    deleted_candidate_all(user_id)
                    write_msg(
                        vk_session,
                        user_id,
                        "Могу показать тех, кто тебе подходит. \n\
                             Напиши через пробел: \n 1. Возраст \n 2. Пол (муж/жен) \n 3. Город",
                    )

                elif text == "стоп":
                    name = search_name(user_id)
                    write_msg(vk_session, user_id, f"Пока, приходи еще, {name}!")
                    break

                elif text.split()[1] == "жен" or "муж":
                    user_data = text.split()
                    collect_data(user_data, user_id, data)

                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button("Поехали!", VkKeyboardColor.POSITIVE)
                    write_msg(
                        vk_session,
                        user_id,
                        'Отлично! Уже ищу подходящих собеседников! Если готов, жми "Поехали!"',
                        keyboard,
                    )

            else:
                write_msg(
                    vk_session, user_id, "По-инопланетному пока не умею.. но я учусь"
                )

    return print("ok")


get_info()
