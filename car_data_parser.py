from bs4 import BeautifulSoup
import requests
from car_data import CarData


class CarDataParser:
    def __init__(self, url):
        self.url = url
        self.html_content = self.fetch_html_content()
        self.car_data = []

    def fetch_html_content(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.content

    def parse_html(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        car_items = soup.find_all('div', class_='card')

        for car in car_items:
            title = car.find('span', class_='card-title bold').text.strip()
            year = car.find('div', class_='card-content').find('span', class_='bold').text.strip()
            price_element = car.find('div', class_='card-content').find('span', class_='')
            price = price_element.text.strip() if price_element else 'N/A'
            mileage_element = car.find('div', class_='card-action').find('span', class_='left')
            mileage = mileage_element.text.strip() if mileage_element else 'N/A'  
            image_src = self.url + car.find('img')['src']
            product_url = self.url + car.find('a')['href']

            print('Vehicle Title:', title)
            print('Year:', year)
            print('Price:', price)
            print('Mileage:', mileage)
            print('Image URL:', image_src)
            print('Product URL:', product_url)
            print('---')

            car_data = CarData(title, year, price, mileage, image_src, product_url)
            self.car_data.append(car_data)

        return self.car_data

    
