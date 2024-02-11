from colorama import Fore
from utils import validate_date
from schedule_printer import SchedulePrinter


class MenuController:
    """Класс для управления меню программы."""

    def __init__(self, schedule_manager):
        """Инициализация объекта MenuController.

        Args:
            schedule_manager (ScheduleManager): Объект для управления расписанием.
        """
        self.schedule_manager = schedule_manager

    def run_menu(self):
        """Запуск основного меню программы."""
        while True:
            print(Fore.BLUE + "\nВыберите действие:")
            print("1. Получить расписание на конкретный день")
            print("2. Получить расписание на текущую неделю")
            print("3. Выйти", Fore.RESET)

            choice = input(Fore.GREEN + "Введите номер действия: " + Fore.RESET)

            if choice == "1":
                self.get_schedule_by_date()
            elif choice == "2":
                self.get_current_week_schedule()
            elif choice == "3":
                print(f"{Fore.MAGENTA}До свидания!{Fore.RESET}")
                break
            else:
                print(f"{Fore.RED}Некорректный ввод. Попробуйте снова.{Fore.RESET}")

    def get_schedule_by_date(self):
        """Получение расписания на конкретный день."""
        date = input("Введите дату в формате ГГГГ-ММ-ДД: ")
        try:
            validate_date(date)
            schedule_data = self.schedule_manager.get_schedule_by_date(date)
            if schedule_data:
                SchedulePrinter.print_schedule(schedule_data)
                SchedulePrinter.save_to_json(schedule_data, f"schedule_{date}.json")
            else:
                print(
                    f"{Fore.YELLOW}Расписание на указанный день отсутствует.{Fore.RESET}"
                )
        except ValueError as e:
            print(f"{Fore.RED}{e}{Fore.RESET}")

    def get_current_week_schedule(self):
        """Получение расписания на текущую неделю."""
        current_week_schedule = self.schedule_manager.get_current_week_schedule()
        print("Расписание на текущую неделю:")
        for date, schedule_data in current_week_schedule.items():
            if schedule_data:
                SchedulePrinter.print_schedule(schedule_data)
            else:
                print(f"День: {date}")
                print(
                    f"{Fore.YELLOW}Расписание на указанный день отсутствует.{Fore.RESET}"
                )
        SchedulePrinter.save_to_json(
            current_week_schedule, "schedule_current_week.json"
        )
