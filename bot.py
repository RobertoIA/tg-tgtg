from os import getenv

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)


def start(update, context):
    location = context.user_data.get('location', None)
    location = (f'{location["latitude"]:.1f}, {location["longitude"]:.1f}'
                if location else 'Unknown')

    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton('Option A1'), KeyboardButton('Option A2')],
         [KeyboardButton('Option B')],
         [KeyboardButton(f'Update my location\nCurrent: {location}',
                         request_location=True)]],
        one_time_keyboard=True
    )
    update.effective_message.reply_text('Select an option:',
                                        reply_markup=keyboard)


def test(update, context):
    pass


def update_location(update, context):
    context.user_data['location'] = update.message.location
    update.message.reply_text('User location updated.',
                              reply_markup=ReplyKeyboardRemove())


token = getenv('TOKEN')
updater = Updater(token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('test', test))

dispatcher.add_handler(MessageHandler(Filters.location, update_location))

updater.start_polling()
updater.idle()
