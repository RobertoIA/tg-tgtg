from os import getenv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

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


def latlon_to_address(latitude, longitude):
    geolocator = Nominatim(user_agent='tg-tgtg')

    for _ in range(1):  # maximum 3 attempts
        try:
            location = geolocator.reverse(f'{latitude}, {longitude}',
                                          addressdetails=False, zoom=16)
            return ', '.join(location.address.split(', ')[:2])
        except GeocoderTimedOut:
            print('timeout')
            pass

    return None


def start(update, context):
    location = context.user_data.get('address', 'Unknown')

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
    latlon = (update.message.location['latitude'],
              update.message.location['longitude'])
    context.user_data['latlon'] = latlon
    context.user_data['address'] = latlon_to_address(*latlon)

    update.message.reply_text(f'User location updated: '
                              f'{context.user_data["address"]}',
                              reply_markup=ReplyKeyboardRemove())


token = getenv('TOKEN')
updater = Updater(token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('test', test))

dispatcher.add_handler(MessageHandler(Filters.location, update_location))

updater.start_polling()
updater.idle()
