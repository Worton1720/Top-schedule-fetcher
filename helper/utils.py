import argparse


def validate_date(date):
    """Проверка корректности формата даты.

    Args:
        date (str): Дата для проверки.

    Raises:
        ValueError: Если дата имеет некорректный формат.
    """
    if not re.match(r"\d{4}-\d{2}-\d{2}", date):
        raise ValueError("Некорректный формат даты. Используйте ГГГГ-ММ-ДД.")


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
        default='{"authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbXNhcGkuaXRzdGVwLm9yZyIsImlhdCI6MTcwNzU3OTMzMiwiYXVkIjoxLCJleHAiOjE3MDc2MDgxMzIsImFwaUFwcGxpY2F0aW9uSWQiOjEsImFwaVVzZXJUeXBlSWQiOjEsInVzZXJJZCI6MjUsImlkQ2l0eSI6NDAyfQ.JhGdE9f0tAlel2Re4PJUMx0uO0dcn2rve7UDosVx_ic", "origin": "https://journal.top-academy.ru", "referer": "https://journal.top-academy.ru/", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}',
        help=f"{Fore.BLUE}Заголовки для запросов к серверу{Fore.RESET}",
    )
    return parser.parse_args()