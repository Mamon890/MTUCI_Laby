import telebot
from telebot import types
import psycopg2, datetime

token = "###"
bot = telebot.TeleBot(token)

conn = psycopg2.connect(
    database="BIN2202",
    user="postgres",
    password="###",
    host="localhost",
    port="5432")
cur = conn.cursor()
cur.execute('SET search_path TO main;')

asd = '____________________________________'


def get_week1(day, str1):
    cur.execute(
        "SELECT subject.name, week1.room_numb, week1.time, teacher.full_name FROM subject, teacher, week1 WHERE week1.wday = %s and week1.subject = subject.name and teacher.subject = subject.name",
        (day))
    data = cur.fetchall()
    res = ''
    m = 1
    for row in data:
        res = res + '\n' + str(m) + '. ' + str(row)
        m += 1
    res = str1 + '\n' + asd + '\n' + res + '\n' + asd + '\n'
    res = res.replace('(', '')
    res = res.replace(')', '')
    res = res.replace("'", '')

    return res


def get_week2(day, str1):
    cur.execute(
        "SELECT subject.name, week2.room_numb, week2.time, teacher.full_name FROM subject, teacher, week2 WHERE week2.wday = %s and week2.subject = subject.name and teacher.subject = subject.name",
        (day))
    data = cur.fetchall()
    res = ''
    for row in data:
        res = res + '\n' + str(row)
    res = str1 + '\n' + asd + '\n' + res + '\n' + asd + '\n'
    res = res.replace('(', '')
    res = res.replace(')', '')
    res = res.replace("'", '')

    return res


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.max_row_keys = 3
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Расписание на текущую неделю",
                 "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Здравствуйте, если хотите посмотреть расписание, нажмите на одну из кнопок ниже',
                     reply_markup=keyboard)


@bot.message_handler(commands=['week'])
def week(message):
    week = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month,
                         datetime.datetime.now().day).isocalendar().week
    if week % 2 == 0:
        ans = "Нижняя неделя"
    else:
        ans = "Верхняя неделя"
    bot.send_message(message.chat.id, f"{ans}")


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, "Официальный сайт МТУСИ – https://mtuci.ru/")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     'Я - бот, отображающий расписание для группы БИН2022. Мои команды:\n'
                     '/help - Отображение этого сообщения\n'
                     '/mtuci - Ссылка на сайт МТУСИ\n'
                     '/week - Узнать, сейчас верхняя или нижняя неделя\n'
                     'Для отображения расписания нажимайте на кнопки под полем ввода сообщения')


@bot.message_handler(content_types=["text"])
def message_handler(message):
    week = (datetime.date(datetime.datetime.now().year, datetime.datetime.now().month,
                          datetime.datetime.now().day).isocalendar().week)
    if week % 2 == 0:
        if message.text == "Понедельник":   bot.send_message(message.chat.id, get_week2('1', message.text))
        elif message.text == "Вторник": bot.send_message(message.chat.id, get_week2('2', message.text))
        elif message.text == "Среда":   bot.send_message(message.chat.id, get_week2('3', message.text))
        elif message.text == "Четверг": bot.send_message(message.chat.id, get_week2('4', message.text))
        elif message.text == "Пятница": bot.send_message(message.chat.id, get_week2('5', message.text))
        elif message.text == "Суббота": bot.send_message(message.chat.id, get_week2('6', message.text))
        elif message.text == "Расписание на текущую неделю":
            bot.send_message(message.chat.id, get_week2('1', "Понедельник") + get_week2('2', "Вторник") + get_week2('3',"Среда") + get_week2(
                '4', "Четверг") + get_week2('5', "Пятница") + get_week2('6', 'Суббота'))
        elif message.text == "Расписание на следующую неделю":
            bot.send_message(message.chat.id, get_week1('1', "Понедельник") + get_week1('2', "Вторник") + get_week1('3',"Среда") + get_week1(
                '4', "Четверг") + get_week1('5', "Пятница") + get_week1('6', 'Суббота'))
        else:
            bot.send_message(message.chat.id, 'Я не понимаю вашу команду')
    else:
        if message.text == "Понедельник":   bot.send_message(message.chat.id, get_week1('1', message.text))
        elif message.text == "Вторник": bot.send_message(message.chat.id, get_week1('2', message.text))
        elif message.text == "Среда":   bot.send_message(message.chat.id, get_week1('3', message.text))
        elif message.text == "Четверг": bot.send_message(message.chat.id, get_week1('4', message.text))
        elif message.text == "Пятница": bot.send_message(message.chat.id, get_week1('5', message.text))
        elif message.text == "Суббота": bot.send_message(message.chat.id, get_week1('6', message.text))
        elif message.text == "Расписание на текущую неделю":
            bot.send_message(message.chat.id, get_week1('1', "Понедельник") + get_week1('2', "Вторник") + get_week1('3',"Среда") + get_week1(
                '4', "Четверг") + get_week1('5', "Пятница") + get_week1('6', 'Суббота'))
        elif message.text == "Расписание на следующую неделю":
            bot.send_message(message.chat.id, get_week2('1', "Понедельник") + get_week2('2', "Вторник") + get_week2('3',"Среда") + get_week2(
'4', "Четверг") + get_week2('5', "Пятница") + get_week2('6', 'Суббота'))

        else:   bot.send_message(message.chat.id, 'Я не понимаю вашу команду')
bot.polling()
