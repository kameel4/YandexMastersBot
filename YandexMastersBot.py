from telegram.ext import *
import json
import telebot
from pprint import pprint
from datetime import datetime

updater = Updater('1676363369:AAHYqAQ2MxbytBdBPJkvtAxx1FwqBSzoXKw', use_context=True)
dp = updater.dispatcher
joinedFile = open('info/joined.txt', 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

bot = telebot.TeleBot('1676363369:AAHYqAQ2MxbytBdBPJkvtAxx1FwqBSzoXKw')


def main():
    timetable_handler = MessageHandler(Filters.text, set_timetable)
    # start_command_handler = CommandHandler('start', checkuserCommand)

    dp.add_handler(timetable_handler)
    updater.start_polling()

    updater.idle()


def set_timetable(update, context):
    if update.message.from_user.id == 988566680 or update.message.from_user.id == 641113946:
        with open('info/timetable.json', 'r', encoding='UTF-8') as file:
            data = json.load(file)
            day = context.args[0]
        timetable = context.args[1:]
        data['week'][day] = timetable
        file.close()
        with open('info/timetable.json', 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)
        file.close()
        update.message.reply_text('Расписание обновлено')
    else:
        update.message.reply_text('Отказано в доступе')
    # ===================Log================================================================
    if update.message.from_user.id == 988566680 or update.message.from_user.id == 641113946:
        with open('info/history.txt', 'w', encoding='UTF-8') as history:
            history.write(f"{update.message.from_user.first_name} изменил расписание.")
        history.close()


def timetable(update, context):
    with open('info/timetable.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
        day = context.args[0]
    s = ''
    for i in data['week'][day]:
        s += i + '\n'
    file.close()
    update.message.reply_text(s)


def bell(update, context):
    with open('info/timetable.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
    s = ''
    for i in data['bell'].keys():
        s += f"{i} | {data['bell'][i]}\n"
    file.close()
    update.message.reply_text(s)


@bot(commands=['start'])
def botMessage(message):
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("info/joined.txt", 'a')
        joinedFile.write(str(message.chat.id) + '\n')
        joinedUsers.add(message.chat.id)


@bot.message_handler(commands=['special'])
def botSpecial(message):
    for user in joinedUsers:
        bot.send_message(user, message.text[message.text.find(' '):])


# def checkuserCommand(bot, update):
#     if update.message.from_user.id == "Свой ID или список ID пользователей на доступ к боту":
#         if update.message.text == "Команда":
#             startCommand(bot, update)


dp.add_handler(CommandHandler("set_timetable", set_timetable))
dp.add_handler(CommandHandler("timetable", timetable))
dp.add_handler(CommandHandler("bell", bell))
# dp.add_handler(start_command_handler)

if __name__ == '__main__':
    main()
