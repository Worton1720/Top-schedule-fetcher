import argparse
import json
import os
from colorama import Fore
import requests
from pathlib import Path


def get_args():
    """Получение аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Получение расписания с сервера")
    parser.add_argument(
        "action",
        nargs="?",
        choices=["day", "week"],
        default="week",
        help=f"{Fore.BLUE}Выберите действие: 'day' для получения расписания на день, 'week' для получения расписания на неделю{Fore.RESET}",
    )
    parser.add_argument(
        "--date",
        help=f"{Fore.BLUE}Дата для получения расписания на день (формат: ГГГГ-ММ-ДД){Fore.RESET}",
    )
    parser.add_argument(
        "--url",
        default="https://msapi.top-academy.ru/api/v2/schedule/operations",
        help=f"{Fore.BLUE}URL для запросов к серверу{Fore.RESET}",
    )
    parser.add_argument(
        "--headers",
        default='{"authorization": "", "referer": "https://journal.top-academy.ru/", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}',
        help=f"{Fore.BLUE}Заголовки для запросов к серверу{Fore.RESET}",
    )
    return parser.parse_args()


def get_refresh_token(username: str, password: str) -> str | None:
    """Запрос refresh_token."""
    url_login = "https://msapi.top-academy.ru/api/v2/auth/login"
    payload = {
        "application_key": "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
        "id_city": None,
        "username": username,
        "password": password,
    }
    headers_login = {
        "Content-Type": "application/json",
        "Referer": "https://journal.top-academy.ru/",
    }
    response = requests.post(url_login, json=payload, headers=headers_login)

    if response.status_code == 200:
        response_data = response.json()
        if "refresh_token" in response_data:
            refresh_token = response_data["refresh_token"]
            print("Refresh token:", refresh_token)
            return refresh_token
        else:
            print("Refresh token не найден в ответе.")
            return None
    else:
        print("Ошибка при отправке запроса:", response.status_code)
        return None


def save_data(refresh_token):
    path = get_file_path("user_data.json")
    data = {"refresh_token": refresh_token, "username": "", "password": ""}
    with open(path, "w") as file:
        json.dump(data, file)


def load_data():
    path = get_file_path("user_data.json")
    if os.path.exists(path):
        with open(path, "r") as file:
            data = json.load(file)
            return data.get("refresh_token"), data.get("username"), data.get("password")
    return None, None, None


def check_token_validity(url, headers):
    """Проверка релевантности refresh token."""
    try:
        requests.get(url, headers=headers)
        return True
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Ошибка при выполнении запроса: {e}{Fore.RESET}")
        return False
    except Exception as e:
        print(f"{Fore.RED}Произошла непредвиденная ошибка: {e}{Fore.RESET}")
        return False


def get_file_path(file_name: str = None) -> str:
    """Return the path to a file in the directory of the current script."""
    try:
        dir_path = Path(__file__).resolve().parent
        return str(dir_path if file_name is None else dir_path / file_name)
    except Exception as e:
        print(f"Ошибка: {e}")
        return "900"