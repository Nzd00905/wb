import logging
import requests
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackContext

# Replace with your Telegram Bot API token
TELEGRAM_BOT_TOKEN = '7766734058:AAFU2PDow5D-Iu5YSvVeuD_7Qs6eK1049sA'

# API URL for SMS service
SMS_API_URL = 'https://tcsdemonic.vercel.app/api/bomber'

# Welcome image URL
WELCOME_IMAGE_URL = 'https://techviral.net/wp-content/uploads/2020/09/smsbomber-latest.jpg'

# Configure logging to log errors and info
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to send SMS using the provided API
def send_sms(phone_number, amount):
    url = f"{SMS_API_URL}?phone={phone_number}&amount={amount}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return "SMS sent successfully! ✔"
        else:
            return f"Failed to send SMS. Error: {response.text}"
    except Exception as e:
        return f"Error occurred while trying to send SMS: {str(e)}"

# Command handler for sending SMS
async def send_sms_command(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) < 2:
            await update.message.reply_text('Usage: /send_sms <phone_number> <amount>')
            return

        phone_number = context.args[0]
        amount = context.args[1]
        
        result = send_sms(phone_number, amount)
        
        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Function to handle the '/start' command
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    full_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
    welcome_message = f"Welcome, {full_name}! \n\nUse /send_sms <phone_number> <amount> to send SMS.\n\n © Md.Sabbir Sheikh"

    await update.message.reply_photo(WELCOME_IMAGE_URL, caption=welcome_message)

# Main function to set up the bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send_sms", send_sms_command))

    app.run_polling()

if __name__ == '__main__':
    main()
