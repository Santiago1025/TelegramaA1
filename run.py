#!/usr/bin/env python3
import asyncio
import logging
import math
import os

from metaapi_cloud_sdk import MetaApi
from prettytable import PrettyTable
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, CallbackContext

# MetaAPI Credentials
API_KEY = os.environ.get("API_KEY")
ACCOUNT_ID = os.environ.get("ACCOUNT_ID")

# Telegram Credentials
TOKEN = os.environ.get("TOKEN")
#TELEGRAM_USER = os.environ.get("TELEGRAM_USER")

# Heroku Credentials
APP_URL = os.environ.get("APP_URL")

# Port number for Telegram bot web hook
PORT = int(os.environ.get('PORT', '8443'))


# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# possibles states for conversation handler
CALCULATE, ORDEN, DECISION = range(3)
def unknown_command(update: Update, context: CallbackContext) -> None:

    update.effective_message.reply_text("Selecciona Tipo de Orden:")
    update.effective_message.reply_text("/idCarrito\n/IdVenta\n/idFavoritos")
    return

def agregarOrden_Command(update: Update, context: CallbackContext) -> int:
    """Asks user to enter the trade they would like to place.

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """
    
    # initializes the user's trade as empty prior to input and parsing
    context.user_data['trade'] = None
    
    # asks user to enter the trade
    update.effective_message.reply_text("Agregar nueva orden")
    update.effective_message.reply_text("Selecciona un instituto:")
    update.effective_message.reply_text("/100 \n /101 \n /102 \n /103 \n /104 \n")

    return ConversationHandler.END
def instituto100_Command(update: Update, context: CallbackContext) -> int:
    # asks user to enter the trade
    update.effective_message.reply_text("Selecciona un Negocio:")
    update.effective_message.reply_text("/DCC")

    return ConversationHandler.END
def negocioDCC_Command(update: Update, context: CallbackContext) -> int:
    # asks user to enter the trade
    update.effective_message.reply_text("idOrdenOK: 100-ff9e51c2d469")
    update.effective_message.reply_text("Escribe el IdOrdenBK:")

    return ConversationHandler.END
def tipoOrdenIdCarrito_Command(update: Update, context: CallbackContext) -> int:
    # asks user to enter the trade
    update.effective_message.reply_text("Selecciona un Rol")
    update.effective_message.reply_text("/idCliente\n/idVendedor\n/idProveedor")

    return ConversationHandler.END
def idCliente_Command(update: Update, context: CallbackContext) -> int:
    # asks user to enter the trade
    update.effective_message.reply_text("Selecciona una persona")
    update.effective_message.reply_text("/Juanito_Perez_Perez \n /Carlos_Fernandez_Diaz \n /Ana_Martinez_Gomez \n /Pedrito_Gonzalez_Martinez \n /Maria_Lopez_Hernandez \n /Luis_Ramirez_Sanchez")

    return ConversationHandler.END
def juanito_Command(update: Update, context: CallbackContext) -> int:
    # asks user to enter the trade
    update.effective_message.reply_text("Orden creada con éxito!")

    return ConversationHandler.END
# Handler Functions
def PlaceOrder(update: Update, context: CallbackContext) -> int:
    """Parses trade and places on MetaTrader account.   
    
    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    # checks if the trade has already been parsed or not

    
    return ORDEN
    return ConversationHandler.END

# Command Handlers
def welcome(update: Update, context: CallbackContext) -> None:
    """Sends welcome message to user.

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    welcome_message = "Prueba del FIC bot 5.0 Órdenes, /help para comandos"
    
    # sends messages to user
    update.effective_message.reply_text(welcome_message)

    return

def help(update: Update, context: CallbackContext) -> None:
    """Sends a help message when the command /help is issued

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    help_message = "Este bot está creado para crear, modificar y eliminar ÓRDENES"
    commands = "Lista de COMANDOS:\n/start : Muestra el mensaje de bienvenida\n/help : Muestra la lista de comandos\n/MostrarOrden : Muestra información de las órdenes (IDOK, IDBK, ID Orden BK, ID Tipo Orden OK, ID rol OK, ID Persona OK) \n/agregarOrden : Crea una orden \n/modificarOrden : Necesitas introducir su ID OK para modificarla \n/eliminarOrden : Necesitas introducir su ID OK para eliminarla"

    # sends messages to user
    update.effective_message.reply_text(help_message)
    update.effective_message.reply_text(commands)
    #update.effective_message.reply_text(trade_example + market_execution_example + limit_example + note)

    return

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation.   
    
    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    update.effective_message.reply_text("Command has been canceled.")

    # removes trade from user context data
    context.user_data['trade'] = None

    return ConversationHandler.END

def error(update: Update, context: CallbackContext) -> None:
    """Logs Errors caused by updates.

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    logger.warning('Update "%s" caused error "%s"', update, context.error)

    return

def main() -> None:
    """Runs the Telegram bot."""

    updater = Updater(TOKEN, use_context=True)

    # get the dispatcher to register handlers
    dp = updater.dispatcher

    # message handler
    dp.add_handler(CommandHandler("start", welcome))

    # help command handler
    dp.add_handler(CommandHandler("help", help))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("agregarOrden", agregarOrden_Command),CommandHandler("100", instituto100_Command),CommandHandler("DCC", negocioDCC_Command),CommandHandler("idCarrito", tipoOrdenIdCarrito_Command),CommandHandler("idCliente", idCliente_Command),CommandHandler("Juanito_Perez_Perez", juanito_Command),  ],
        states={
            ORDEN: [MessageHandler(Filters.text & ~Filters.command, PlaceOrder)],
            #TRADE: [MessageHandler(Filters.text & ~Filters.command, PlaceTrade)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # conversation handler for entering trade or calculating trade information
    dp.add_handler(conv_handler)

    # message handler for all messages that are not included in conversation handler
    dp.add_handler(MessageHandler(Filters.text, unknown_command))

    # log all errors
    dp.add_error_handler(error)
    
    # listens for incoming updates from Telegram
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_URL + TOKEN)
    updater.idle()

    return


if __name__ == '__main__':
    main()
