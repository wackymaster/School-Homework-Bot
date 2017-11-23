from icalendar import Calendar, Event
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import vobject
import datetime
import dateutil.parser
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello Fellows, I am a Telegram Bot that forwards homework based on the school calendar')

def help(bot,update):
    update.message.reply_text('/Steele10H for Steele 10H HW \n/Steele10SC for Steele 10H HW \n/HoseyH for Hosey Physics Honors')

def request(url):
    r = requests.get(url)
    open('icalfeed.ics', 'wb').write(r.content)
    # update.message.reply_text('Request Received')
    cal_data = Calendar.from_ical(open('icalfeed.ics', 'rb').read())
    for event in cal_data.walk('vevent'):
        date = event.get('dtstart')
        date = dateutil.parser.parse(str(date.dt))
        margin = datetime.timedelta(days=2)
        today = datetime.datetime.today().date()
        if today <= date.date() <= today + margin:
            date = date.strftime('%b %d')
            # hwstring = str(date) + ': ' + str(event.get('SUMMARY')) + ' ' + event.get('DESCRIPTION')
            # update.message.reply_text(hwstring)
            output = str(date) + ': '
            if event.get('SUMMARY'):
                output = output + str(event.get('SUMMARY')) + ' '
            if event.get('DESCRIPTION'):
                output = output + str(event.get('DESCRIPTION'))
            return(output)

def steele10H(bot,update):
    #update.message.reply_text('Attempting Request...')
    url = "https://www.pittsfordschools.org//site/handlers/icalfeed.ashx?MIID=29561"
    output = request(url=url)
    update.message.reply_text(output)

def steeleSC(bot,update):
    #update.message.reply_text('Attempting Request...')
    url = "https://www.pittsfordschools.org/site/handlers/icalfeed.ashx?MIID=29563"
    output = request(url=url)
    update.message.reply_text(output)


def HoseyH(bot, update):
    # update.message.reply_text('Attempting Request...')
    url = "https://www.pittsfordschools.org/site/handlers/icalfeed.ashx?MIID=32661"
    output = request(url=url)
    update.message.reply_text(output)

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("475979582:AAGDqhfpd2zV8DRylIVb6ZqyD9DXTOG2m8Y")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("steele10H", steele10H))
    dp.add_handler(CommandHandler("steele10h", steele10H))
    dp.add_handler(CommandHandler("Steele10h", steele10H))
    dp.add_handler(CommandHandler("Steele10H", steele10H))
    dp.add_handler(CommandHandler("Steele10SC", steeleSC))
    dp.add_handler(CommandHandler("steele10sc", steeleSC))
    dp.add_handler(CommandHandler("steelesc", steeleSC))
    dp.add_handler(CommandHandler("HoseyH", HoseyH))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()