import json
from colorama import Fore
from helper.utils import get_args
from parsing.schedule_fetcher import ScheduleFetcher
from parsing.schedule_manager import ScheduleManager
from helper.menu_controller import MenuController


def main():
    args = get_args()

    headers = json.loads(args.headers)

    print(
        f"{Fore.MAGENTA}Добро пожаловать в программу получения расписания с сайта TOP!{Fore.RESET}"
    )

    schedule_fetcher = ScheduleFetcher(args.url, headers)
    schedule_manager = ScheduleManager(schedule_fetcher)
    menu_controller = MenuController(schedule_manager)
    menu_controller.run_menu()


if __name__ == "__main__":
    main()
