import config
import telebot
import json
import shelve_tool
from SQLighter import SQLighter
from telebot import types
bot = telebot.TeleBot(config.token)
db = SQLighter(config.database_name)


@bot.message_handler(commands=['start'])
def menu(message):
    if db.exists_user(message.chat.id):
        pass
    else:
        shelve_tool.set_shelve("mode.db", str(message.chat.id), 1)
        bot.send_message(message.chat.id, "Введите ФИО через пробел.")


@bot.message_handler(content_types=['text'])
def work(message):
    if shelve_tool.get_shelve("mode.db", str(message.chat.id)) == 1:
        if message.text in config.subjects:
            if shelve_tool.exist_shelve("Subjects.db", str(message.chat.id)):
                if message.text not in shelve_tool.get_shelve("Subjects.db", str(message.chat.id)):
                    shelve_tool.set_shelve("Subjects.db", str(message.chat.id), shelve_tool.get_shelve("Subjects.db",
                                           str(message.chat.id)) + ", " + message.text)
            else:
                shelve_tool.set_shelve("Subjects.db", str(message.chat.id), message.text)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for j in range(0, len(config.subjects) - 1, 2):
                markup.row(config.subjects[j], config.subjects[j + 1])
            markup.row(config.subjects[-1])
            markup.add("Далее")
            bot.send_message(message.chat.id, "Если вы выбрали нужные предметы, то нажмите Далее", reply_markup=markup)
        elif message.text in ["1 уровень", "3 уровень", "2 уровень", "ВСОШ"]:
            if shelve_tool.exist_shelve("Levels.db", str(message.chat.id)):
                if message.text not in shelve_tool.get_shelve("Levels.db", str(message.chat.id)):
                    shelve_tool.set_shelve("Levels.db", str(message.chat.id), shelve_tool.get_shelve("Levels.db",
                                           str(message.chat.id)) + ", " + message.text)
            else:
                shelve_tool.set_shelve("Levels.db", str(message.chat.id), message.text)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row("1 уровень", "2 уровень", "3 уровень")
            markup.add("ВСОШ")
            markup.add("Далее")
            bot.send_message(message.chat.id, "Если вы выбрали нужные уровни, то нажмите Далее",
                             reply_markup=markup)
        else:
            for i in range(len(config.user_params)):
                if not shelve_tool.exist_shelve(config.user_params[i] + ".db", str(message.chat.id)):
                    if message.text != "Далее":
                        shelve_tool.set_shelve(config.user_params[i] + '.db', str(message.chat.id), message.text)
                    if i == 0:
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        markup.row("9", "10", "11")
                        bot.send_message(message.chat.id, config.bot_words[i], reply_markup=markup)
                    elif i == 1:
                        bot.send_message(message.chat.id, config.bot_words[i], reply_markup=None)
                    elif i == 2:
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        markup.row("1 уровень", "2 уровень", "3 уровень")
                        markup.add("ВСОШ")
                        bot.send_message(message.chat.id, config.bot_words[i], reply_markup=markup)
                    elif i == 4:
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        for j in range(0, len(config.subjects) - 1, 2):
                            markup.row(config.subjects[j], config.subjects[j + 1])
                        markup.row(config.subjects[-1])
                        bot.send_message(message.chat.id, config.bot_words[i - 1], reply_markup=markup)
                    elif i == 5 and message.text == 'Далее':
                        bot.send_message(message.chat.id, config.bot_words[i - 1], reply_markup=None)
                    elif i == 5:
                        db.insert_user(message.chat.id, shelve_tool.get_shelve("Name.db", str(message.chat.id)),
                                       shelve_tool.get_shelve("class.db", str(message.chat.id)),
                                       shelve_tool.get_shelve("Location.db", str(message.chat.id)),
                                       shelve_tool.get_shelve("Levels.db", str(message.chat.id)),
                                       shelve_tool.get_shelve("Subjects.db", str(message.chat.id)),
                                       shelve_tool.get_shelve("School.db", str(message.chat.id)))

                        with open("subjects.json", "r") as file:
                            data = json.load(file)
                            for subj in shelve_tool.get_shelve("Subjects.db", str(message.chat.id)).split(', '):
                                data[subj].append(message.chat.id)
                        with open("subjects.json", "w") as file:
                            json.dump(data, file)

                        shelve_tool.set_shelve("mode.db", str(message.chat.id), 2)
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        subj = db.get_user_info(message.chat.id)[5].split(", ")
                        for j in range(len(subj)):
                            if j % 3 != 2:
                                markup.row(subj[j])
                            else:
                                markup.add(subj[j])
                        bot.send_message(message.chat.id, "Выбор отслеживаемых олимпиад \n "
                                                          "Выберите предмет олимпиады", reply_markup=markup)

                    break
    elif shelve_tool.get_shelve("mode.db", str(message.chat.id)) == 2:
        if message.text in db.get_user_info(message.chat.id)[5].split(", "):
            subs = db.get_suboly(message.text)
            a = []
            for i in subs:
                a.append(str(i[3]))
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup1.row("Назад", "Далее")
            markup1.add("Выбрать другой предмет")
            markup1.add("Завершить")
            bot.send_message(message.chat.id, "Олимпиады по " + message.text, reply_markup=markup1)
            shelve_tool.set_shelve("oly2.db", str(message.chat.id), ' '.join(a))
            shelve_tool.set_shelve("oly2ind.db", str(message.chat.id), '0')
            olymp = db.get_oly(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split()[0])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileO")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addO")))
            bot.send_message(message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2],
                             reply_markup=markup)
        elif message.text == "Далее":
            index = (int(shelve_tool.get_shelve("oly2ind.db", str(message.chat.id))) + 1) % \
                    len(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split(' '))
            shelve_tool.set_shelve("oly2ind.db", str(message.chat.id), str(index))
            olymp = db.get_oly(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split()[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileO")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addO")))
            bot.send_message(message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2],
                             reply_markup=markup)
        elif message.text == "Назад":
            index = int(shelve_tool.get_shelve("oly2ind.db", str(message.chat.id)))
            if index == 0:
                index = len(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split(' ')) - 1
            else:
                index -= 1
            olymp = db.get_oly(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split()[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileO")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addO")))
            bot.send_message(message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2],
                             reply_markup=markup)
        elif message.text == "Выбрать другой предмет":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            subj = db.get_user_info(message.chat.id)[5].split(", ")
            for i in range(len(subj)):
                if i % 3 != 2:
                    markup.row(subj[i])
                else:
                    markup.add(subj[i])
            bot.send_message(message.chat.id, "Выберите предмет олимпиады", reply_markup=markup)
        elif message.text == "Завершить":
            if shelve_tool.exist_shelve("prefers.db", str(message.chat.id)):
                shelve_tool.set_shelve("mode.db", str(message.chat.id), 3)
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup.row("Гуманитарная", "Техническая")
                markup.row("Медицинская", "Соц-эконом")
                bot.send_message(message.chat.id, "Выберите направленность ВУЗа", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "Вы не выбрали не одной олимпиады.")

    elif shelve_tool.get_shelve("mode.db", str(message.chat.id)) == 3:
        if message.text in config.directions:
            subs = db.get_diruny(message.text)
            a = []
            for i in subs:
                a.append(str(i[0]))
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup1.row("Назад", "Далее")
            markup1.add("Выбрать другую направленность")
            markup1.add("Завершить")
            bot.send_message(message.chat.id, "ВУЗы с " + message.text[:-2] + "ой направленностью",
                             reply_markup=markup1)
            shelve_tool.set_shelve("uny2.db", str(message.chat.id), ' '.join(a))
            shelve_tool.set_shelve("uny2ind.db", str(message.chat.id), '0')
            uny = db.get_univer(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split()[0])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileY")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addY")))
            bot.send_message(message.chat.id, "🏫Университет🏫 \n\n" + uny[1] + "\n" + "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность", reply_markup=markup)
        elif message.text == "Далее":
            index = (int(shelve_tool.get_shelve("uny2ind.db", str(message.chat.id))) + 1) % \
                    len(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split(' '))
            shelve_tool.set_shelve("uny2ind.db", str(message.chat.id), str(index))
            uny = db.get_univer(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split()[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileY")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addY")))
            bot.send_message(message.chat.id,
                             "🏫Университет🏫 \n\n" + uny[1] + "\n" + "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность", reply_markup=markup)
        elif message.text == "Назад":
            index = int(shelve_tool.get_shelve("uny2ind.db", str(message.chat.id)))
            if index == 0:
                index = len(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split(' ')) - 1
            else:
                index -= 1
            shelve_tool.set_shelve("uny2ind.db", str(message.chat.id), str(index))
            uny = db.get_univer(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split()[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileY")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addY")))
            bot.send_message(message.chat.id,
                             "🏫Университет🏫 \n\n" + uny[1] + "\n" + "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность", reply_markup=markup)
        elif message.text == "Выбрать другую направленность":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row("Гуманитарная", "Техническая")
            markup.row("Медицинская", "Соц-эконом")
            bot.send_message(message.chat.id, "Выберите направленность ВУЗа", reply_markup=markup)
        elif message.text == "Завершить":
            if shelve_tool.get_shelve("prefers1.db", str(message.chat.id)):
                shelve_tool.set_shelve("mode.db", str(message.chat.id), 4)
                with open("dateOfOli.json", 'r') as file:
                    data = json.load(file)
                for i in shelve_tool.get_shelve("prefers.db", str(message.chat.id)).split(', '):
                    data[i].append(message.chat.id)
                with open("dateOfOli.json", 'w') as file:
                    json.dump(data, file)
                db.insert_prefers(str(message.chat.id), shelve_tool.get_shelve("prefers.db", str(message.chat.id)),
                                  shelve_tool.get_shelve("prefers1.db", str(message.chat.id)))
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row("Профиль", "Олимпиады и ВУЗы")
                markup.row("Избранное", "Уведомления")
                bot.send_message(message.chat.id, "Настройка профиля законечена!", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "Вы не выбрали ни одного университета")
    elif shelve_tool.get_shelve("mode.db", str(message.chat.id)) == 4:
        if message.text == "Профиль":
            row = db.get_user_info(str(message.chat.id))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Назад", "Изменить")
            bot.send_message(message.chat.id, "ФИО: " + row[1] + '\n' + "Класс " + str(row[2]) + '\n' + "Город: " +
                             row[3] + "\n" + "Предметы олимпиад: " + row[5] + '\n' + "Школа: " + row[6],
                             reply_markup=markup)
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 5)
        elif message.text == "Олимпиады и ВУЗы":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Олимпиады", "Вузы")
            bot.send_message(message.chat.id, "Выберите, что хотите посмотреть", reply_markup=markup)
        elif message.text == "Олимпиады":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Мои олимпиады", "Выбрать новые олимпиады")
            bot.send_message(message.chat.id, "Выберите, что хотите посмотреть", reply_markup=markup)
        elif message.text == "Вузы":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Мои ВУЗы", "Выбрать новые ВУЗы")
            bot.send_message(message.chat.id, "Выберите, что хотите посмотреть", reply_markup=markup)
        elif message.text == "Мои олимпиады":
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 6)
            olymps = db.get_prefers(str(message.chat.id))[1]
            if olymps != "":
                shelve_tool.set_shelve("oly3.db", str(message.chat.id), olymps)
                shelve_tool.set_shelve("oly3ind.db", str(message.chat.id), 0)
                markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup1.row("Назад", "Далее")
                markup1.add("Завершить")
                bot.send_message(message.chat.id, "Мои олимпиады", reply_markup=markup1)
                olymp = db.get_oly(shelve_tool.get_shelve("oly3.db", str(message.chat.id)).split(', ')[0])
                markup = types.InlineKeyboardMarkup()
                markup.add((types.InlineKeyboardButton(text="Удалить", callback_data="delO")))
                bot.send_message(message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2],
                                 reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "Вы не выбрали ни одной олимпиады")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row("Профиль", "Олимпиады и ВУЗы")
                markup.row("Избранное", "Уведомления")
                bot.send_message(message.chat.id, "Сохранено", reply_markup=markup)
                shelve_tool.set_shelve("mode.db", str(message.chat.id), 4)
        elif message.text == "Выбрать новые олимпиады":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            subj = db.get_user_info(message.chat.id)[5].split(", ")
            for j in range(len(subj)):
                if j % 3 != 2:
                    markup.row(subj[j])
                else:
                    markup.add(subj[j])
            bot.send_message(message.chat.id, "Выбор отслеживаемых олимпиад \n "
                                              "Выберите предмет олимпиады", reply_markup=markup)
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 7)
        elif message.text == "Мои ВУЗы":
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 8)
            unys = db.get_prefers(str(message.chat.id))[2]
            shelve_tool.set_shelve("uny3.db", str(message.chat.id), unys)
            shelve_tool.set_shelve("uny3ind.db", str(message.chat.id), 0)
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup1.row("Назад", "Далее")
            markup1.add("Завершить")
            bot.send_message(message.chat.id, "Мои Вузы", reply_markup=markup1)
            uny = db.get_univer(shelve_tool.get_shelve("uny3.db", str(message.chat.id)).split(', ')[0])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Удалить", callback_data="delY")))
            bot.send_message(message.chat.id,
                             "🏫Университет🏫 \n\n" + uny[1] + "\n" + "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность", reply_markup=markup)
        elif message.text == "Выбрать новые ВУЗы":
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 9)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row("Гуманитарная", "Техническая")
            markup.row("Медицинская", "Соц-эконом")
            bot.send_message(message.chat.id, "Выберите направленность ВУЗа", reply_markup=markup)
    elif shelve_tool.get_shelve("mode.db", str(message.chat.id)) == 5:
        if message.text == "Изменить":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.row("ФИО", "Класс", "Город")
            markup.row("Предметы олимпиад", "Школа", "Назад")
            bot.send_message(message.chat.id, "Выберите, что хотите изменить", reply_markup=markup)
        elif message.text == "ФИО":
            shelve_tool.set_shelve("change.db", str(message.chat.id), 1)
            bot.send_message(message.chat.id, "Введите ФИО через пробел")
        elif message.text == "Класс":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row("9", "10", "11")
            shelve_tool.set_shelve("change.db", str(message.chat.id), 2)
            bot.send_message(message.chat.id, "Выберите ваш класс", reply_markup=markup)
        elif message.text == "Город":
            shelve_tool.set_shelve("change.db", str(message.chat.id), 3)
            bot.send_message(message.chat.id, "Введите ваш город")
        elif message.text == "Предметы олимпиад":
            shelve_tool.set_shelve("change.db", str(message.chat.id), 4)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for j in range(0, len(config.subjects) - 1, 2):
                markup.row(config.subjects[j], config.subjects[j + 1])
            markup.row(config.subjects[-1])
            shelve_tool.del_shelve("Subjects.db", str(message.chat.id))
            bot.send_message(message.chat.id, "Выберите предметы олимпиад", reply_markup=markup)
        elif message.text in config.subjects:
            if shelve_tool.exist_shelve("Subjects.db", str(message.chat.id)):
                if message.text not in shelve_tool.get_shelve("Subjects.db", str(message.chat.id)):
                    shelve_tool.set_shelve("Subjects.db", str(message.chat.id), shelve_tool.get_shelve("Subjects.db",
                                           str(message.chat.id)) + ", " + message.text)
            else:
                shelve_tool.set_shelve("Subjects.db", str(message.chat.id), message.text)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for j in range(0, len(config.subjects) - 1, 2):
                markup.row(config.subjects[j], config.subjects[j + 1])
            markup.row(config.subjects[-1])
            markup.add("Закончить")
            bot.send_message(message.chat.id, "Если вы выбрали нужные предметы, то нажмите Закончить",
                             reply_markup=markup)
        elif message.text == "Школа":
            shelve_tool.set_shelve("change.db", str(message.chat.id), 5)
            bot.send_message(message.chat.id, "Введите название вашей школы")
        elif message.text == "Закончить":
            row = db.get_user_info(str(message.chat.id))
            db.delete_user(str(message.chat.id))
            db.insert_user(row[0], row[1], row[2], row[3], row[4], shelve_tool.get_shelve("Subjects.db",
                                                                                          str(message.chat.id)), row[6])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.row("ФИО", "Класс", "Город")
            markup.row("Предметы олимпиад", "Школа", "Назад")
            bot.send_message(message.chat.id, "Выберите, что хотите изменить", reply_markup=markup)
        elif message.text == "Назад":
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 4)
            with open("dateOfOli.json", 'r') as file:
                data = json.load(file)
            for i in shelve_tool.get_shelve("prefers.db", str(message.chat.id)).split(', '):
                data[i].append(message.chat.id)
            with open("dateOfOli.json", 'w') as file:
                json.dump(data, file)
            db.insert_prefers(str(message.chat.id), shelve_tool.get_shelve("prefers.db", str(message.chat.id)),
                              shelve_tool.get_shelve("prefers1.db", str(message.chat.id)))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Профиль", "Олимпиады и ВУЗы")
            markup.row("Избранное", "Уведомления")
            bot.send_message(message.chat.id, "Сохранено", reply_markup=markup)
        else:
            if shelve_tool.get_shelve("change.db", str(message.chat.id)) == 1:
                row = db.get_user_info(str(message.chat.id))
                db.delete_user(str(message.chat.id))
                db.insert_user(row[0], message.text, row[2], row[3], row[4], row[5], row[6])
            elif shelve_tool.get_shelve("change.db", str(message.chat.id)) == 2:
                row = db.get_user_info(str(message.chat.id))
                db.delete_user(str(message.chat.id))
                db.insert_user(row[0], row[1], message.text, row[3], row[4], row[5], row[6])
            elif shelve_tool.get_shelve("change.db", str(message.chat.id)) == 3:
                row = db.get_user_info(str(message.chat.id))
                db.delete_user(str(message.chat.id))
                db.insert_user(row[0], row[1], row[2], message.text, row[4], row[5], row[6])
            elif shelve_tool.get_shelve("change.db", str(message.chat.id)) == 5:
                row = db.get_user_info(str(message.chat.id))
                db.delete_user(str(message.chat.id))
                db.insert_user(row[0], row[1], row[2], row[3], row[4], row[5], message.text)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.row("ФИО", "Класс", "Город")
            markup.row("Предметы олимпиад", "Школа", "Назад")
            bot.send_message(message.chat.id, "Изменения сохранены. \n Выберите, что хотите изменить или нажмите Назад",
                             reply_markup=markup)
    elif shelve_tool.get_shelve("mode.db", str(message.chat.id)) == 6:
        if message.text == "Далее":
            index = (int(shelve_tool.get_shelve("oly3ind.db", str(message.chat.id))) + 1) % \
                    len(shelve_tool.get_shelve("oly3.db", str(message.chat.id)).split(', '))
            shelve_tool.set_shelve("oly3ind.db", str(message.chat.id), str(index))
            olymp = db.get_oly(shelve_tool.get_shelve("oly3.db", str(message.chat.id)).split(', ')[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Удалить", callback_data="delO")))
            bot.send_message(message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2],
                             reply_markup=markup)
        elif message.text == "Назад":
            index = int(shelve_tool.get_shelve("oly3ind.db", str(message.chat.id)))
            if index == 0:
                index = len(shelve_tool.get_shelve("oly3.db", str(message.chat.id)).split(', ')) - 1
            else:
                index -= 1
            shelve_tool.set_shelve("oly3ind.db", str(message.chat.id), str(index))
            olymp = db.get_oly(shelve_tool.get_shelve("oly3.db", str(message.chat.id)).split(', ')[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Удалить", callback_data="delO")))
            bot.send_message(message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2],
                             reply_markup=markup)
        elif message.text == "Завершить":
            row = db.get_prefers(str(message.chat.id))
            db.del_prefers(str(message.chat.id))
            with open("dateOfOli.json", 'r') as file:
                data = json.load(file)
            for i in shelve_tool.get_shelve("oly3.db", str(message.chat.id)).split(', '):
                data[i].append(message.chat.id)
            with open("dateOfOli.json", 'w') as file:
                json.dump(data, file)
            db.insert_prefers(str(message.chat.id), shelve_tool.get_shelve('oly3.db', str(message.chat.id)), row[2])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Профиль", "Олимпиады и ВУЗы")
            markup.row("Избранное", "Уведомления")
            bot.send_message(message.chat.id, "Сохранено", reply_markup=markup)
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 4)
    elif shelve_tool.get_shelve("mode.db", str(message.chat.id)) == 7:
        if message.text in config.subjects:
            shelve_tool.del_shelve("prefers.db", str(message.chat.id))
            subs = db.get_suboly(message.text)
            a = []
            for i in subs:
                a.append(str(i[3]))
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup1.row("Назад", "Далее")
            markup1.add("Выбрать другой предмет")
            markup1.add("Завершить")
            bot.send_message(message.chat.id, "Олимпиады по " + message.text, reply_markup=markup1)
            shelve_tool.set_shelve("oly2.db", str(message.chat.id), ' '.join(a))
            shelve_tool.set_shelve("oly2ind.db", str(message.chat.id), '0')
            olymp = db.get_oly(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split()[0])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileO")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addO")))
            bot.send_message(message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2],
                             reply_markup=markup)
        elif message.text == "Далее":
            index = (int(shelve_tool.get_shelve("oly2ind.db", str(message.chat.id))) + 1) % \
                    len(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split(' '))
            shelve_tool.set_shelve("oly2ind.db", str(message.chat.id), str(index))
            olymp = db.get_oly(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split()[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileO")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addO")))
            bot.send_message(message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2],
                             reply_markup=markup)
        elif message.text == "Назад":
            index = int(shelve_tool.get_shelve("oly2ind.db", str(message.chat.id)))
            if index == 0:
                index = len(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split(' ')) - 1
            else:
                index -= 1
            olymp = db.get_oly(shelve_tool.get_shelve("oly2.db", str(message.chat.id)).split()[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileO")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addO")))
            bot.send_message(message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2],
                             reply_markup=markup)
        elif message.text == "Выбрать другой предмет":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            subj = db.get_user_info(message.chat.id)[5].split(", ")
            for i in range(len(subj)):
                if i % 3 != 2:
                    markup.row(subj[i])
                else:
                    markup.add(subj[i])
            bot.send_message(message.chat.id, "Выберите предмет олимпиады", reply_markup=markup)
        elif message.text == "Завершить":
            row = db.get_prefers(str(message.chat.id))
            db.del_prefers(str(message.chat.id))
            db.insert_prefers(str(message.chat.id), row[1] +
                              ', ' + shelve_tool.get_shelve('prefers.db', str(message.chat.id)), row[2])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Профиль", "Олимпиады и ВУЗы")
            markup.row("Избранное", "Уведомления")
            bot.send_message(message.chat.id, "Сохранено", reply_markup=markup)
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 4)
    elif shelve_tool.get_shelve("mode.db", str(message.chat.id)) == 8:
        if message.text == "Далее":
            index = (int(shelve_tool.get_shelve("uny3ind.db", str(message.chat.id))) + 1) % \
                    len(shelve_tool.get_shelve("uny3.db", str(message.chat.id)).split(', '))
            shelve_tool.set_shelve("uny3ind.db", str(message.chat.id), str(index))
            uny = db.get_univer(shelve_tool.get_shelve("uny3.db", str(message.chat.id)).split(', ')[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Удалить", callback_data="delY")))
            bot.send_message(message.chat.id,
                             "🏫Университет🏫 \n\n" + uny[1] + "\n" + "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность", reply_markup=markup)
        elif message.text == "Назад":
            index = int(shelve_tool.get_shelve("uny3ind.db", str(message.chat.id)))
            if index == 0:
                index = len(shelve_tool.get_shelve("uny3.db", str(message.chat.id)).split(', ')) - 1
            else:
                index -= 1
            shelve_tool.set_shelve("uny3ind.db", str(message.chat.id), str(index))
            uny = db.get_univer(shelve_tool.get_shelve("uny3.db", str(message.chat.id)).split(', ')[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Удалить", callback_data="delY")))
            bot.send_message(message.chat.id,
                             "🏫Университет🏫 \n\n" + uny[1] + "\n" + "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность", reply_markup=markup)
        elif message.text == "Завершить":
            row = db.get_prefers(str(message.chat.id))
            db.del_prefers(str(message.chat.id))
            db.insert_prefers(str(message.chat.id), row[1], shelve_tool.get_shelve('uny3.db', str(message.chat.id)))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Профиль", "Олимпиады и ВУЗы")
            markup.row("Избранное", "Уведомления")
            bot.send_message(message.chat.id, "Сохранено", reply_markup=markup)
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 4)
    elif shelve_tool.get_shelve("mode.db", str(message.chat.id)) == 9:
        if message.text in config.directions:
            subs = db.get_diruny(message.text)
            shelve_tool.del_shelve("prefers1.db", str(message.chat.id))
            a = []
            for i in subs:
                a.append(str(i[0]))
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup1.row("Назад", "Далее")
            markup1.add("Выбрать другую направленность")
            markup1.add("Завершить")
            bot.send_message(message.chat.id, "ВУЗы с " + message.text[:-2] + "ой направленностью",
                             reply_markup=markup1)
            shelve_tool.set_shelve("uny2.db", str(message.chat.id), ' '.join(a))
            shelve_tool.set_shelve("uny2ind.db", str(message.chat.id), '0')
            uny = db.get_univer(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split()[0])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileY")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addY")))
            bot.send_message(message.chat.id,
                             "🏫Университет🏫 \n\n" + uny[1] + "\n" + "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность", reply_markup=markup)
        elif message.text == "Далее":
            index = (int(shelve_tool.get_shelve("uny2ind.db", str(message.chat.id))) + 1) % \
                    len(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split(' '))
            shelve_tool.set_shelve("uny2ind.db", str(message.chat.id), str(index))
            uny = db.get_univer(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split()[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileY")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addY")))
            bot.send_message(message.chat.id,
                             "🏫Университет🏫 \n\n" + uny[1] + "\n" + "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность", reply_markup=markup)
        elif message.text == "Назад":
            index = int(shelve_tool.get_shelve("uny2ind.db", str(message.chat.id)))
            if index == 0:
                index = len(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split(' ')) - 1
            else:
                index -= 1
            shelve_tool.set_shelve("uny2ind.db", str(message.chat.id), str(index))
            uny = db.get_univer(shelve_tool.get_shelve("uny2.db", str(message.chat.id)).split()[index])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Подробнее", callback_data="profileY")))
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addY")))
            bot.send_message(message.chat.id,
                             "🏫Университет🏫 \n\n" + uny[1] + "\n" + "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность", reply_markup=markup)
        elif message.text == "Выбрать другую направленность":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row("Гуманитарная", "Техническая")
            markup.row("Медицинская", "Соц-эконом")
            bot.send_message(message.chat.id, "Выберите направленность ВУЗа", reply_markup=markup)
        elif message.text == "Завершить":
            row = db.get_prefers(str(message.chat.id))
            db.del_prefers(str(message.chat.id))
            db.insert_prefers(str(message.chat.id), row[1],
                              row[2] + ', ' + shelve_tool.get_shelve('prefers1.db', str(message.chat.id)))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("Профиль", "Олимпиады и ВУЗы")
            markup.row("Избранное", "Уведомления")
            bot.send_message(message.chat.id, "Сохранено", reply_markup=markup)
            shelve_tool.set_shelve("mode.db", str(message.chat.id), 4)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "profileO":
            olymp = db.get_oly(shelve_tool.get_shelve("oly2.db", str(call.message.chat.id)).split()[
                                   int(shelve_tool.get_shelve("oly2ind.db", str(call.message.chat.id)))])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addO")))
            markup.add((types.InlineKeyboardButton(text="Сайт олимпиады", url=olymp[4])))
            markup.add((types.InlineKeyboardButton(text="Оценить олимпиаду", callback_data="rateO")))
            q = ''
            if olymp[5] != "ab":
                q = "\n\n" + olymp[5]
            bot.send_message(call.message.chat.id, "🏆Олимпиада🏆\n\n" + olymp[1] + '\n' + "Предмет: " + olymp[2]
                             + q, reply_markup=markup)
        elif call.data == "addO":
            if shelve_tool.exist_shelve("prefers.db", str(call.message.chat.id)):
                shelve_tool.set_shelve("prefers.db", str(call.message.chat.id), shelve_tool.get_shelve("prefers.db",
                                       str(call.message.chat.id)) + ", " +
                                       shelve_tool.get_shelve("oly2.db", str(call.message.chat.id)).split()[
                                           int(shelve_tool.get_shelve("oly2ind.db", str(call.message.chat.id)))])
            else:
                shelve_tool.set_shelve("prefers.db", str(call.message.chat.id),
                                       shelve_tool.get_shelve("oly2.db", str(call.message.chat.id)).split()[
                                           int(shelve_tool.get_shelve("oly2ind.db", str(call.message.chat.id)))])
        elif call.data == "rateO":
            pass
        elif call.data == 'profileY':
            uny = db.get_univer(shelve_tool.get_shelve("uny2.db", str(call.message.chat.id)).split()[
                                   int(shelve_tool.get_shelve("uny2ind.db", str(call.message.chat.id)))])
            markup = types.InlineKeyboardMarkup()
            markup.add((types.InlineKeyboardButton(text="Отслеживать", callback_data="addY")))
            markup.add((types.InlineKeyboardButton(text="Сайт университета", url=uny[4])))
            bot.send_message(call.message.chat.id, "🏫Университет🏫 \n\n" + uny[1] + '\n' "Город: " + uny[2] + '\n' + uny[6] +
                             " направленность\n\n" + uny[5], reply_markup=markup)
        elif call.data == "addY":
            if shelve_tool.exist_shelve("prefers1.db", str(call.message.chat.id)):
                shelve_tool.set_shelve("prefers1.db", str(call.message.chat.id), shelve_tool.get_shelve("prefers1.db",
                                       str(call.message.chat.id)) + ", " +
                                       shelve_tool.get_shelve("uny2.db", str(call.message.chat.id)).split()[
                                           int(shelve_tool.get_shelve("uny2ind.db", str(call.message.chat.id)))])
            else:
                shelve_tool.set_shelve("prefers1.db", str(call.message.chat.id),
                                       shelve_tool.get_shelve("uny2.db", str(call.message.chat.id)).split()[
                                           int(shelve_tool.get_shelve("uny2ind.db", str(call.message.chat.id)))])
        elif call.data == "delO":
            olymps = shelve_tool.get_shelve("oly3.db", str(call.message.chat.id)).split(', ')
            index = int(shelve_tool.get_shelve("oly3ind.db", str(call.message.chat.id)))
            if index != len(olymps) - 1 and index != 0:
                olymps = (' '.join(olymps[:index]) + ' ' + ' '.join(olymps[index + 1:])).split()
            elif index == 0:
                olymps = olymps[1:]
            else:
                olymps = olymps[:len(olymps) - 1]
            shelve_tool.set_shelve("oly3.db", str(call.message.chat.id), ', '.join(olymps))
            shelve_tool.set_shelve("oly3ind.db", str(call.message.chat.id), max([0, index - 1]))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удалено",
                                  reply_markup=None)
        elif call.data == "delY":
            unys = shelve_tool.get_shelve("uny3.db", str(call.message.chat.id)).split(', ')
            index = int(shelve_tool.get_shelve("uny3ind.db", str(call.message.chat.id)))
            if index != len(unys) - 1 and index != 0:
                unys = (' '.join(unys[:index]) + ' ' + ' '.join(unys[index + 1:])).split()
            elif index == 0:
                unys = unys[1:]
            else:
                unys = unys[:len(unys) - 1]
            shelve_tool.set_shelve("uny3.db", str(call.message.chat.id), ', '.join(unys))
            shelve_tool.set_shelve("uny3ind.db", str(call.message.chat.id), max([0, index - 1]))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Удалено",
                                  reply_markup=None)


if __name__ == '__main__':
    bot.infinity_polling()
