from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

TOKEN = 6795150115:AAECKTUAE99ilDgBT9wWKoc1Smp4NOLZeaU
bot = Bot(TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Karachi'))

# Registered users' chat IDs
users = []

# Command to register a user
def register(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id not in users:
        users.append(chat_id)
        update.message.reply_text('You are now registered for daily attendance.')
    else:
        update.message.reply_text('You are already registered.')

# Callback for button press
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    # Log or save attendance here
    query.edit_message_text(text="Attendance recorded!")

# Sends attendance message with button
def send_attendance():
    for chat_id in users:
        keyboard = [[InlineKeyboardButton("Mark Attendance", callback_data='1')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=chat_id, text="Please mark your attendance.", reply_markup=reply_markup)

# Schedule the job
scheduler.add_job(send_attendance, 'cron', hour=6, minute=0)
scheduler.start()

dispatcher.add_handler(CommandHandler('register', register))
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
