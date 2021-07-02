"""Зарегистрироваться на https://openweathermap.org/api и
написать функцию, которая получает погоду в данный момент для города,
название которого получается через input.
https://openweathermap.org/current"""
import os
import requests
from dotenv import load_dotenv

load_dotenv(
    r"C:\Users\golub\Desktop\GeekBrains\homework\parsing\task_one\.env"
)
key = os.getenv('KEY_W', None)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}

def get_weather():
    inp = input('Enter the name of the city''\n')
    url= f'http://api.openweathermap.org/data/2.5/weather?q=London&appid={key}'
    if not (inp is None or inp ==''):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={inp}&appid={key}'
    r = requests.get(url, headers=headers)
    temp = r.json()
    return print('\n''temp_min:',round(temp['main']['temp_min'] - 273.15, 1),
                 '\n''temp_max',round(temp['main']['temp_max'] - 273.15, 1))

get_weather()