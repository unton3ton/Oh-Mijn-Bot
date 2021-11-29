from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import matplotlib
matplotlib.use('Agg') # иначе главный поток пошлёт в Runtimeerror

import matplotlib.pyplot as plt

# print("Бот запущен. Нажмите Ctrl+C для завершения")

def on_start(update, context):
	chat = update.effective_chat
	context.bot.send_message(chat_id=chat.id, text="Привет, я Граф-бот")

def on_help(update, context):
	chat = update.effective_chat
	context.bot.send_message(chat_id=chat.id, text="Напишите список данных: x , y, x_error, y_error, x_label, y_label")

def on_exmpl(update, context):
	chat = update.effective_chat
	context.bot.send_message(chat_id=chat.id, text="Например: 1.1 2.6 3.2 , 1.09 2.2 3.4, 0.1 0.6 0.2,\
	 0.09 0.2 0.4, x m/s, y kg")

	
token = "ВАШ ТОКЕН" # полученный от https://t.me/BotFather


def errorplot(x,y,x_error,y_error,x_label,y_label):
	fig = plt.figure()

	plt.errorbar(x, y, yerr = y_error, xerr = x_error, fmt ='o', color = 'black', ecolor = 'orange') 
	
	plt.grid()
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	fig.savefig('plot.png', dpi = 100)


def on1_message(update, context):
	chat = update.effective_chat
	text = update.message.text
	
	try:
		N = text.split(',') 
		global x_data, y_data, x_er, y_er, x_lab, y_lab 
		x_data = list(map(float,N[0].split())) 
		y_data = list(map(float,N[1].split())) 
		x_er = list(map(float,N[2].split())) 
		y_er = list(map(float,N[3].split()))
		x_lab = N[4]
		y_lab = N[5]
		
		context.bot.send_message(chat_id=chat.id, text='теперь пришли \n /plot')
	except:
		context.bot.send_message(chat_id=chat.id, text="Напишите список данных для графика как в примере!")


def on_plot(update, context):
	chat = update.effective_chat
	try:
		errorplot(x_data,y_data,x_er,y_er,x_lab,y_lab) 
		context.bot.send_message(chat_id=chat.id, text="построил график - теперь пришли \n /send \n \
			если нет сетки нажми \n /plot ещё раз")
	except:
		context.bot.send_message(chat_id=chat.id, text="не построил график")


def on_send(update, context):
	chat = update.effective_chat
	try:
		context.bot.send_photo(chat_id=chat.id, photo=open('plot.png', 'rb'))
	except:
		context.bot.send_message(chat_id=chat.id, text="не нашёл график :(")


updater = Updater(token, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", on_start))
dispatcher.add_handler(CommandHandler("help", on_help))
dispatcher.add_handler(CommandHandler("plot", on_plot))
dispatcher.add_handler(CommandHandler("send", on_send))
dispatcher.add_handler(CommandHandler("exmpl", on_exmpl))
dispatcher.add_handler(MessageHandler(Filters.all, on1_message))

updater.start_polling()
updater.idle()