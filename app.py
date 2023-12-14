from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
from slack_sdk import WebClient
import time
import datetime

from dotenv import load_dotenv

load_dotenv()

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Получить статусы /get_statuses")


async def get_statuses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = ''
    users_in_group = client.usergroups_users_list(usergroup='S046Z9NF49H')['users']
    for user in users_in_group:
        profile = client.users_profile_get(user=user)['profile']
        if profile['status_expiration'] != 0:
            status_duration = datetime.datetime.now()+datetime.timedelta(seconds=int(profile['status_expiration'])-time.time())
            status = profile['status_text'] + ', до ' + status_duration.strftime('%H:%M')
            message += profile['real_name'] + ' - ' + status + '\n'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token=os.environ.get("TG_BOT_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    get_statuses_handler = CommandHandler('get_statuses', get_statuses)
    application.add_handler(start_handler)
    application.add_handler(get_statuses_handler)

    application.run_polling()
