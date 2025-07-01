import telebot

# Reemplaza con tu token de bot de Telegram
TOKEN = "7747413792:AAFIgakahHwP53qRkPkv_4rvCaoUkalpVBw"

# Crea una instancia del bot
bot = telebot.TeleBot(TOKEN)

# Manejador de comandos /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "¡Hola! Soy un bot de prueba en Termux.  Usa /ayuda para ver los comandos disponibles.")

# Manejador de comandos /ayuda
@bot.message_handler(commands=['ayuda'])
def help_command(message):
    help_text = """
Comandos disponibles:
/start - Inicia el bot y muestra un saludo.
/ayuda - Muestra esta lista de comandos.
/eco <texto> - Repite el texto que envíes.
"""
    bot.reply_to(message, help_text)


# Manejador de comandos /eco
@bot.message_handler(commands=['eco'])
def echo_command(message):
    try:
        # Divide el mensaje en comando y texto
        text = message.text.split(' ', 1)[1]
        bot.reply_to(message, text)
    except IndexError:
        bot.reply_to(message, "Uso: /eco <texto>")


# Manejador para cualquier otro mensaje (solo responde con un saludo genérico)
@bot.message_handler(func=lambda message: True)  # Recibe cualquier mensaje
def echo_all(message):
    bot.reply_to(message, "No entiendo.  Prueba /ayuda para ver los comandos.")


# Inicia el bot (escucha por mensajes)
bot.infinity_polling()
