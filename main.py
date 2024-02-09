import telebot
from telebot import types
import random
import functions
# Загрузка токена из переменных окружения
bot = telebot.TeleBot("6831587612:AAEUQ4m30-Pajetdnw0AwZ4omaNmzVkc-4o")

class PokemonBot:


    def __init__(self):
        # Словарь для хранения состояний пользователей
        self.states = {}

    def start(self, message):
        # Приветственное сообщение при старте
        bot.send_message(message.chat.id, f"Hi, {message.from_user.first_name}")
        self.show_go_buttons(message.chat.id)

    def handle_go_callback(self, call):
        chat_id = call.message.chat.id

        # Обработка нажатия кнопок "Go", "Keep going", "Skip"
        if call.data in ['go', 'keepgoing', 'skip']:
            # if call.data == 'keepgoing':
            #     bot.delete_message(call.message.chat.id, call.message.message_id)      # удаляет сообщение в котором было нажато "keepgoing"
            if random.choice([True, False]):
                self.states[chat_id] = 'choose_catch_or_skip'
                self.show_catch_or_skip_buttons(chat_id, call.message.message_id)
            else:
                self.states[chat_id] = 'choose_find_or_skip'
                self.back_to_start(chat_id, call.message.message_id)


        # Обработка нажатия кнопок "Catch", "Retry"
        elif call.data in ['catch', 'retry']:
            #bot.delete_message(call.message.chat.id, call.message.message_id)      #удаляет сообщение в котором было нажато catch или retry
            if random.choice([True, False]):
                self.states[chat_id] = 'choose_captured_or_retry'
                self.show_captured_or_retry_buttons(chat_id, call.message.message_id)
            else:
                self.states[chat_id] = 'choose_find_or_skip'
                self.show_captured_or_not_buttons(chat_id, call.message.message_id)

        # Обработка нажатия кнопки "Captured"
        elif call.data == 'captured':
            bot.send_message(chat_id, "Вы успешно поймали покемона!")

    def callback_handler(self, call):
        # Обработка команды "help"
        if call.data == 'help':
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, helpinfo)

    def show_go_buttons(self, chat_id):
        # Отправка кнопки "Go" для начала поиска покемона
        markup = types.InlineKeyboardMarkup()

        button_go = types.InlineKeyboardButton('Go', callback_data='go')
        markup.add(button_go)

        bot.send_message(chat_id, "Press 'Go' to start searching for a Pokemon:", reply_markup=markup)

    def back_to_start(self, chat_id, message_id):
        # Возвращение к начальному состоянию после неудачной попытки
        markup = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton('Keep going', callback_data='keepgoing')
        markup.add(button_back)
        bot.send_message(chat_id, 'You did not find anything', reply_markup=markup)
        #bot.delete_message(chat_id, message_id)

    def show_catch_or_skip_buttons(self, chat_id, message_id):
        # Отображение кнопок "Try to Catch" и "Skip" после успешной попытки
        markup = types.InlineKeyboardMarkup()
        button_catch = types.InlineKeyboardButton('Try to Catch', callback_data='catch')
        button_skip = types.InlineKeyboardButton('Skip', callback_data='skip')
        markup.add(button_catch, button_skip)

        # Отображение случайного покемона с весами
        chosen_pokemon = functions.pokemon_catch() #функция с вероятностями выпадения покемонов в файле functions.py
        pokemon_image = f'image/{chosen_pokemon.lower()}.png'
        with open(pokemon_image, 'rb') as pokemon_photo:
            sent_message = bot.send_photo(chat_id, pokemon_photo, caption=f"You found a {chosen_pokemon}! What would you like to do?", reply_markup=markup)

            self.states[chat_id] = {'message_id': sent_message.message_id, 'state': 'choose_catch_or_skip'}

    def show_captured_or_retry_buttons(self, chat_id, message_id):
        # Отображение кнопки "Keep going" после успешного захвата
        markup = types.InlineKeyboardMarkup()
        button_go = types.InlineKeyboardButton('Keep going', callback_data='go')
        markup.add(button_go)
        bot.send_message(chat_id, "You captured a Pokemon!", reply_markup=markup)
       
        #bot.delete_message(chat_id, message_id)

    def show_captured_or_not_buttons(self, chat_id, message_id):
        # Отображение кнопки "Try again" после неудачной попытки захвата
        markup = types.InlineKeyboardMarkup()
        button_try_again = types.InlineKeyboardButton('Try again', callback_data='catch')
        markup.add(button_try_again)
        bot.send_message(chat_id, 'Bad luck', reply_markup=markup)
        #bot.delete_message(chat_id, message_id)

    def run(self):
        # Запуск бота в режиме бесконечного опроса
        bot.infinity_polling()

# Если файл запущен напрямую (а не импортирован как модуль)
if __name__ == "__main__":
    # Создание экземпляра класса PokemonBot
    pokemon_bot = PokemonBot()

    # Обработчики сообщений и колбеков
    @bot.message_handler(commands=['start'])
    def start_wrapper(message):
        pokemon_bot.start(message)

    @bot.callback_query_handler(func=lambda call: call.data in ['go', 'keepgoing', 'skip', 'retry', 'catch'])
    def handle_go_callback_wrapper(call):
        markup = types.InlineKeyboardMarkup()
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        pokemon_bot.handle_go_callback(call)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler_wrapper(call):
        markup = types.InlineKeyboardMarkup()
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        pokemon_bot.callback_handler(call)

    # Запуск бота
    pokemon_bot.run()
