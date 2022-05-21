import config 
import telebot
# import pickle
from model import Model 

# import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

# import os

# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))

# filename = "data\\mnid_author_dict.pkl"
# with open(filename,'rb') as inp:
#     authors_dict = pickle.load(inp)
# ind = 0
# for k, v in authors_dict.items():
#     ind += 1
#     print(k,v)
#     if ind>4:
#         break

model = Model(path = 'data/')

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    if message.text == 'otus':
        bot.reply_to(message," i'm stopping")
        bot.stop_polling()
    else:
        print(message.text)
        # print(message.chat.id)
        # print(message.text)
        bot.send_message(message.chat.id, model.get_model_response(message.text))
    
if __name__ == '__main__':
    bot.infinity_polling()