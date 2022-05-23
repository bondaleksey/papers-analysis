import config 
import telebot
# import pickle
 
from botfunctions import BotMenu
from datetime import datetime

menu = BotMenu()
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    # bot.send_message(message.chat.id,"Привет ✌️ ")
    print('5 I am here ')
    markup = menu.generate_menu_markup()
    bot.send_message(message.chat.id, "Привет ✌️\n"+menu.menu_default_text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):    
    print(message.from_user)
    # print(message.from_user.first_name, message.from_user.last_name, message.from_user.username)    
    print(datetime.utcfromtimestamp(message.date))    
    print(message.text)
    print("inmain = ", menu.inmain)
    print("undermain = ",menu.undermain)
    if message.text.lower() == 'otus':
        bot.reply_to(message," i'm stopping")
        bot.stop_polling()
        return 
    if menu.inmain:        
        if message.text in menu.main_menu_text:
            print('1 I am here ')
            output_result = menu.main_menu_reaction(message.text)
            markup = menu.generate_undermenu_markup()
            bot.send_message(message.chat.id, output_result,reply_markup=markup)
            # сделать кнопку возврата в главное меню 
        else:
            print('2 I am here ')
            markup = menu.generate_menu_markup()
            bot.send_message(message.chat.id, menu.menu_default_text, reply_markup=markup)
    else:
        if message.text in menu.undermenu_text:
            print('3 I am here ')
            output_text = menu.from_undermenu_to_main_menu()
            markup = menu.generate_menu_markup()
            bot.send_message(message.chat.id, output_text, reply_markup=markup)            
        else:
            markup = menu.generate_undermenu_markup()
            output_result = menu.under_menu_reaction(message.text)
            # print(output_result)
            # print(type(output_result))
            print('4 I am here ')
            bot.send_message(message.chat.id, output_result, reply_markup=markup)            
            # bot.send_message(message.chat.id, output_result)  


if __name__ == '__main__':
    bot.infinity_polling(interval=0, timeout=5)