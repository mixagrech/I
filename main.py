import telebot
from telebot import types
from telebot.types import WebAppInfo
import time
from datetime import datetime, timedelta
import pickle
import os

bot = telebot.TeleBot('7804303855:AAEJEORGTo9qq6E2lewLjm4vwg2N1oEwNBM')

# Файл для хранения данных
DATA_FILE = 'user_data.pkl'


# Загрузка данных из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as f:
            return pickle.load(f)
    return {
        'unique_users': set(),
        'total_count': 0,
        'last_reset_date': datetime.now(),
        'monthly_count': 0
    }


# Сохранение данных в файл
def save_data(data):
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)


# Инициализация данных
user_data = load_data()


# Проверка и обновление уникальных пользователей
def update_user_stats(user_id):
    global user_data
    user_added = False

    if user_id not in user_data['unique_users']:
        user_data['unique_users'].add(user_id)
        user_data['total_count'] += 1
        user_data['monthly_count'] += 1
        user_added = True
        save_data(user_data)
        print(
            f"Новый уникальный пользователь! Всего пользователей: {user_data['total_count']} (за месяц: {user_data['monthly_count']})")

    # Проверка, нужно ли сбросить месячную статистику
    if datetime.now() - user_data['last_reset_date'] >= timedelta(days=30):
        print(f"Сбрасываем месячную статистику. Было {user_data['monthly_count']} пользователей за месяц.")
        user_data['monthly_count'] = 0
        user_data['last_reset_date'] = datetime.now()
        save_data(user_data)

    return user_added


@bot.message_handler(commands=['start'])
def start(message):
    # Обновляем статистику пользователей
    update_user_stats(message.from_user.id)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Начать играть🛶",
                                          web_app=WebAppInfo(url='https://mixagrech.github.io/rowlivefgfmkskefker/')))
    button1 = types.InlineKeyboardButton("Комьюнити", url='https://t.me/ROWlive')
    button2 = types.InlineKeyboardButton("🎓Как играть?", callback_data='test')
    markup.add(button1, button2)
    bot.send_photo(message.chat.id, open('dfgfdd.png', 'rb'),
                   '\n Привет, {0.first_name}!👋 \n\nДобро пожаловать в ROW-LIVE!\n\n🎮Играй в мини-игру каждый день 💰Зарабатывай $ROW\n✨Получай NFT-бонусы за друзей\n\n5 приглашённых людей = 1 NFT!'.format(
                       message.from_user), reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # Обновляем статистику пользователей
    update_user_stats(callback.from_user.id)

    markup2 = types.InlineKeyboardMarkup()
    buttonwhatgame1 = types.InlineKeyboardButton("Начать играть🛶", web_app=WebAppInfo(
        url='https://mixagrech.github.io/rowlivefgfmkskefker/'))
    buttonwhatcommunity = types.InlineKeyboardButton("Комьюнити", url='https://t.me/ROWlive')
    markup2.add(buttonwhatgame1, buttonwhatcommunity)
    if callback.data == 'test':
        bot.send_message(callback.message.chat.id, (
            '1. Запускай игру\n2. Приглашай друзей ( 5 друзей = 1 NFT\n3. NFT увеличивают твой доход\n4. Зарабатывай $ROW ежедневно\n\nЧем реже NFT - тем больше бонус! 🚀'),
                         reply_markup=markup2)


# Выводим начальную статистику при запуске
print(f"Бот запущен. Всего уникальных пользователей: {user_data['total_count']}")
print(f"Пользователей за текущий месяц: {user_data['monthly_count']}")
print(f"Следующий сброс статистики: {user_data['last_reset_date'] + timedelta(days=30)}")

bot.polling(none_stop=True)
