import config 
import telebot
 
from botfunctions import BotMenu

menu = BotMenu()
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):    
    text = menu.from_undermenu_to_main_menu()
    markup = menu.generate_menu_markup()
    bot.send_message(message.chat.id, "Привет ✌️\n"+text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def reaction_to_all_messages(message):        
    if message.text.lower() == config.STOPWORD:
        menu.from_undermenu_to_main_menu()        
        markup = menu.generate_menu_markup()
        bot.send_message(message.chat.id, "I'm stopping",reply_markup=markup)
        bot.stop_polling()
        return       
    if menu.inmain:        
        if message.text in menu.main_menu_text:            
            output_result = menu.main_menu_reaction(message.text)
            markup = menu.generate_undermenu_markup()
            bot.send_message(message.chat.id, output_result,reply_markup=markup)            
        else:            
            markup = menu.generate_menu_markup()
            bot.send_message(message.chat.id, menu.menu_default_text, reply_markup=markup)
    else:
        if message.text in menu.undermenu_text:            
            output_text = menu.from_undermenu_to_main_menu()
            markup = menu.generate_menu_markup()
            bot.send_message(message.chat.id, output_text, reply_markup=markup)            
        else:
            markup = menu.generate_undermenu_markup()
            output_result = menu.under_menu_reaction(message.text)            
            bot.send_message(message.chat.id, output_result, reply_markup=markup)                        

if __name__ == '__main__':
    bot.infinity_polling(interval=0, timeout=5)