import json
import os
import sqlite3
import requests
import datetime
from colorama import Fore
from tabulate import tabulate
from modules.utils import get_file_path

DB_FILE = "schedule.db"


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


class SchedulePrinter:
    """Класс для вывода расписания."""

    @staticmethod
    def print_schedule(schedule_data):
        """Вывод расписания на экран.

        Args:
            schedule_data (dict): Данные расписания.
        """
        if schedule_data:
            sorted_schedule = sorted(schedule_data, key=lambda x: x["date"])
            current_date = None
            table_data = []
            for entry in sorted_schedule:
                if entry["date"] != current_date:
                    if current_date:
                        table_data.append([""])
                    date_obj = datetime.datetime.strptime(entry["date"], "%Y-%m-%d")
                    day_of_week = ScheduleManager.get_weekday_by_date(entry["date"])

                    print(
                        f"{Fore.LIGHTCYAN_EX}Дата: {entry['date']} ({day_of_week}){Fore.RESET}"
                    )
                    current_date = entry["date"]
                lesson_info = [
                    f"Урок: {entry['lesson']}",
                    f"Длительность пары: {entry['started_at']}|{entry['finished_at']}",
                    f"Преподаватель: {entry['teacher_name']}",
                    f"Предмет: {entry['subject_name']}",
                    f"Аудитория: {entry['room_name']}",
                ]
                table_data.append(lesson_info)
            print(tabulate(table_data, tablefmt="grid"))
        else:
            print(f"{Fore.YELLOW}Расписание на указанный день отсутствует.{Fore.RESET}")

    @staticmethod
    def save_to_json(schedule_data, filename):
        if not os.path.exists(filename):
            open(filename, 'w').close()

        with open(filename, 'w', encoding='cp1251') as file:
            json.dump(schedule_data, file, ensure_ascii=False)

    @staticmethod
    def save_to_database(schedule_data, db_file_name: str = DB_FILE):
        """Сохранение данных в базу данных.

        Args:
            schedule_data (dict): Данные расписания.
        """
        db_file_name = get_file_path(db_file_name)
        conn = sqlite3.connect(db_file_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                lesson TEXT,
                started_at TEXT,
                finished_at TEXT,
                teacher_name TEXT,
                subject_name TEXT,
                room_name TEXT
            )
        """
        )
        for date, entries in schedule_data.items():
            for entry in entries:
                cursor.execute(
                    """
                    INSERT INTO schedule (date, lesson, started_at, finished_at, teacher_name, subject_name, room_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        date,
                        entry["lesson"],
                        entry["started_at"],
                        entry["finished_at"],
                        entry["teacher_name"],
                        entry["subject_name"],
                        entry["room_name"],
                    ),
                )
        conn.commit()
        conn.close()
        print(f"{Fore.GREEN}Данные успешно сохранены в базу данных.{Fore.RESET}")


class ScheduleManager:
    """Класс для управления расписанием."""

    def __init__(self, schedule_fetcher):
        """Инициализация объекта ScheduleManager.

        Args:
            schedule_fetcher (ScheduleFetcher): Объект для получения расписания.
        """
        self.schedule_fetcher = schedule_fetcher

    @staticmethod
    def get_weekday_by_date(date):
        """Получение дня недели по дате.

        Args:
            date (str): Дата в формате 'ГГГГ-ММ-ДД'.

        Returns:
            str: Название дня недели на русском.
        """
        weekdays = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье",
        }
        date_obj = datetime.datetime.strptime(date, r"%Y-%m-%d")
        return weekdays[date_obj.weekday()]

    def get_schedule_by_date(self, date):
        """Получение расписания на указанный день.

        Args:
            date (str): Дата в формате 'ГГГГ-ММ-ДД'.

        Returns:
            dict: Данные расписания на указанный день.
        """
        return self.schedule_fetcher.fetch_schedule(
            "/get-by-date", params={"date_filter": date}
        )

    def get_schedule_for_week(self):
        """Получение расписания на неделю.

        Returns:
            dict: Данные расписания на неделю.
        """
        return self.schedule_fetcher.fetch_schedule("/get-month")

    def get_current_week_schedule(self):
        """Получение расписания на текущую неделю.

        Returns:
            dict: Данные расписания на текущую неделю.
        """
        current_week_dates = self.get_current_week_dates()
        current_week_schedule = {}

        for date in current_week_dates:
            schedule_data = self.get_schedule_by_date(date)
            current_week_schedule[date] = schedule_data

        return current_week_schedule

    @staticmethod
    def get_current_week_dates():
        """Возвращает список дат текущей недели от понедельника до воскресенья."""
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        return [
            (start_of_week + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(7)
        ]
