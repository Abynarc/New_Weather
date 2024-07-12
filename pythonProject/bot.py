import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime, timedelta
import pytz

# Настройки
TELEGRAM_TOKEN = '7206246769:AAEg6AJ5VrLkbqApze_agUwEd-MWh2heNxY'
WEATHER_API_KEY = '9a9c7fa2ff96300d51c030baa6b849e0'
CITY_NAME = 'Volgograd'
WEATHER_API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}&units=metric'

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Функция получения погоды
def get_weather():
    response = requests.get(WEATHER_API_URL)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f'Погода в {CITY_NAME}: {weather}, температура: {temperature}°C'
    else:
        return 'Не удалось получить данные о погоде.'

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот, который отправляет погоду в Волгограде каждый день в 7 утра.')

# Команда /weather
def weather(update: Update, context: CallbackContext) -> None:
    weather_info = get_weather()
    update.message.reply_text(weather_info)

# Главная функция
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", weather))

    # Планировщик
    job_queue = updater.job_queue
    moscow_tz = pytz.timezone('Europe/Moscow')
    target_time = datetime.now(moscow_tz).replace(hour=7, minute=0, second=0, microsecond=0)
    if target_time < datetime.now(moscow_tz):
        target_time += timedelta(days=1)
    interval = 24 * 60 * 60
    job_queue.run_repeating(lambda context: context.bot.send_message(chat_id='259139918', text=get_weather()),
                            interval, first=target_time)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()