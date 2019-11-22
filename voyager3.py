import telebot
import datetime
i = datetime.datetime.now()
from telebot import types

API_TOKEN = '843897114:AAHiETgXI5IGgI6G7onD8r8A6BsQiLda8fo'

bot = telebot.TeleBot(API_TOKEN)


user_dict = {}

price = ("""
Чай
0,5г. = 140 UAH
от 1г. до 4г. = 220 UAH/г.
от 5г. до 10г. = 200 UAH/г.
---------------------------
Кохфе
0.5г. = 200 UAH
от 1г. до 4г. = 360 UAH/г.
от 5г. до 9г. = 330 UAH/г.
10г. = 3000 грн
---------------------------
Цикорий
от 1г. до 4г. = 170 UAH/г.
от 5г. до 9г. = 160 UAH/г.
от 10г. до 20г. = 150 UAH/г.

Нажи /start чтобы начать.
""")

class User:
	def __init__(self, name):
		self.name = name
		self.age = None
		self.sex = None
		self.fw = None
		self.orderid = None

welcome = ("""\

Привет, ниже информация для ознакомления:
📩Способы оплаты

💴EasyPay - 52862223
💷GlobalMoney - 84018360427423

ℹ️Контактная информация
🙋‍♂️Оператор - @GorillaDrug
🏠Новостной канал - @gorilladrugshop
📨Чат для общения - @gorilladrugchat

Готов сделать заказ?
""")

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	try:
		chat_id = message.chat.id
		fw = message.text
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
		markup.add('Да', 'Прайс')
		msg = bot.reply_to(message, welcome, reply_markup=markup)
		bot.register_next_step_handler(msg, process_welcome_step)
	except Exception as e:
		bot.reply_to(message, """Нажми /start чтоб начать сначала и введи корректные данные""")

def process_welcome_step(message):
	try:
		chat_id = message.chat.id
		fw = message.text
		user = User(fw)
		user_dict[chat_id] = user
		if fw == 'Прайс':
			bot.reply_to(message, price)
		else: 
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('Торгмаш', 'Развилка', 'Другое место(уточнить)')
			msg = bot.reply_to(message, 'Выбери свой район', reply_markup=markup)
			bot.register_next_step_handler(msg, process_name_step)
	except Exception as e:
		bot.reply_to(message, """Нажми /start чтоб начать сначала и введи корректные данные""")


def process_name_step(message):
	try:
		chat_id = message.chat.id
		name = message.text
		if name == 'Другое место(уточнить)':
			msg = bot.reply_to(message, 'Какой район?')
			bot.register_next_step_handler(msg, process_name_step)
			return
		user = User(name)
		user_dict[chat_id] = user
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
		markup.add('Чай', 'Кохфе', 'Цикорий')
		msg = bot.reply_to(message, 'Что хочешь купить?', reply_markup=markup)
		bot.register_next_step_handler(msg, process_age_step)
	except Exception as e:
		bot.reply_to(message, """Нажми /start чтоб начать сначала и введи корректные данные""")


