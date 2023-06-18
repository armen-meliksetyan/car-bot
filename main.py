from car_data_parser import CarDataParser
import telebot
from database import Database
import config


bot = telebot.TeleBot(config.bot_token)
parser = CarDataParser(config.url)
car_data = parser.parse_html()
db = Database(config.db_name, car_data)
db.clear_table()
db.store_in_database()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}! I am ready to work for you.")
    sticker_id = "CAACAgQAAxkBAAG6bGFka76jp5kO21_zXTpuuUjk6RPrqQACsCQAAlfTzgJaBgHsSnYuQi8E"
    bot.send_sticker(message.chat.id, sticker_id)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "📌 Commands:\n/addcar: Add a new car to the database. Provide the name, year, price, description, and image to create a comprehensive entry.\n/allcars: View all the cars in the database. Get details about each car, including its name, year, price, description and an accompanying image.")
    bot.send_message(message.chat.id, "I am in the phase of development. Please contact my admin if you have any questions or offers. https://t.me/armmeliksetyan")
    sticker_id = "CAACAgQAAxkBAAG6bVFka8Bc-kzIbshacQdPy7ttPpxziwACwiQAAlfTzgKDtQnxBwqyDC8E"
    bot.send_sticker(message.chat.id, sticker_id)

@bot.message_handler(commands=['allcars'])
def show_all_cars(message):
    cars = db.fetch()
    for car in cars:
        name = car[0]
        year = car[1]
        price = car[2]
        mileage = car[3]
        image_src = car[4]
        product_url = car[5]

        bot.send_photo(message.chat.id, photo=image_src, caption=f'Name: {name}\nYear: {year}\nPrice: {price}\nMileage: {mileage}\nVisit for more: {product_url}')

@bot.message_handler(commands=['filter'])
def start_filter(message):
    bot.send_message(message.chat.id, "Let's start filtering. Please provide the following information:\nCar model (or type 'any' to ignore model). You can also type 'cancel'.")

    bot.register_next_step_handler(message, process_filter)

def process_filter(message):
    model = message.text
    if model.lower() == 'cancel':
        bot.send_message(message.chat.id, "Filtering canceled.")
        return

    bot.send_message(message.chat.id, "Enter the year or type 'any' to ignore year. You can also type 'cancel'.")
    bot.register_next_step_handler(message, process_year, model)

def process_year(message, model):
    year = message.text
    if year.lower() == 'cancel':
        bot.send_message(message.chat.id, "Filtering canceled.")
        return

    if year.lower() == 'any':
        year = None
    else:
        try:
            year = int(year)
        except ValueError:
            bot.send_message(message.chat.id, "Invalid input. Year must be a number or 'any'.")
            return

    cars = db.filter_cars(model, year)

    if not cars:
        bot.send_message(message.chat.id, "There are no cars with details like these.")

    for car in cars:
        title = car[0]
        year = car[1]
        price = car[2]
        mileage = car[3]
        image_src = car[4]
        product_url = car[5]

        bot.send_photo(message.chat.id, photo=image_src, caption=f'Title: {title}\nYear: {year}\nPrice: {price}\nMileage: {mileage}\nVisit for more: {product_url}')

bot.polling(none_stop=True)