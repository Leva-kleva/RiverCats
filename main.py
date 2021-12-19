import telebot
from conf import *
import data
import response

bot = telebot.TeleBot(tg_token)
users = {}


@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, data.answers["start"])

    if users.get(message.chat.id) is None: users[message.chat.id] = {}
    users[message.chat.id] = {"last_cmd": "start", "interactive": None}

    keyboard = response.menu()
    bot.send_message(message.chat.id, "Выбирай!", reply_markup=keyboard)


@bot.message_handler(commands=["help"])
def cmd_start(message):
    users[message.chat.id] = {"last_cmd": "help"}
    bot.send_message(message.chat.id, data.answers["help"])


@bot.message_handler(content_types=["location"])
def location(message):
    cmd = users[message.chat.id]["last_cmd"]
    data.text_cmd["location"][cmd](bot, message, users[message.chat.id])


@bot.message_handler(content_types=["text"])
def other_messages(message):
    if data.text_cmd["text"].get(message.text):
        users[message.chat.id] = {"last_cmd": message.text,}
        users[message.chat.id] = data.text_cmd["text"][message.text](bot, message, users[message.chat.id])
    elif data.text_cmd["text_hidden"].get(message.text):
        users[message.chat.id] = data.text_cmd["text_hidden"][message.text](bot, message, users[message.chat.id])
    else:
        bot.send_message(message.chat.id, data.answers["not found"])


@bot.callback_query_handler(func=lambda call: True)
def callback_messages(call):
    def do_keyboard(number_slide, max_num):
        keyboard = telebot.types.InlineKeyboardMarkup()
        if number_slide == 0:
            buttons = ["next",]
        elif number_slide == max_num-1:
            buttons = ["back",]
        else:
            buttons = ["back", "next"]
        for text_button in buttons:
            button = telebot.types.InlineKeyboardButton(text=text_button, callback_data=text_button)
            print(text_button)
            keyboard.add(button)
        return keyboard

    def do_text(info, n):
        name = ""
        # print(info)
        i = 0
        for el in info.keys():
            # print(el)
            if i == n:
                name = el
                break
            i += 1
        text = ""
        text += name+"\n\n"
        text += f"{info[name]['Ссылка']}\n\n"
        text += f"{info[name]['Информация']}"
        return text

    if call.message:
        if users[call.message.chat.id]["view_route"]["routes"] is None:
            users[call.message.chat.id]["view_route"]["routes"] = call.data
            users[call.message.chat.id]["view_route"]["current_slide"] = 0
        if call.data == "next":
            users[call.message.chat.id]["view_route"]["current_slide"] += 1
        elif call.data == "back":
            users[call.message.chat.id]["view_route"]["current_slide"] -= 1
        keyboard = do_keyboard(users[call.message.chat.id]["view_route"]["current_slide"],
                               len(data.routes[users[call.message.chat.id]["view_route"]["routes"]]))
        n = users[call.message.chat.id]["view_route"]["current_slide"]
        info = data.routes[users[call.message.chat.id]["view_route"]["routes"]]#[n]

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=do_text(info, n),
                         reply_markup=keyboard)


if __name__ == "__main__":
    bot.polling(none_stop=True)
