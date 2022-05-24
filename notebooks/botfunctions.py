
from telebot import types
import random 
from model import Model
from os.path import exists


if exists('../data/'):
    model = Model()
elif exists('data/'):
    model = Model(path = 'data/')
else:
    print("You don't have folder with pkl files")
    exit(131)



class BotMenu():
    
    def __init__(self): #, inmenu=True)
        self.inmain = True
        self.undermain = -1
        self.main_menu_text = ['поиск по ключевым словам', 'поиск по фамилии', 'информация о боте', 'контакты']
        self.undermenu_text = ['перейти в главное меню']
        self.menu_default_text = "Выберите действие:"
        self.funny_answers=['Чего еще желаете?', 'Ну что тебе?','Может в главное меню?', 'Пора в главное меню ...']
                    
    def generate_menu_markup(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for item in self.main_menu_text:
            itembt = types.KeyboardButton(item)
            markup.add(itembt)
        return markup
    
    def generate_undermenu_markup(self):
        # markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for item in self.undermenu_text:
            itembt = types.KeyboardButton(item)
            markup.add(itembt)                    
        return markup
    
    def main_menu_reaction(self,button_text):
        # print('i see you put this button:',button_text)
        self.undermain = self.main_menu_text.index(button_text)        
        self.inmain = False
        return self.get_undermenu_reply()
    
    def get_undermenu_reply(self):
        text = ['Введите ключевые слова для поиска. Например: "Суперкомпьютерное моделирование","MPI","openMP", "GPU", "параллельные алгоритмы", "системы дифференциальных уравнений"',
                'Введите фамилию автора',
                '''Бот находит сотрудников ИПМ им. М.В. Келдыша по аннотациям их публикаций из открытых источников.\nЗамечание 1. Рейтинг авторов - условная величина, отображающая частоту слов поиска в аннотациях его работ. \nЗамечание 2. Приводимые статьи не исчерпывают всех работ авторов, так как в данном боте поиска представлена лишь часть работ.''',
                '''Вопросы  и предложения отправляете на почту: yabondaleksey@yandex.ru''']
        return text[self.undermain]
    
    def from_undermenu_to_main_menu(self):
        self.undermain = -1
        self.inmain = True
        return self.menu_default_text
    
    def under_menu_reaction(self, text):
        # self.undermain = -1
        # self.inmain = True
        if self.undermain == 0:
            return model.get_model_response(text)
        if self.undermain == 1:
            return model.get_authors_last_papers(text)
        
        
        
        # return 'Some reaction should be here ))) '
        return random.choices(self.funny_answers)
    
        