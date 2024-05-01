"""
Этот модуль представляет возможность скрытого ввода.
"""
from getpass import getpass
import json
from colorama import Fore
from modules.schedule import ScheduleFetcher
from modules.schedule import ScheduleManager
from modules.menu_controller import MenuController
from modules.utils import get_args, load_data, check_token_validity, get_refresh_token, save_data

DB_FILE = "schedule.db"


def main() -> None:
    args = get_args()
    headers = json.loads(args.headers)

    print(
        f"{Fore.MAGENTA}Добро пожаловать в программу получения расписания с сайта TOP!{Fore.RESET}"
    )

    refresh_token = load_data(DB_FILE)

    if not (refresh_token and check_token_validity(args.url, headers)):
        username = input("Введите ваш логин: ").strip()
        password = getpass("Введите ваш пароль(пороль скрыт при записи): ").strip()

        refresh_token = get_refresh_token(username, password)
        if refresh_token:
            save_data(refresh_token, DB_FILE)
        else:
            print("Не удалось получить refresh token. Пожалуйста, повторите попытку.")
            return

    headers["authorization"] = f"Bearer {refresh_token}"

    schedule_fetcher = ScheduleFetcher(args.url, headers)
    schedule_manager = ScheduleManager(schedule_fetcher)
    menu_controller = MenuController(schedule_manager)
    menu_controller.run_menu()


if __name__ == "__main__":
    main()
