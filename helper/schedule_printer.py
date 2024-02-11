import json
from colorama import Fore
import datetime
import tabulate


class SchedulePrinter:
    """Класс для вывода расписания."""

    @staticmethod
    def print_schedule(schedule_data):
        russian_days = {
            "Monday": "Понедельник",
            "Tuesday": "Вторник",
            "Wednesday": "Среда",
            "Thursday": "Четверг",
            "Friday": "Пятница",
            "Saturday": "Суббота",
            "Sunday": "Воскресенье",
        }

        if schedule_data:
            sorted_schedule = sorted(schedule_data, key=lambda x: x["date"])
            current_date = None
            table_data = []
            for entry in sorted_schedule:
                if entry["date"] != current_date:
                    date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d")
                    day_of_week = russian_days[
                        date_obj.strftime("%A")
                    ]  # Получаем день недели на русском
                    table_data.append(
                        [
                            f"{Fore.MAGENTA}Дата: {entry['date']} ({day_of_week}){Fore.RESET}"
                        ]
                    )
                    current_date = entry["date"]
                lesson_info = [
                    f"{Fore.BLUE}Урок: {entry['lesson']}",
                    f"Время начала: {entry['started_at']}",
                    f"Время окончания: {entry['finished_at']}",
                    f"Преподаватель: {entry['teacher_name']}",
                    f"Предмет: {entry['subject_name']}",
                    f"Аудитория: {entry['room_name']}{Fore.RESET}",
                ]
                table_data.append(lesson_info)
            print(tabulate(table_data, tablefmt="grid"))
        else:
            print(f"{Fore.YELLOW}Расписание на указанный день отсутствует.{Fore.RESET}")

    @staticmethod
    def save_to_json(data, filename):
        """Сохранение данных в JSON файл.

        Args:
            data (dict): Данные для сохранения.
            filename (str): Имя файла для сохранения.
        """
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(
                f'{Fore.GREEN}Данные успешно сохранены в файл: "{filename}"{Fore.RESET}'
            )
        except Exception as e:
            print(
                f'{Fore.RED}Ошибка при сохранении данных в файл "{filename}": {e}{Fore.RESET}'
            )
