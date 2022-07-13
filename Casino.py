import telebot
import time
from config import token

cash = int(1000)  # начальный баланс
result_Prise = int(0)  # начальная ставка
bot = telebot.TeleBot(token)  # токен для Бота(указывается в файле config)


@bot.message_handler(commands=['start'])
def command_start(message):
    stic = open('sticker.webp', 'rb')
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    start_markup.row('/Баланс', '/credits')
    start_markup.row('/Ставка')
    start_markup.row('/casic')

    bot.send_sticker(message.chat.id, stic, reply_markup=start_markup)


@bot.message_handler(commands=['Баланс'])
def command_cash(message):
    money = bot.send_message(message.chat.id, cash)


@bot.message_handler(commands=['credits'])
def command_credit(message):
    global cash
    cash += 1000
    balance = bot.send_message(message.chat.id, 'Ваш баланс пополнен на 1000')


@bot.message_handler(commands=['Ставка'])
def handle_text(message):
    cid = message.chat.id
    Stavka = bot.send_message(cid, 'Введите ставку:')
    bot.register_next_step_handler(Stavka, step_Set_Price)


def step_Set_Price(message):
    global result_Prise
    cid = message.chat.id
    userPrice = message.text
    if userPrice.isdigit() == True:

        stvk = bot.send_message(cid, 'Ваша ставка:')
        stvk1 = bot.send_message(cid, userPrice)
        result_Prise = int(userPrice)

    else:
        msgErr = bot.send_message(cid, 'Введи число!')
    return result_Prise


@bot.message_handler(commands=['casic'])
def command_casic(message):
    global cash
    global result_Prise

    if cash >= result_Prise and result_Prise > 0:

        value = bot.send_dice(message.chat.id, emoji='🎰')
        win = [1, 22, 43, 64]

        x = value.dice.value

        if x in win:

            cash = cash + (54 * result_Prise)
            bot.send_message(message.chat.id, "Вы выиграли!!! \nБаланс пополнен на:")
            bot.send_message(message.chat.id, 5 * result_Prise)

        else:
            cash = cash - result_Prise
            bot.send_message(message.chat.id, "Вы проиграли \nВаш баланс:")
            bot.send_message(message.chat.id, cash)

        print(value.dice.value, value.chat.username, cash)

    else:
        bot.send_message(message.chat.id, "Пополни баланс или измени ставку")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
