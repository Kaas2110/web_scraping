"""Посмотреть документацию к API GitHub, разобраться как
вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json; написать функцию, возвращающую
список репозиториев."""

import json
import requests
from dotenv import load_dotenv

load_dotenv("./.env")

def get_repo(x="Kaas2110"):
    request = requests.get(f"https://api.github.com/users/{x}/repos")
    with open("data.json", "w") as f:
        json.dump(request.json(), f)
    for i in request.json():
        print(i["name"])

get_repo("Diyago")
