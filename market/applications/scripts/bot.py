import telebot
from datetime import datetime
import threading
import time
import locale
from timeit import Timer
locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))


import psycopg2 as postgres
import datetime as dates
try:
    connection = postgres.connect(
        host='db',
        database='marketdb3',
        user='postgres',
        password='root'
        )
    print('Conexion establecida')
    cur = connection.cursor()
    bot = telebot.TeleBot("5768298048:AAFyjsbxKprBNpSw_VldOM8BxOuEMzNMU0Q")

    @bot.message_handler(commands=["cierre", "inventario"])
    def handle_cierre_inventario(message):
        now =  datetime.now()
        bot.reply_to(message,"⛳️Hola, te mostrare el cierre del día de hoy: " + str(now.strftime("%A, %d de %B de %Y a las %I:%M %p")) + " ⛳️")
        cur.execute("SELECT product_report_id, count_add_report,count_total_report  FROM producto_ListFinal")
        for product_report_id,count_add_report,count_total_report in cur.fetchall():
            a = product_report_id
            cur.execute("SELECT name FROM producto_Product WHERE id=(%s)",[a])
            for name in cur.fetchall():
                if count_total_report < 0:
                    bot.reply_to(message,"🥐🥯🍞🥖" + str(name) + "🥐🥯🍞🥖 " + " En puerta: " + str(count_add_report) + " 🤦🏽‍♂️ Falto ingresar al sistema: " + str(-1*count_total_report) + "pzas 🤦🏽‍♂️")
                elif (count_total_report == 0):
                    bot.reply_to(message,"🥐🥯🍞🥖" + str(name) + "🥐🥯🍞🥖 " + " En puerta: " + str(count_add_report) + " 🎊 Felicidades sin diferencia: 🎊")
                else:
                    bot.reply_to(message,"🥐🥯🍞🥖" + str(name) + "🥐🥯🍞🥖 " + " En puerta: " + str(count_add_report) + " 🤷🏽 Tenemos de más en el sistema: " + str(count_total_report)+ "pzas 🤷🏽 ‍")



    @bot.message_handler(commands = ["help","start"])
    def enviar(message):
        def timer():
            print("Entre al timer")
         #   while True:
          #      print("¡Hola, mundo!")
           #     time.sleep(3)   # 3 segundos.
        bot.reply_to(message,"Hola, Bienvenido al bot de MauPan")
        datetime_object = datetime.now()
        t = threading.Thread(target=timer)
        t.start()
        print(datetime_object)

    @bot.message_handler(content_types=["text"])
    def bot_mensaje_texto(message):
        """Gestiona los mensajes de texto recibidos"""
        if message.text.startswith("/"):
            bot.send_message(message.chat.id,"Comando no disponible")
        else:
            bot.send_message(message.chat.id,"Estamos probando")

    bot.polling()

except (Exception, postgres.Error) as error:
    print("Error: ",error)
except:
    print('error de conexion')
