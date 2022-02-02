import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

import numpy as np
import gspread

from additional_functions import clean_users
from combinatios import *
from config import tg_bot_token, google_sheet_link
from conn import create_connection

import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineQueryResultArticle, Update, \
    InputTextMessageContent
from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
    InlineQueryHandler,
    CallbackContext,
)
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

STEP_3, STEP_4, STEP_5, STEP_6, STEP_7, STEP_8 = range(6)
STEP_10, STEP_11, STEP_12, STEP_13, STEP_14, STEP_15, STEP_16, STEP_17, STEP_18, STEP_19, STEP_20, STEP_21, GET_SOCIAL_LINK = range(13)


def start(update: Update, context: CallbackContext):
    reply_keys = [['Старт']]
    try:
        db = create_connection(sqlite3)
        cursor = db.cursor()
        sql = f"SELECT * FROM users_table WHERE chat_id = {update.message.chat.id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        db.close()
        if not result:
            update.message.reply_text(text=f"Привет! Я Психобот.\n"
                                           f"Я помогу тебе пройти тест на психотипы.\n"
                                           f"Тест определит твой психотип и роль в профессиональной команде,\n"
                                           f"которая лучше всего сочетается с твоими личными качествами и интересами.\n"
                                           f"Также он укажет, какие навыки и качества тебе необходимо развивать,\n"
                                           f"чтобы достигнуть заветных карьерных целей.\n\n"
                                           f"Чтобы начать тест, нажми кнопку “Старт”",
                                      reply_markup=ReplyKeyboardMarkup(reply_keys,
                                                                       resize_keyboard=True,
                                                                       one_time_keyboard=True),
                                      )
        else:
            update.message.reply_text(f"Привет! Ты уже проходил тест.")

    except sqlite3.Error as error:
        print("Ошибка подключения", error)

    return ConversationHandler.END


def name(update: Update, context: CallbackContext):
    try:
        db = create_connection(sqlite3)
        cursor = db.cursor()
        sql = f"SELECT * FROM users_table WHERE chat_id = {update.message.chat.id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        db.close()
        if not result:
            update.message.reply_text(f"В первой части теста я задам несколько личных вопросов:\n"
                                      f"про твое имя, возраст, город проживания и т.д.\n"
                                      f"Все это - твои персональные данные.\n"
                                      f"Я очень ценю, что ты доверишь их мне\n"
                                      f"и обязуюсь не передавать их третьим лицам.\n\n"
                                      f"Как тебя зовут? Мне достаточно имени.\n"
                                      f"Например: Иван")
            return STEP_3
        else:
            update.message.reply_text(f"Привет! Ты уже проходил тест.")
            return ConversationHandler.END

    except sqlite3.Error as error:
        print("Ошибка подключения", error)


