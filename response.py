import random
import telebot, data


def menu():
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for text_button in data.text_cmd["text"].keys():
        button = telebot.types.KeyboardButton(text=text_button)
        keyboard.add(button)
    return keyboard


def echo(bot, call):
    bot.send_message(call.message.chat.id, call.data)


def find_flights(bot, message, user):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    button = telebot.types.KeyboardButton(text="Выслать геопозицию", request_location=True)
    keyboard.add(button)
    bot.send_message(message.chat.id, "Мне нужна твоя геолокация", reply_markup=keyboard)
    return user


def find_flightss(bot, message, user):
    # print(message.location)
    #TODO find flights and send info about flight
    text = "Ближайший причал: Киевский\nБлижайший рейс: теплоход 'RiverCats', отправление в 17:30, 300 руб."
    bot.send_message(message.chat.id, text)
    bot.send_location(message.chat.id, 55.743616, 37.571721)
    keyboard = menu()
    bot.send_message(message.chat.id, "Выбирай!", reply_markup=keyboard)
    return user


def go_interactive(bot, message, user):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    button = telebot.types.KeyboardButton(text="Выслать геопозицию", request_location=True)
    stop_button = telebot.types.KeyboardButton(text="Выключить гид")
    keyboard.add(button, stop_button)
    bot.send_message(message.chat.id, "Обнови геолокацию", reply_markup=keyboard)
    return user


def go_interactivee(bot, message, user):
    # TODO add find pier and send text about pier and flights
    text1 = "Сейчас ты проезжаешь мимо Парка Горького\n\nПарк Горького - самое популярное место отдыха москвичей. В основном площадка рассчитана на молодежную аудиторию, но здесь найдется развлечение для семейной прогулки и досуг для старших посетителей. Территория парка включает в себя партерную часть, Пушкинскую набережную и Нескучный сад, который переходит в Воробьевы горы. На сегодняшний день в парке имеется большое количество активностей: открыт велопрокат, установлены столы для настольного тенниса, оборудована самая большая песочница, открыт первый в стране кинотеатр под открытым небом. На территории всего парка имеется бесплатный доступ к Wi-Fi."
    text2 = "Оглянись и ты увидишь дом Музыки\n\nДом Музыки - один из крупнейших в России и мире филармонических комплексов, многофункциональный культурный центр, направленный на развитие современного исполнительского искусства. Дом музыки представляет собой десятиэтажное здание с трёхэтажным стилобатом и двухэтажным подвалом, уходящим на 6 метров под землю. Высота здания составляет более 46 метров. Общая площадь комплекса — около 42 000 квадратных метров. В четырёх залах Дома музыки — Светлановском, Камерном, Театральном и Новом ежедневно проходят выступления российских и зарубежных симфонических оркестров, камерных ансамблей, солистов-инструменталистов, артистов оперы и балета, театральных, джазовых, эстрадных и фольклорных коллективов, международные форумы и фестивали, творческие вечера и презентации, праздничные шоу и конференции."
    TEXT = [text2, text1]
    bot.send_message(message.chat.id, TEXT[random.randint(1,2)-1])
    bot.send_message(message.chat.id, "Не забывай обновлять геолокацию")
    return user


def stop_interactive(bot, message, user):
    bot.send_message(message.chat.id, data.answers["stop_interactive"])
    keyboard = menu()
    bot.send_message(message.chat.id, "Выбирай!", reply_markup=keyboard)
    return user


def get_routes(bot, message, user):
    user = {"last_cmd": message.text, "view_route": {"current_slide": None, "routes": None}}

    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    stop_button = telebot.types.KeyboardButton(text="Завершить просмотр")
    keyboard.add(stop_button)
    bot.send_message(message.chat.id, "Чтобы завершить просмотр нажмите кнопку 'Завершить просмотр'", reply_markup=keyboard)

    keyboard = telebot.types.InlineKeyboardMarkup()
    for text_button in data.routes.keys():
        button = telebot.types.InlineKeyboardButton(text=text_button, callback_data=text_button)
        keyboard.add(button)
    bot.send_message(message.chat.id, "Выбирай!", reply_markup=keyboard)
    return user