def process_age_step(message):
	try:
		chat_id = message.chat.id
		sex = message.text
		user = user_dict[chat_id]
		if (sex == u'Чай') or (sex == u'Кохфе') or (sex == u'Цикорий'):
			user.sex = sex
		else:
			raise Exception()
		if (sex == u'Чай'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('0,5г. = 140UAH', '1-4г. = 220UAH', '5-10г. = 200UAH')
			msg = bot.reply_to(message, 'Сколько отсыпать?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_age1_step)
		elif (sex == u'Цикорий'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('1-4г. = 170UAH', '5-9г. = 160UAH', '10-20г. = 150UAH')
			msg = bot.reply_to(message, 'Сколько отсыпать?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_age1_step)
		elif (sex == u'Кохфе'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('0,5г. = 200UAH', '1-4г. = 360UAH', '5-9г. = 330UAH', '10г. = 3000UAH')
			msg = bot.reply_to(message, 'Сколько отсыпать?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_age1_step)
	except Exception as e:
		bot.reply_to(message, """Нажми /start чтоб начать сначала и введи корректные данные""")

def process_age1_step(message):
	try:
		chat_id = message.chat.id
		age = message.text
		sex1 = message.text
		user = user_dict[chat_id]
		if (age == '0,5г. = 140UAH') and (user.sex == 'Чай'):
			process_sex_step(message)
		elif (age == '1-4г. = 220UAH') and (user.sex == 'Чай'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('1г. = 220 UAH', '2г. = 440 UAH', '3г. = 660 UAH', '4г. = 880 UAH')
			msg = bot.reply_to(message, 'Уточни', reply_markup=markup)
			bot.register_next_step_handler(msg, process_sex_step)
		elif (age == '5-10г. = 200UAH') and (user.sex == 'Чай'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('5г. = 1000 UAH', '6г. = 1200 UAH', '7г. = 1400 UAH', '8г. = 1600 UAH','9г. = 1800 UAH','10г. = 2000 UAH')
			msg = bot.reply_to(message, 'Уточни', reply_markup=markup)
			bot.register_next_step_handler(msg, process_sex_step)
		elif (age == '0,5г. = 200UAH') and (user.sex == 'Кохфе'):
			process_sex_step(message)
		elif (age == '1-4г. = 360UAH') and (user.sex == 'Кохфе'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('1г. = 360UAH', '2г. = 720UAH', '3г. = 1080UAH', '4г. = 1440UAH')
			msg = bot.reply_to(message, 'Уточни', reply_markup=markup)
			bot.register_next_step_handler(msg, process_sex_step)
		elif (age == '5-9г. = 330UAH') and (user.sex == 'Кохфе'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('5г. = 1650 UAH', '6г. = 1980 UAH', '7г. = 2310 UAH', '8г. = 2640 UAH','9г. = 2970 UAH')
			msg = bot.reply_to(message, 'Уточни', reply_markup=markup)
			bot.register_next_step_handler(msg, process_sex_step)
		elif (age == '10г. = 3000UAH') and (user.sex == 'Кохфе'):
			process_sex_step(message)
		elif (age == '10г. = 1300UAH') and (user.sex == 'Цикорий'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			msg = bot.reply_to(message, 'Уточни', reply_markup=markup)
			bot.register_next_step_handler(msg, process_sex_step)
		elif (age == '1-4г. = 170UAH') and (user.sex == 'Цикорий'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('1г. = 170 UAH', '2г. = 340 UAH', '3г. = 510 UAH', '4г. = 680 UAH')
			msg = bot.reply_to(message, 'Уточни', reply_markup=markup)
			bot.register_next_step_handler(msg, process_sex_step)
		elif (age == '5-9г. = 160UAH') and (user.sex == 'Цикорий'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			markup.add('5г. = 800 UAH', '6г. = 960 UAH', '7г. = 1120 UAH', '8г. = 1280 UAH','9г. = 1440 UAH')
			msg = bot.reply_to(message, 'Уточни', reply_markup=markup)
			bot.register_next_step_handler(msg, process_sex_step)
		elif (age == '10-20г. = 150UAH') and (user.sex == 'Цикорий'):
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
			msg = bot.reply_to(message, 'Введи вручную от 10 до 20 (только число)', reply_markup=markup)
			bot.register_next_step_handler(msg, process_sex_step)
	except Exception as e:
		bot.reply_to(message, """Нажми /start чтоб начать сначала и введи корректные данные""")

def process_sex_step(message):
	try:
		chat_id = message.chat.id
		user = user_dict[chat_id]
		age = message.text
		user.age = str(age).split(' = ')[0]
		if 'UAH' in age:
			user.age1 = str(age).split(' = ')[1]
		else:
			user.age1 = str(int(str(age).split(' = ')[0]) * 150) + 'UAH'
		myname  = message.from_user.username
		user.orderid = str("%s" %i.second + "%s" %i.minute + "%s" %i.hour + "%s%s%s" % (i.month, i.day, i.year))
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
		msg = bot.reply_to(message, 'Твой заказ принят! ' + '\nID заказа: #' + user.orderid +'\nРайон: ' + user.name + '\nТовар: ' + user.sex + '\nВес: ' + str(user.age) + '\nЦена: ' + str(user.age1) + '\nМожем переходить к оплате!', reply_markup=markup)
		markup = types.InlineKeyboardMarkup()
		btn_easypay = types.InlineKeyboardButton(text='EasyPay', url='https://easypay.ua/catalog/e-money/easypay/easypay-money-deposit')
		btn_globalmoney = types.InlineKeyboardButton(text='globalmoney', url='https://easypay.ua/catalog/e-money/global-wallet')
		markup.add(btn_easypay, btn_globalmoney)
		bot.send_message(message.chat.id, """Реквизиты для оплаты:
EasyPay: 52862223
globalmoney: 84018360427423
❗️Внимание❗️
❗️Сделай скрин оплаты и отправь боту.❗️
❗️В подпись сообщения не забудь добавить ID заказа.❗️
❗️Иначе заказ не будет рассмотрен опреатором.❗️
❗️Твой ID: """ + user.orderid + ' ❗️', reply_markup = markup)
	except Exception as e:
		bot.reply_to(message, """Нажми /start чтоб начать сначала и введи корректные данные""")
	
def replyme(message):
	try:
		chat_id = message.chat.id
		user = user_dict[chat_id]
		bot.forward_message(chat_id='-1001350609769',
							from_chat_id=message.chat.id,
							message_id=message.message_id)
	except Exception as e:
		bot.reply_to(message, """Нажми /start чтоб начать сначала и введи корректные данные""")



@bot.message_handler(content_types = ['photo'])
def send_nudes(message):
	try:
		chat_id = message.chat.id
		user = user_dict[chat_id]
		myname  = message.from_user.username
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
		bot.reply_to(message, """Спасибо, оператор свяжется с тобой, как только проверит оплату.
	Если хочешь заказать ещё - пиши /start""")
		bot.send_message('-1001350609769', 'Новый заказ: '+ '\nID заказа: #' + user.orderid +'\nРайон: ' + user.name + '\nТовар: ' + user.sex + '\nВес: ' + str(user.age) + '\nЦена: ' + str(user.age1) + '\n@' + str(myname)) # добавить ID пользователя
		replyme(message)
	except Exception as e:
		bot.reply_to(message, """Нажми /start чтоб начать сначала и введи корректные данные""")

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling(none_stop=False)


