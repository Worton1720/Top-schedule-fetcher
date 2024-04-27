from colorama import Fore
from modules.Schedule import SchedulePrinter, ScheduleManager
import pyfiglet


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
        self.print_welcome_message()

        while True:
            self.print_menu_options()
            choice = input("Введите номер действия: ")

            if choice == "1":
                self.get_schedule_by_date()
            elif choice == "2":
                self.get_current_week_schedule()
            elif choice == "3":
                print("До свидания!")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")

    def print_welcome_message(self):
        """Вывод приветственного сообщения."""
        text = pyfiglet.figlet_format("WELCOME", font="banner3-D")
        colored_text = Fore.CYAN + text + Fore.RESET
        print(colored_text)

    def print_menu_options(self):
        """Вывод опций меню."""
        print(Fore.BLUE + "\nВыберите действие:")
        print("1. Получить расписание на конкретный день")
        print("2. Получить расписание на текущую неделю")
        print("3. Выйти", Fore.RESET)

    def get_schedule_by_date(self):
        """Получение расписания на конкретный день."""
        date = input("Введите дату в формате ГГГГ-ММ-ДД: ")
        try:
            self.validate_date(date)
            schedule_data = self.schedule_manager.get_schedule_by_date(date)
            if schedule_data:
                SchedulePrinter.print_schedule(schedule_data)
                SchedulePrinter.save_to_json(schedule_data, f"schedule_{date}.json")
            else:
                print("Расписание на указанный день отсутствует.")
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
                day_of_week = ScheduleManager.get_weekday_by_date(date)
                print(f"{Fore.YELLOW}Дата: {date} ({day_of_week}){Fore.RESET}")
                print("Расписание на указанный день отсутствует.")
        SchedulePrinter.save_to_json(
            current_week_schedule, "schedule_current_week.json"
        )

    @staticmethod
    def validate_date(date):
        """Проверка корректности формата даты.

        Args:
            date (str): Дата для проверки.

        Raises:
            ValueError: Если дата имеет некорректный формат.
        """
        if not re.match(r"\d{4}-\d{2}-\d{2}", date):
            raise ValueError("Некорректный формат даты. Используйте ГГГГ-ММ-ДД.")
