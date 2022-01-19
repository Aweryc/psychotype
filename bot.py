import numpy as np
from combinatios import *
from config import tg_bot_token
from conn import create_connection

import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
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

STEP_2, STEP_3, STEP_4, STEP_5, STEP_6, STEP_7, STEP_8, STEP_9, STEP_10, STEP_11, STEP_12, STEP_13, STEP_14, STEP_15, \
STEP_16, STEP_17, STEP_18, STEP_19, STEP_20, STEP_21 = range(20)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(f"Привет! Я проверяю наш персонал на психотип. 😎"
                              f"Если еще не проходил тест, тогда самое время это сделать!"
                              f""
                              f"Для продолжения, нажми /begin")
    return ConversationHandler.END


def name(update: Update, context: CallbackContext):
    update.message.reply_text(f"Пришли свои имя и фамилию ( в таком порядке 😉 )."
                              f"Например: Иван Смирнов")
    return STEP_3


def age(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    update.message.reply_text(f"Сколько тебе лет?")

    return STEP_4


def city(update: Update, context: CallbackContext):
    context.user_data["age"] = update.message.text
    update.message.reply_text(f"В каком городе проживаешь?")

    return STEP_5


def social_link(update: Update, context: CallbackContext):
    context.user_data["city"] = update.message.text
    update.message.reply_text(f"Скинь ссылку на личный аккаунт в соц.сетях 🙈")

    return STEP_6


def real_income(update: Update, context: CallbackContext):
    context.user_data["social_link"] = update.message.text
    update.message.reply_text(f"Какой реальный доход сейчас у тебя?")
    return STEP_7


def wish_income(update: Update, context: CallbackContext):
    context.user_data["current_income"] = update.message.text
    update.message.reply_text(f"Желаемый доход через 1 год?")
    return STEP_8


def test_start(update: Update, context: CallbackContext):
    context.user_data["wish_income"] = update.message.text
    inline_key = [["Поехали"]]
    update.message.reply_text(f"ОК! Начнем же тестирование!\n"
                              f"Помни, отвечать нужно в первую очередь честно для себя 😘\n"
                              f"В тесте представлены блоки качеств личности.\n"
                              f"Выбери в каждом блоке качество, наиболее характеризующее тебя.\n"
                              f"Всего будет 12 вопросов.\n\n"
                              f"Для продолжения нажми 'Поехали!' внизу 👇",
                              reply_markup=ReplyKeyboardMarkup(inline_key,
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
    update.message.reply_text(text="Что больше характеризует тебя?\n"
                                   "Вопрос 1 из 12",
                              reply_markup=inline_keyboad,
                              parse_mode='HTML')

    return STEP_10


def q2(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    context.user_data["answer1"] = query.data

    shuffle_q2 = np.random.permutation(q_2)
    answer_btns = []
    for row in shuffle_q2:
        answer_btns.append([InlineKeyboardButton(text=f'{row[1]}', callback_data=row[0])])

    inline_keyboad = InlineKeyboardMarkup(answer_btns)
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
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
    query.message.edit_text(text="Что больше характеризует тебя?\n"
                                 "Последний вопрос",
                            reply_markup=inline_keyboad,
                            parse_mode='HTML')
    return STEP_21


def final(update: Update, context: CallbackContext):
    print(update)
    query = update.callback_query
    chat_id = query.message.chat.id
    print(chat_id)
    context.user_data["answer12"] = query.data
    desc_type = f''
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
    # print(answers)
    label_type = get_a_type(answers)
    url_type = get_url_type(label_type)
    # print(label_type)
    # print(url_type)
    inline_keyboad = InlineKeyboardMarkup([[InlineKeyboardButton(text=f'Ссылка 🔗', url=url_type)]])

    try:
        db = create_connection(sqlite3)
        cursor = db.cursor()
        sql = f"INSERT INTO users_table(chat_id, name, age, city, social_link, current_income, wish_income, answers)" \
              f"VALUES(?,?,?,?,?,?,?,?)"
        cursor.execute(sql,
                       (chat_id,
                        context.user_data["name"],
                        context.user_data["age"],
                        context.user_data["city"],
                        context.user_data["social_link"],
                        context.user_data["current_income"],
                        context.user_data["wish_income"],
                        str(answers),))
        db.commit()
        db.close()
    except sqlite3.Error as error:
        print("Ошибка подключения", error)

    query.message.delete()
    query.message.reply_text(text=f'Твой психотип: {label_type}\n'
                                  f'Немного о твоем типе:\n'
    # f'{desc_type}'
                                  f'Кстати,можно перейди по ссылке ниже\n'
                                  f'для полной информации  👇',
                             reply_markup=inline_keyboad,

                             parse_mode="HTML")
    query.answer()
    context.user_data.clear()
    return ConversationHandler.END


def dont_know(update: Update, context: CallbackContext):
    update.message.reply_text(text=f'<b>Извини, не понимаю тебя.</b>\n',
                              # reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                              #                                  resize_keyboard=True,
                              #                                  one_time_keyboard=True,
                              #                                  ),
                              parse_mode="HTML")
    return ConversationHandler.END


def error(update: Update, context):
    # записывает что пошло не так
    logging.error(f'Апдейт {update}, причина ошибки {context.error}')


def main():
    updater = Updater(tg_bot_token)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.regex('.*start.*'), start))

    dialog = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('.*begin.*'), name)],
        states={STEP_3: [MessageHandler(Filters.text, age)],
                STEP_4: [MessageHandler(Filters.text, city)],
                STEP_5: [MessageHandler(Filters.text, social_link)],
                STEP_6: [MessageHandler(Filters.text, real_income)],
                STEP_7: [MessageHandler(Filters.text, wish_income)],
                STEP_8: [MessageHandler(Filters.text, test_start)]
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
                },
        fallbacks=[ConversationHandler.END]
    )
    dp.add_handler(dialog)
    dp.add_handler(dialog2)

    dp.add_handler(MessageHandler(Filters.text, dont_know))

    dp.add_error_handler(error)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
