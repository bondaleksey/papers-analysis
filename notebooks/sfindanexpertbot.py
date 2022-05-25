import config 
import telebot
 
from sbotfunctions import BotMenu

menu = BotMenu()
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):    
    # text = menu.to_main_menu_state()
    markup = menu.generate_menu_markup()
    bot.send_message(message.chat.id, "Привет ✌️\n", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def reaction_to_all_messages(message):        
    if message.text.lower() == config.STOPWORD:
        # menu.to_main_menu_state()        
        markup = menu.generate_menu_markup()
        bot.send_message(message.chat.id, "I'm stopping",reply_markup=markup)
        bot.stop_polling()
        return
    else:
        try:
            if message.text in menu.main_menu_text:
                # bot.register_next_step_handler(message, process_buttons)
                state = menu.main_menu_text.index(message.text)     
                if state == 0:
                    msg = bot.send_message(message.chat.id, menu.main_menu_text_reaction(message.text))                           
                    bot.register_next_step_handler(msg , process_search_by_keywords)                    
                elif state == 1:
                    msg = bot.send_message(message.chat.id, menu.main_menu_text_reaction(message.text))                           
                    bot.register_next_step_handler(msg , process_search_by_surname)                                    
                else:
                    markup = menu.generate_menu_markup()
                    bot.send_message(message.chat.id, menu.main_menu_text_reaction(message.text),reply_markup=markup)                    
            else:
                markup = menu.generate_menu_markup()
                bot.send_message(message.chat.id, menu.menu_default_text,reply_markup=markup)
                # bot.register_next_step_handler(msg, process_buttons)
        except Exception as e:
            markup = menu.generate_menu_markup()
            bot.send_message(message.chat.id, 'oooops\n'+ menu.menu_default_text,reply_markup=markup)            

def process_search_by_keywords(message):    
    markup = menu.generate_menu_markup()
    output = menu.search_by_keywords(message.text)
    bot.send_message(message.chat.id, output,reply_markup=markup)            
    
def process_search_by_surname(message):    
    markup = menu.generate_menu_markup()
    output = menu.search_by_surname(message.text)
    bot.send_message(message.chat.id, output,reply_markup=markup)                                    

if __name__ == '__main__':
    bot.infinity_polling(interval=0, timeout=5)