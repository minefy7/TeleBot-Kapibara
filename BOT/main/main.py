from config import token
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

bot = TeleBot(token=token)

# TODO: Поставить ограничение параметрам до 100

name = 'Капибара'
energy = 70
satiety = 10
happiness = 100
coins = 500
meal = 5

def reset():
    global energy,satiety,happiness,coins,meal
    energy = 100
    satiety = 50
    happiness = 100
    coins = 500
    meal = 5




def stats(mess):
    global energy,satiety,happiness,coins,meal
    bot.send_message(mess.chat.id,f'энергия вашего питомца составляет {energy}')
    bot.send_message(mess.chat.id,f"сытость вашего питомца составляет {satiety}")
    bot.send_message(mess.chat.id,f'счастье вашего питомца составляет {happiness}')
    bot.send_message(mess.chat.id,f'кол-во ваших монет составляет {coins}')
    bot.send_message(mess.chat.id,f'кол-во еды для вашего питомца составляет {meal}')

user_states = {}

def check(mess: Message):
    global energy, satiety, happiness
    if satiety <= 0:
        bot.send_message(mess.chat.id,
                         f'{name}, умер от голода. Вы проиграли. P.S.: Не забывайте кормить своего питомца')
    elif satiety >= 100:
        bot.send_message(mess.chat.id, f'{name},наелся и счастлив')

    if energy <= 0:
        bot.send_message(mess.chat.id, f'{name}, устал и ничего не может делать, вы проиграли')
    elif energy >= 100:
        bot.send_message(mess.chat.id, f'{name},очень энергично себя чувствует, ему хочется играть')

    if happiness <= 0:
        bot.send_message(mess.chat.id, f'{name}, загрустил и впал в депрессию вы проиграли')
    elif happiness >= 100:
        bot.send_message(mess.chat.id, f'{name},очень счастлив')


def feed():
    global satiety, energy, meal
    satiety += 10
    energy += 5
    meal -= 1


def play():
    global satiety, happiness, energy
    satiety -= 5
    happiness += 10
    energy -= 10


def shop_button(mess):
    markup = ReplyKeyboardMarkup(row_width=3)
    itembtn1 = KeyboardButton('1')
    itembtn2 = KeyboardButton('2')
    itembtn3 = KeyboardButton('5')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(mess.chat.id, "Это магазин еды, сколько ты бы хотел купить? 1 шт - 50 монет", reply_markup=markup)

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     if message.text == '1':
#         bot.send_message(message.chat.id, "Ты выбрал 1")
#     elif message.text == '2':
#         bot.send_message(message.chat.id, "Ты выбрал 2")
#     elif message.text == '5':
#         bot.send_message(message.chat.id, "Ты выбрал 5")
#     else:
#         bot.send_message(message.chat.id, "Не правильный ввод")

@bot.message_handler(commands=['shop'])
def start_interaction(message):
    # Set the user's state to "awaiting_response"
    user_states[message.chat.id] = "awaiting_response"

    # Create a custom keyboard
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('1', callback_data='meal_1')
    button2 = InlineKeyboardButton('2', callback_data='meal_2')
    button3 = InlineKeyboardButton('5', callback_data='meal_5')
    markup.add(button1, button2, button3)

    # Send the keyboard to the user
    bot.send_message(message.chat.id, "Это магазин еды, сколько ты бы хотел купить? 1 шт - 50 монет", reply_markup=markup)

# Handler to process the user's response
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global meal,coins
    if call.data == 'meal_1':
        meal += 1
        coins -= 50
        if coins < 0:
            bot.answer_callback_query(call.id, 'Вы не смогли купить еду для питомца')
            meal -= 1
            coins += 50
        else:
            bot.answer_callback_query(call.id, 'Вы купили 1 еду для питомца')
    elif call.data == 'meal_2':
        meal += 2
        coins -= 100
        if coins < 0:
            bot.answer_callback_query(call.id, 'Вы не смогли купить еду для питомца')
            meal -= 2
            coins+= 100
        else:
            bot.answer_callback_query(call.id, 'Вы купили 2 еды для питомца')
    elif call.data == 'meal_5':
        meal += 5
        coins -= 250
        if coins < 0:
            bot.answer_callback_query(call.id, 'Вы не смогли купить еду для питомца')
            meal -= 5
            coins += 250
        else:
            bot.answer_callback_query(call.id, 'Вы купили 5 штучек еды для питомца')



def sleep():
    global satiety, energy, happiness
    satiety -= 5
    happiness -= 5
    energy = 100
@bot.message_handler(commands=['check_stats'])
def statisticks(mess):
    stats(mess)
    bot.send_message(mess.chat.id, 'Вот характеристики вашего питомца' )
@bot.message_handler(commands=['feed'])
def feed_handler(mess):
    feed()
    if meal <= 0:
        bot.send_message(mess.chat.id,
                         f'Вы не смогли покормить своего питомца, так как у вас нет еды.Купить еду можно по комманде /shop')
    else:
        bot.send_message(mess.chat.id, f'{name} вкусно поел и теперь его голод составляет {satiety}')
        check(mess)


@bot.message_handler(commands=['play'])
def play_handler(mess):
    play()
    bot.send_message(mess.chat.id, f'{name}, поиграл и теперь хочет спать, его счастье составляет {happiness}')
    check(mess)
@bot.message_handler(commands=['reset'])
def shop(mess):
    reset()


@bot.message_handler(commands=['sleep'])
def sleep_handler(mess):
    sleep()
    bot.send_message(mess.chat.id, f'{name}, поспал и теперь его энергия составляет {energy}')
    check(mess)

@bot.message_handler(commands=['start'])
def start(mess):
    bot.send_message(mess.chat.id, f'Я твой питомец, {name}')

@bot.message_handler(commands=['commands'])
def commands(mess):
    pass


# TODO: добавить список комманд


if __name__ == '__main__':
    bot.polling()