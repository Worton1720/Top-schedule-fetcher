import getpass
import json
from colorama import Fore
from modules.utils import *
from modules.Schedule import ScheduleFetcher
from modules.Schedule import ScheduleManager
from modules.menu_controller import MenuController


def main():
    args = get_args()
    headers = json.loads(args.headers)

    print(
        f"{Fore.MAGENTA}Добро пожаловать в программу получения расписания с сайта TOP!{Fore.RESET}"
    )

    refresh_token, username, password = load_data()

    if not (refresh_token and check_token_validity(args.url, headers)):
        if not (username and password):
            username = input("Введите ваш логин: ").strip()
            password = getpass.getpass("Введите ваш пароль: ").strip()

        refresh_token = get_refresh_token(username, password)
        if refresh_token:
            save_data(refresh_token)
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
