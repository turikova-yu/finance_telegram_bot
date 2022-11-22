from dotenv import load_dotenv
import os
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import database.db_handler as db
from config import bot_text
import time
import graph_generator
import pie_generator

tconv = lambda x: time.strftime("%d.%m.%Y", time.localtime(x)) # Конвертация даты в читаемый вид

load_dotenv('.env')
bot = TeleBot(token=os.getenv('TELEGRAM_TOKEN'))

def register_user(user_name : str, chat_id : int) -> None:
    db.get_cursor(f"""
    INSERT INTO
    USERS (NAME, TELEGRAMID)
    VALUES ('{user_name}', {chat_id});
    """)

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    user_name = message.from_user.full_name
    message_text = bot_text['welcome_msg'].format(user_name)
    bot.send_message(message.chat.id, message_text)
    
    if not find_user(chat_id):
        register_user(user_name, chat_id)

# Категория сумма комментарий
# Продукты: 250.54 Купил продукты на неделю

@bot.message_handler(commands=['stats'])
def get_stats(message):

    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, 
        one_time_keyboard=True, 
        row_width=1
    )

    year_stat_button = KeyboardButton(text=bot_text['year_stat_button'])
    category_stat_button = KeyboardButton(text=bot_text['category_stat_button'])

    keyboard.add(year_stat_button)
    keyboard.add(category_stat_button)


    bot.send_message(message.chat.id, bot_text["stats_message"], reply_markup=keyboard)


def parse_user_message(message : str) -> bool:
    try:
        words = message.split()
        category = words[0].replace(':', "")
        money = words[1]
        index = message.index(money) + len(money) + 1
        comment = message[index:]
        money = float(money) 

        query = f"""
        SELECT * FROM CATEGORIES WHERE NAME = "{category}";
        """
        cur = db.get_cursor(query).fetchone()
    
        if cur:
            return (cur[0], money, comment)
        raise Exception()
    except:
         return None

@bot.message_handler(commands=['add'])
def add_operation(message):
    user_name = message.from_user.full_name
    message_text = bot_text['register_operation']
    bot.send_message(message.chat.id, message_text)

def find_user(id : int) -> int:
    results = db.get_cursor(f"""
    SELECT ID
    FROM USERS
    WHERE TELEGRAMID = {id};
    """)
    if results:
        return results.fetchone()[0]
    return None

@bot.message_handler(content_types=['text'])
def get_user_answer(message):
    user_name = message.from_user.full_name
    chat_id = message.chat.id
    user_id = find_user(chat_id)
   
    if bot_text['year_stat_button'] == message.text:
        graph_generator.bars_by_year()
        with open('pic.png', 'rb') as pic:
            photo = pic.read()
        bot.send_photo(
            chat_id=chat_id, 
            photo=photo, 
            caption=bot_text['your_graph_ready']
        )
        return

    if bot_text['category_stat_button'] == message.text:
        pie_generator.pie_by_categories()
        with open('pie.png', 'rb') as pic:
            photo = pic.read()
        bot.send_photo(
            chat_id=chat_id, 
            photo=photo, 
            caption=bot_text['your_graph_ready']
        )
        return
    
    if not user_id: return
    data = parse_user_message(message=message.text)
    date = message.date
    if data:
        query = f"""
        INSERT INTO 
        OPERATIONS (USERID, CATEGORYID, DATE, MONEY, COMMENT)
        VALUES ({user_id}, {data[0]}, "{tconv(date)}", {data[1]}, "{data[2]}");
        """
        db.get_cursor(query=query)
        message_text = bot_text['success_parse']
    else:
        message_text = bot_text['fail_parse']

    bot.send_message(chat_id, message_text)



bot.polling(non_stop=True)