from telegram.ext import Updater,InlineQueryHandler,RegexHandler, MessageHandler,CommandHandler,ConversationHandler,CallbackQueryHandler,Filters
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from lang_dict import *
import logging
global LANG
LANG = 'EN'
global BOT_TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
MENU, SET_STAT, FILES, DELETE, NEW, = range(5)
STATE = MENU

def start(bot , update):
    """
    Start function. Displayed whenever /start command is called.
    """
    # This is used to change the language of the keybaord
    message = "Hey i am a bot...."
   
    update.message.reply_text(message)
    return MENU

def menu(bot, update):
    """
    Main menu function.
    This will display the options from the main menu.
    """
    print('menu callled')
    keyboard = [[see_files[LANG], new_file[LANG]],
                [delete_file[LANG]]]

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    user = update.message.from_user
    logger.info("Menu command requested by {}.".format(user.first_name))
    update.message.reply_text(main_menu[LANG], reply_markup=reply_markup)

    return SET_STAT
    
def set_state(bot, update):
    """
    Set option selected from menu.
    """
    # Set state:
    global STATE
    if update.message.text == see_files[LANG]:
        STATE = FILES
        files(bot, update)
        return MENU
    elif update.message.text == new_file[LANG]:
        STATE = NEW
        new_torrent(bot, update)
        return MENU
    elif update.message.text == delete_file[LANG]:
        STATE = DELETE
        delete(bot, update)
        return MENU
    else:
        STATE = MENU
        return MENU

def files(bot , update):
    print('select file')
    pass


def new_torrent(bot , update):
    print('new torrent')
    pass


def delete(bot , update):
    print('ollala')
    pass


def about_bot(bot, update):
    """
    About function. Displays info about DisAtBot.
    """
    user = update.message.from_user
    logger.info("About info requested by {}.".format(user.first_name))
    bot.send_message(chat_id=update.message.chat_id, text=about_info[LANG])
    bot.send_message(chat_id=update.message.chat_id, text=back2menu[LANG])
    return

def help(bot, update):
    """
    Help function.
    This displays a set of commands available for the bot.
    """
    user = update.message.from_user
    logger.info("User {} asked for help.".format(user.first_name))
    update.message.reply_text(help_info[LANG],
                              reply_markup=ReplyKeyboardRemove())
def cancel(bot, update):
    """
    User cancelation function.
    Cancel conersation by user.
    """
    user = update.message.from_user
    logger.info("User {} canceled the conversation.".format(user.first_name))
    update.message.reply_text(goodbye[LANG],
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """
    Main function.
    This function handles the conversation flow by setting
    states on each step of the flow. Each state has its own
    handler for the interaction with the user.
    """
    global LANG
    # Create the EventHandler and pass it your bot's token.
    
    updater = Updater(BOT_TOKEN)
    # Get the dispatcher to register handlers:
    dp = updater.dispatcher

    # Add conversation handler with predefined states:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MENU: [CommandHandler('menu', menu)],
            SET_STAT: [RegexHandler(
                        '^({}|{}|{})$'.format(
                            see_files['EN'], new_file['EN'],
                            delete_file['EN']),
                        set_state),
                       RegexHandler(
                        '^({}|{}|{})$'.format(
                            see_files['EN'], new_file['EN'],
                            delete_file['EN'],),
                        set_state)],
        },

        fallbacks=[CommandHandler('menu', cancel),
                   CommandHandler('help', help)]
    )

    dp.add_handler(conv_handler)

    # Log all errors:
    dp.add_error_handler(error)

    # Start DisAtBot:
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process
    # receives SIGINT, SIGTERM or SIGABRT:
    updater.idle()


if __name__ == '__main__':
    main()

