from telebot import types
import os
import pickle


class Users:
    activeUsers = {}

    def __init__(self, chat_id, user_json):
        self.id = user_json["id"]
        self.isBot = user_json["is_bot"]
        self.firstName = user_json["first_name"]
        self.userName = user_json["username"]
        self.languageCode = user_json.get("language_code", "")
        self.__class__.activeUsers[chat_id] = self

    def __str__(self):
        return f"Name user: {self.firstName}   id: {self.userName}   lang: {self.languageCode}"

    def getUserHTML(self):
        return f"Name user: {self.firstName}   id: <a href='https://t.me/{self.userName}'>{self.userName}</a>   lang: {self.languageCode}"

    @classmethod
    def getUser(cls, chat_id):
        return cls.activeUsers.get(chat_id)



class Menu:
    hash = {}
    cur_menu = None
    extendParameters = {}

    def __init__(self, name, buttons=None, parent=None, action=None):
        self.parent = parent
        self.name = name
        self.buttons = buttons
        self.action = action

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
        markup.add(*buttons)
        self.markup = markup
        self.__class__.hash[name] = self

    @classmethod
    def getExtPar(cls, id):
        return cls.extendParameters.pop(id, None)

    @classmethod
    def setExtPar(cls, parameter):
        import uuid
        id = uuid.uuid4().hex
        cls.extendParameters[id] = parameter
        return id
    @classmethod
    def getMenu (cls, name):
        menu = cls.hash.get(name)
        if menu !=None:
            cls.cur_menu = menu
        return menu

    @classmethod
    def getCurMenu(cls, chat_id):
        return cls.cur_menu.get(chat_id)

    @classmethod
    def loadCurMenu(self):
        if os.path.exists(self.namePickleFile):
            with open(self.namePickleFile, 'rb') as pickle_in:
                self.cur_menu = pickle.load(pickle_in)
        else:
            self.cur_menu = {}

    @classmethod
    def saveCurMenu(self):
        with open(self.namePickleFile, 'wb') as pickle_out:
            pickle.dump(self.cur_menu, pickle_out)



def goto_menu(bot, chat_id, name_menu):
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)
        return target_menu
    else:
        return None

m_main = Menu("Главное меню", buttons=["Развлечения, картинки", "Игры", "Уныние (курсы валют)"])
m_games = Menu("Игры", buttons=["Числа"], parent=m_main)
# m_game_rsp = Menu("Костяшки", buttons=["Бросить кость", "Выход"], parent=m_games)
m_fun = Menu("Развлечения, картинки", buttons=["Рассказать анекдот", "Показать собачку", "Показать уточку", "Показать лисичку", "Выход"], parent=m_main)
m_course = Menu("Уныние (курсы валют)", buttons=["USD", "EUR", "Выход"], parent=m_main)