def age(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    update.message.reply_text(f"Сколько тебе лет?\n"
                              f"Например: 25")
    return STEP_4


def city(update: Update, context: CallbackContext):
    context.user_data["age"] = update.message.text
    update.message.reply_text(f"В каком городе живешь?\n"
                              f"Например: Нижний Новгород")
    return STEP_5


def social_link(update: Update, context: CallbackContext):
    context.user_data["city"] = update.message.text
    answer_btns = [[InlineKeyboardButton(text='Инстаграмм', callback_data='Инстаграмм'),
                    InlineKeyboardButton(text='Фейсбук', callback_data='Фейсбук')],
                   [InlineKeyboardButton(text='Одноклассники', callback_data='Одноклассники'),
                    InlineKeyboardButton(text='Вконтакте', callback_data='Вконтакте')],
                   [InlineKeyboardButton(text='Никакой', callback_data='Никакой')]
                   ]
    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    update.message.reply_text(f"Какой социальной сетью ты пользуешься чаще всего?\n",
                              reply_markup=inline_keyboad,
                              parse_mode='HTML')
    return STEP_6


def real_income(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["social_net"] = query.data
    answer_btns = [[InlineKeyboardButton(text='меньше 100.000 руб.', callback_data='меньше 100.000 руб.'),
                    InlineKeyboardButton(text='101.000 - 200.000 руб.', callback_data='101.000 - 200.000 руб.')],
                   [InlineKeyboardButton(text='Больше 200.000 руб.', callback_data='Больше 200.000 руб.'),
                    InlineKeyboardButton(text='Не хочу говорить', callback_data='Не хочу говорить')]
                   ]
    inline_keyboad = InlineKeyboardMarkup(answer_btns)

    query.message.edit_text(f"Какой реальный доход сейчас у тебя (руб/мес)?",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    query.answer()
    return STEP_7


def wish_income(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["current_income"] = query.data
    answer_btns = [[InlineKeyboardButton(text='больше 100.000 руб.', callback_data='больше 100.000 руб.')],
                   [InlineKeyboardButton(text='больше 200.000руб.', callback_data='больше 200.000 руб.')],
                   ]
    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(f"Желаемый доход через 1 год (руб/мес)?\n"
                            f"Свой вариант можешь написать мне в сообщении.",
                            reply_markup=inline_keyboad,
                            )
    query.answer()
    return STEP_8


def test_start(update: Update, context: CallbackContext):
    reply_key = [["Поехали"]]
    mes_text = f"Теперь мы перейдем к основной части теста.\n" \
               f"Тебе будет предложено 12 блоков.\n" \
               f"В каждом блоке содержится 4 качества личности.\n" \
               f"Выбери то качество, которое наиболее точно характеризует тебя.\n\n" \
               f"В некоторых блоках тебе покажется, что подходят 2 и более вариантов ответа.\n" \
               f"Это нормально.\n" \
               f"Каждый из нас обладает многогранным характером.\n\n" \
               f"У меня есть подсказка, как выбрать правильный ответ:\n" \
               f"1. Отвечай быстро.\n" \
               f"Выбирай тот ответ, который откликнулся тебе сильней всего.\n" \
               f"2. Отвечай честно.\n" \
               f"Это не всегда просто, но полезно: только так ты узнаешь сильные и\n" \
               f"слабые стороны своей личности.\n\n" \
               f"Для продолжения нажми 'Поехали!' внизу 👇"

    if update.callback_query:
        query = update.callback_query
        context.user_data["wish_income"] = query.data
        query.message.delete()
        query.message.reply_text(text=mes_text,
                                 reply_markup=ReplyKeyboardMarkup(reply_key,
                                                                  resize_keyboard=True,
                                                                  one_time_keyboard=True),
                                 )
        query.answer()
    else:
        context.user_data["wish_income"] = update.message.text
        update.message.reply_text(text=mes_text,
                                  reply_markup=ReplyKeyboardMarkup(reply_key,
                                                                   resize_keyboard=True,
                                                                   one_time_keyboard=True),
                                  )
    return ConversationHandler.END


def q1(update: Update, context: CallbackContext):
    shuffle_q1 = np.random.permutation(q_1)
    answer_btns = []
    for row in shuffle_q1:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])
    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    try:
        db = create_connection(sqlite3)
        cursor = db.cursor()
        sql = f"SELECT * FROM users_table WHERE chat_id = {update.message.chat.id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        db.close()
        if not result:
            update.message.reply_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                           "Вопрос 1 из 12",
                                      reply_markup=inline_keyboad,
                                      parse_mode='HTML')
            return STEP_10
        else:
            update.message.reply_text(f"Привет! Ты уже проходил тест.")
        return ConversationHandler.END

    except sqlite3.Error as error:
        print("Ошибка подключения", error)


def q2(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer1"] = query.data
    shuffle_q2 = np.random.permutation(q_2)
    answer_btns = []
    for row in shuffle_q2:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 2 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_11


def q3(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer2"] = query.data
    shuffle_q3 = np.random.permutation(q_3)
    answer_btns = []
    for row in shuffle_q3:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 3 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_12


def q4(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer3"] = query.data
    shuffle_q4 = np.random.permutation(q_4)
    answer_btns = []
    for row in shuffle_q4:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 4 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_13


def q5(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer4"] = query.data
    shuffle_q5 = np.random.permutation(q_5)
    answer_btns = []
    for row in shuffle_q5:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 5 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_14


def q6(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer5"] = query.data
    shuffle_q6 = np.random.permutation(q_6)
    answer_btns = []
    for row in shuffle_q6:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 6 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_15


def q7(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer6"] = query.data
    shuffle_q7 = np.random.permutation(q_7)
    answer_btns = []
    for row in shuffle_q7:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 7 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_16


def q8(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer7"] = query.data
    shuffle_q8 = np.random.permutation(q_8)
    answer_btns = []
    for row in shuffle_q8:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 7 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_17


def q9(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer8"] = query.data
    shuffle_q9 = np.random.permutation(q_9)
    answer_btns = []
    for row in shuffle_q9:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 9 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_18


def q10(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer9"] = query.data
    shuffle_q10 = np.random.permutation(q_10)
    answer_btns = []
    for row in shuffle_q10:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 10 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_19


def q11(update: Update, context: CallbackContext):
    query = update.callback_query

    context.user_data["answer10"] = query.data

    shuffle_q11 = np.random.permutation(q_11)
    answer_btns = []
    for row in shuffle_q11:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Вопрос 11 из 12",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_20


def q12(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer11"] = query.data
    shuffle_q12 = np.random.permutation(q_12)
    answer_btns = []
    for row in shuffle_q12:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Выбери качество, которое наиболее точно характеризует тебя:\n"
                                 "Последний вопрос",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_21


def final(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["answer12"] = query.data
    answers = [context.user_data['answer1'],
               context.user_data['answer2'],
               context.user_data['answer3'],
               context.user_data['answer4'],
               context.user_data['answer5'],
               context.user_data['answer6'],
               context.user_data['answer7'],
               context.user_data['answer8'],
               context.user_data['answer9'],
               context.user_data['answer10'],
               context.user_data['answer11'],
               context.user_data['answer12']]

    label_type, a_score, b_score, c_score, d_score, main_label = get_a_type(answers)

    query.message.delete()

    query.message.reply_text(text=get_desc_type(main_label),
                             parse_mode="HTML")
    query.message.reply_text(text='Пришли ссылку на твою соц. сеть',
                             parse_mode="HTML")
    query.answer()

    return GET_SOCIAL_LINK


def get_social_link(update: Update, context: CallbackContext) -> None:
    context.user_data["social_link"] = update.message.text
    update.message.reply_text(text='Спасибо!',
                              parse_mode="HTML")
    chat_id = update.message.chat.id
    answers = [context.user_data['answer1'],
               context.user_data['answer2'],
               context.user_data['answer3'],
               context.user_data['answer4'],
               context.user_data['answer5'],
               context.user_data['answer6'],
               context.user_data['answer7'],
               context.user_data['answer8'],
               context.user_data['answer9'],
               context.user_data['answer10'],
               context.user_data['answer11'],
               context.user_data['answer12']
               ]

    label_type, a_score, b_score, c_score, d_score, main_label = get_a_type(answers)

    ts = time.localtime()
    date = time.strftime("%d.%m.%y %H:%M", ts)  # 29.01.22 10:40
    data = [context.user_data["name"],
            context.user_data["age"],
            context.user_data["city"],
            context.user_data["social_link"],
            context.user_data["current_income"],
            context.user_data["wish_income"],
            str(answers),
            str(label_type),
            a_score,
            b_score,
            c_score,
            d_score,
            main_label,
            date,
            context.user_data["social_net"]]

    try:
        gc = gspread.service_account(filename='credentials_polbza.json')
        sh = gc.open_by_key(google_sheet_link)
        worksheet = sh.sheet1
        worksheet.append_row(data)
    except Exception as error:
        print("Ошибка подключения Гугл таблице", error)

    try:
        db = create_connection(sqlite3)
        cursor = db.cursor()
        sql = f"INSERT INTO users_table(" \
              f"chat_id, name, age, city, social_link, current_income, wish_income, answers," \
              f"label_type, a_score, b_score, c_score, d_score, main_label, date, active, social_net)" \
              f"VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(sql, (chat_id,
                             context.user_data["name"],
                             context.user_data["age"],
                             context.user_data["city"],
                             context.user_data["social_link"],
                             context.user_data["current_income"],
                             context.user_data["wish_income"],
                             str(answers), str(label_type), a_score, b_score, c_score, d_score, main_label,
                             date, 1,
                             context.user_data["social_net"],
                             )
                       )
        db.commit()
        db.close()
    except sqlite3.Error as error:
        print("Ошибка подключения Sqlite", error)

    context.user_data.clear()
    return ConversationHandler.END


def profile_search(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    results = []
    key_word = query.split(":")[1].strip().lower()
    try:
        database = create_connection(sqlite3)
        cursor_key = database.cursor()
        sql_key = f'SELECT chat_id, name, age, city, social_link,' \
                  f'current_income, wish_income, label_type FROM users_table WHERE main_label = ? AND active = 1'
        cursor_key.execute(sql_key, (key_word,))
        records = cursor_key.fetchall()
        if records:
            for row in records:
                keyboad = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=f'Отправить в архив', callback_data=f'archive.{row[0]}')],
                    [InlineKeyboardButton(text=f'Написать пользователю: Привет.', callback_data=f'dialog.{row[0]}')],
                ])
                results.append(
                    InlineQueryResultArticle(id=row[0],
                                             title=f"{row[1]}",
                                             description=f"{key_word}: {row[1]}, {row[2]} лет, {row[3]}",
                                             input_message_content=InputTextMessageContent(
                                                 message_text=f"{key_word.upper()}\n\n"
                                                              f"<b>Имя:</b> {row[1]}\n"
                                                              f"<b>Возраст:</b> {row[2]}\n"
                                                              f"<b>Город:</b> {row[3]}\n"
                                                              f"<b>Ссылка на профиль:</b> {row[4]}\n"
                                                              f"<b>Текущий доход:</b> {row[5]}\n"
                                                              f"<b>Желаемый доход:</b> {row[6]}\n\n"
                                                              f"<b>Результаты теста:</b> {row[7]}",
                                                 parse_mode="HTML"
                                             ),
                                             reply_markup=keyboad,
                                             ),
                )
        else:
            results = [InlineQueryResultArticle(id='None',
                                                title=f"{key_word}",
                                                description='Ничего не найдено',
                                                input_message_content=InputTextMessageContent(
                                                    message_text=f"Ничего не найдено")
                                                )
                       ]
    except sqlite3.Error as error:
        print("ПРОБЛЕМА С ЗАБОРОМ ТОВАРОВ НА СКЛАДЕ", error)

    update.inline_query.answer(results)
    return ConversationHandler.END


def get_a_user(update: Update, context: CallbackContext):
    query = update.callback_query
    current_user_id = query.from_user.id
    user_id = query.data.split('.')[1]
    if 'archive' in query.data:

        try:
            db = create_connection(sqlite3)
            cursor = db.cursor()
            sql1 = f"UPDATE users_table SET active = 0 WHERE chat_id = ? "
            cursor.execute(sql1, (user_id,))
            db.commit()
            db.close()
        except sqlite3.Error as error:
            print("Ошибка подключения 1", error)

        context.bot.send_message(chat_id=current_user_id, text=f'Запись о пользователе отправлена в архив.\n'
                                                               f'Теперь она доступна только в Google Таблицах',
                                 parse_mode="HTML")
    else:
        context.bot.send_message(chat_id=user_id, text='Привет.')
    query.answer()
    return ConversationHandler.END


def dont_know(update: Update, context: CallbackContext):
    update.message.reply_text(text=f'<b>Извини, не понимаю тебя.</b>\n',
                              parse_mode="HTML")
    return ConversationHandler.END


def error(update: Update, context):
    # записывает что пошло не так
    logging.error(f'Апдейт {update}, причина ошибки {context.error}')


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_users, 'interval', days=7)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    updater = Updater(tg_bot_token)
    dp = updater.dispatcher
    dp.add_handler(CallbackQueryHandler(get_a_user, pattern='^' + str('.*archive.*|.*dialog.*') + '$'))
    dp.add_handler(InlineQueryHandler(profile_search, pattern='^' + str('.*Поиск:.*') + '$'))
    dp.add_handler(MessageHandler(Filters.regex('.*start.*'), start))

    dialog = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('.*Старт.*'), name)],
        states={STEP_3: [MessageHandler(Filters.text, age)],
                STEP_4: [MessageHandler(Filters.text, city)],
                STEP_5: [MessageHandler(Filters.text, social_link)],
                STEP_6: [CallbackQueryHandler(real_income)],
                STEP_7: [CallbackQueryHandler(wish_income)],
                STEP_8: [MessageHandler(Filters.text, test_start),
                         CallbackQueryHandler(test_start)]
                },
        fallbacks=[ConversationHandler.END]
    )

    dialog2 = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('.*Поехали.*'), q1)],
        states={STEP_10: [CallbackQueryHandler(q2, pattern='^' + str('.*a1.*|.*b1.*|.*c1.*|.*d1.*') + '$')],
                STEP_11: [CallbackQueryHandler(q3, pattern='^' + str('.*a2.*|.*b2.*|.*c2.*|.*d2.*') + '$')],
                STEP_12: [CallbackQueryHandler(q4, pattern='^' + str('.*a3.*|.*b3.*|.*c3.*|.*d3.*') + '$')],
                STEP_13: [CallbackQueryHandler(q5, pattern='^' + str('.*a4.*|.*b4.*|.*c4.*|.*d4.*') + '$')],
                STEP_14: [CallbackQueryHandler(q6, pattern='^' + str('.*a5.*|.*b5.*|.*c5.*|.*d5.*') + '$')],
                STEP_15: [CallbackQueryHandler(q7, pattern='^' + str('.*a6.*|.*b6.*|.*c6.*|.*d6.*') + '$')],
                STEP_16: [CallbackQueryHandler(q8, pattern='^' + str('.*a7.*|.*b7.*|.*c7.*|.*d7.*') + '$')],
                STEP_17: [CallbackQueryHandler(q9, pattern='^' + str('.*a8.*|.*b8.*|.*c8.*|.*d8.*') + '$')],
                STEP_18: [CallbackQueryHandler(q10, pattern='^' + str('.*a9.*|.*b9.*|.*c9.*|.*d9.*') + '$')],
                STEP_19: [CallbackQueryHandler(q11, pattern='^' + str('.*a10.*|.*b10.*|.*c10.*|.*d10.*') + '$')],
                STEP_20: [CallbackQueryHandler(q12, pattern='^' + str('.*a11.*|.*b11.*|.*c11.*|.*d11.*') + '$')],
                STEP_21: [CallbackQueryHandler(final, pattern='^' + str('.*a12.*|.*b12.*|.*c12.*|.*d12.*') + '$')],
                GET_SOCIAL_LINK: [MessageHandler(Filters.text, get_social_link)],
                },
        fallbacks=[ConversationHandler.END]
    )
    dp.add_handler(dialog)
    dp.add_handler(dialog2)

    if_not_via = '(?!^ИСКАТЕЛЬ|СОЗИДАТЕЛЬ|СТРАТЕГ|КОММУНИКАТОР|Ничего не найдено)(^.*$)'
    dp.add_handler(MessageHandler(Filters.regex(if_not_via), dont_know))

    dp.add_error_handler(error)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
