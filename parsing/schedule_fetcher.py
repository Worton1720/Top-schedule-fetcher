import requests
from colorama import Fore


class ScheduleFetcher:
    """Класс для получения расписания с сервера."""

    def __init__(self, url, headers):
        """Инициализация объекта ScheduleFetcher.

        Args:
            url (str): URL сервера.
            headers (dict): Заголовки для запросов к серверу.
        """
        self.url = url
        self.headers = headers

    def fetch_schedule(self, endpoint, params=None):
        """Получение расписания с сервера.

        Args:
            endpoint (str): Конечная точка API для запроса.
            params (dict): Параметры запроса.

        Returns:
            dict: Данные расписания в формате JSON или None в случае ошибки.
        """
        try:
            response = requests.get(
                self.url + endpoint, headers=self.headers, params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Ошибка при выполнении запроса: {e}{Fore.RESET}")
            return None
        except Exception as e:
            print(f"{Fore.RED}Произошла непредвиденная ошибка: {e}{Fore.RESET}")
            return None
