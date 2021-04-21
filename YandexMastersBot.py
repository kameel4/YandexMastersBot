from telegram.ext import *
import json
from CheckFunctions import *

updater = Updater('1676363369:AAHYqAQ2MxbytBdBPJkvtAxx1FwqBSzoXKw', use_context=True)
dp = updater.dispatcher
joinedFile = open('info/joined.txt', 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()


def main():
    updater.start_polling()
    updater.idle()


def set_timetable(update, context):
    if check_teacher(update.message.from_user.id):
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
        with open('info/history.txt', 'a', encoding='UTF-8') as history:
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


def add_teacher(update, context):
    password = context.args[0]
    name = context.args[1]
    if password == 'deadline':
        with open('info/teachers.txt', 'a', encoding='UTF-8') as teachers:
            teachers.write(f'{name} {update.message.from_user.id}\n')
    else:
        update.message.reply_text('Ты не учитель, пшел вон отсюда')


dp.add_handler(CommandHandler("set_timetable", set_timetable))
dp.add_handler(CommandHandler("timetable", timetable))
dp.add_handler(CommandHandler("bell", bell))
dp.add_handler(CommandHandler("add_teacher", add_teacher))

if __name__ == '__main__':
    main()
