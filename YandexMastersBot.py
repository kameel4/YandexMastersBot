from telegram.ext import *
from telegram import *
import json
from datetime import datetime as dt
from CheckFunctions import *

updater = Updater('1676363369:AAHYqAQ2MxbytBdBPJkvtAxx1FwqBSzoXKw', use_context=True)
bot = Bot(token="1676363369:AAHYqAQ2MxbytBdBPJkvtAxx1FwqBSzoXKw")
dp = updater.dispatcher


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
    check_join(update.message.from_user.id)


def timetable(update, context):
    with open('info/timetable.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
        day = context.args[0]
    s = ''
    for i in data['week'][day]:
        s += i + '\n'
    file.close()
    update.message.reply_text(s)
    check_join(update.message.from_user.id)


def bell(update, context):
    with open('info/timetable.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
    s = ''
    for i in data['bell'].keys():
        s += f"{i} | {data['bell'][i]}\n"
    file.close()
    update.message.reply_text(s)
    check_join(update.message.from_user.id)


def add_teacher(update, context):
    password = context.args[0]
    name = " ".join(context.args[1:])
    if password == 'deadline':
        with open('info/teachers.txt', 'a', encoding='UTF-8') as teachers:
            teachers.write(f'{name} {update.message.from_user.id}\n')
        update.message.reply_text(f'Учитель {name} добавлен.')
    else:
        update.message.reply_text('Ты не учитель, пшел вон отсюда')
    check_join(update.message.from_user.id)


def send_messages(update, context):
    name = ''
    if check_teacher(update.message.from_user.id):
        for s in open('info/teachers.txt', encoding='UTF-8').readlines():
            if int(s.strip().split()[-1]) == update.message.from_user.id:
                name = ''.join(s[:-10])
        message = name + ': ' + ' '.join(context.args)
        with open('info/joined.txt', 'r') as joined:
            data = joined.readlines()
            for i in data:
                bot.send_message(text=message, chat_id=i)
    else:
        update.message.reply_text('Ты не учитель, пшел вон отсюда')


def add_marks(update, context):
    if check_teacher(update.message.from_user.id):
        try:
            marks = json.load(open('info/marks.json', 'r', encoding='UTF-8'))
        except Exception:
            marks = {}
        data = context.args
        pupil_name, half, subject, list_of_marks = data[0], data[1], data[2], data[3:]
        if pupil_name not in marks:
            marks[pupil_name] = {}
            marks[pupil_name]['1'] = {}
            marks[pupil_name]['2'] = {}
        if subject not in marks[pupil_name][half]:
            marks[pupil_name][half][subject] = []
        marks[pupil_name][half][subject] += list_of_marks
        json.dump(marks, open('info/marks.json', 'w', encoding='UTF-8'), ensure_ascii=False)
    else:
        update.message.reply_text('Ты не учитель, пшел вон отсюда')


def marks(update, context):
    access = []
    entered_name = context.args[0]
    half = context.args[1]
    answ = ''
    with open('info/marks.json', 'r', encoding="UTF-8") as marks_file:
        marks = json.load(marks_file)
    for teacher in open("info/teachers.txt", "r", encoding="UTF-8").readlines():
        access.append(int(teacher.strip().split()[-1]))
    for pupil in open("info/pupils.txt", "r", encoding="UTF-8").readlines():
        if entered_name == ' '.join(pupil.strip().split()[:-1]):
            access.append(int(pupil.strip().split()[-1]))
    if update.message.from_user.id in access:
        try:
            subjects = marks[entered_name][half]
        except Exception:
            update.message.reply_text("Нет такого бивня.")
            return True
        for subject in subjects.keys():
            answ += f"{subject}: {' '.join(marks[entered_name][half][subject])} ({average(marks[entered_name][half][subject])})\n"
        if not answ:
            update.message.reply_text("Нет оценок в этой четверти")
        update.message.reply_text(answ)
    else:
        update.message.reply_text("Отказано в доступе.")
        marks_file.close()


def add_pupil(update, context):
    name = context.args[0]
    id = update.message.from_user.id
    with open('info/pupils.txt', 'a', encoding="UTF-8") as pupils:
        pupils.write(f'{name} {id}\n')
    pupils.close()


def help(update, context):
    update.message.reply_text('''/set_timetable - Команда для установки расписания. 
    Синтаксис: /set_timetable <день недели> <предметы через пробел>
    -----------------------------------
    /timetable - Команда для просмотра расписания уроков.
    Синтаксис: /timetable <день недели>
    -----------------------------------
    /bell - Команда для просмотра расписания звонков
    Синтаксис: /bell
    -----------------------------------
    /add_teacher - Команда для добавления учителей (Только для учителей)
    Синтаксис: /add_teacher <пароль> <имя>
    -----------------------------------
    /send_messages - Команда для рассылки сообщений (Только для учителей)
    Синтаксис: /send_messages <текст сообщения>
    -----------------------------------
    /add_marks - Команда для добавления оценок в табель (Только для учителей)
    Синтаксис: /add_marks <имя ученика> <полугодие> <предмет> <оценки через пробел>
    -----------------------------------
    /add_pupil - Команда для добавления учеников
    Синтаксис: /add_pupil <имя>
    ----------------------------------------------------------------------
    /marks - Команда для просмтора табеля
    Синтаксис: /marks <имя> <полугодие цифрой 1 или 2>
    -----------------------------------
    /help - Список команд
    Синтаксис: /help''')


dp.add_handler(CommandHandler("set_timetable", set_timetable))
dp.add_handler(CommandHandler("timetable", timetable))
dp.add_handler(CommandHandler("bell", bell))
dp.add_handler(CommandHandler("add_teacher", add_teacher))
dp.add_handler(CommandHandler("send_message", send_messages))
dp.add_handler(CommandHandler("add_marks", add_marks))
dp.add_handler(CommandHandler("add_pupil", add_pupil))
dp.add_handler(CommandHandler("marks", marks))
dp.add_handler(CommandHandler("help", help))

if __name__ == '__main__':
    main()
