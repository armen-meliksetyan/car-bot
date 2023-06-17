import telebot
from database import create_connection, create_table
import base64

bot_token = '<token>'
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name}! I am ready to work for you.")
    sticker_id = "CAACAgQAAxkBAAG6bGFka76jp5kO21_zXTpuuUjk6RPrqQACsCQAAlfTzgJaBgHsSnYuQi8E"
    bot.send_sticker(message.chat.id, sticker_id)

@bot.message_handler(commands=['addcar'])
def add_car(message):
    msg = bot.send_message(message.chat.id, 'Enter the car name:')
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    car_name = message.text

    bot.send_message(message.chat.id, 'Enter the car year:')
    bot.register_next_step_handler(message, process_year_step, car_name)

def process_year_step(message, car_name):
    car_year = message.text

    bot.send_message(message.chat.id, 'Enter the car price:')
    bot.register_next_step_handler(message, process_price_step, car_name, car_year)

def process_price_step(message, car_name, car_year):
    car_price = message.text

    bot.send_message(message.chat.id, 'Enter the car description:')
    bot.register_next_step_handler(message, process_description_step, car_name, car_year, car_price)

def process_description_step(message, car_name, car_year, car_price):
    car_description = message.text

    bot.send_message(message.chat.id, 'Send the car image:')
    bot.register_next_step_handler(message, process_image_step, car_name, car_year, car_price, car_description)

def process_image_step(message, car_name, car_year, car_price, car_description):
    if message.photo:
        # Get the largest photo size available
        photo = message.photo[-1]

        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        encoded_image = base64.b64encode(downloaded_file).decode('utf-8')

        conn = create_connection()
        with conn:
            cursor = conn.cursor()
            insert_query = 'INSERT INTO cars (name, year, price, description, image) VALUES (?, ?, ?, ?, ?)'
            cursor.execute(insert_query, (car_name, car_year, car_price, car_description, encoded_image))
            conn.commit()

        bot.send_message(message.chat.id, f'Car details added successfully:\nName: {car_name}\nYear: {car_year}\nPrice: {car_price}\nDescription: {car_description}', parse_mode='Markdown', disable_notification=True)
        bot.send_photo(message.chat.id, photo=photo.file_id, caption=f'Name: {car_name}\nYear: {car_year}\nPrice: {car_price}\nDescription: {car_description}')
    else:
        bot.send_message(message.chat.id, 'No image was provided.')

@bot.message_handler(commands=['allcars'])
def show_all_cars(message):
    conn = create_connection()
    with conn:
        cursor = conn.cursor()
        select_query = 'SELECT name, year, price, description, image FROM cars'
        cursor.execute(select_query)
        cars = cursor.fetchall()

        for car in cars:
            name = car[0]
            year = car[1]
            price = car[2]
            description = car[3]
            image_encoded = car[4]

            image = base64.b64decode(image_encoded)

            bot.send_photo(message.chat.id, photo=image, caption=f'Name: {name}\nYear: {year}\nPrice: {price}\nDescription: {description}')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "📌 Commands:\n/addcar: Add a new car to the database. Provide the name, year, price, description, and image to create a comprehensive entry.\n/allcars: View all the cars in the database. Get details about each car, including its name, year, price, description and an accompanying image.")
    bot.send_message(message.chat.id, "I am in the phase of development. Please contact my admin if you have any questions or offers. https://t.me/armmeliksetyan")
    sticker_id = "CAACAgQAAxkBAAG6bVFka8Bc-kzIbshacQdPy7ttPpxziwACwiQAAlfTzgKDtQnxBwqyDC8E"
    bot.send_sticker(message.chat.id, sticker_id)

conn = create_connection()
create_table(conn)

bot.polling(none_stop=True)






