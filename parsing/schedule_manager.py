import datetime


class ScheduleManager:
    """Класс для управления расписанием."""

    @staticmethod
    def sort_schedule_by_day(schedule_data):
        """Сортировка расписания по дням.

        Args:
            schedule_data (list): Данные расписания.

        Returns:
            dict: Отсортированные данные расписания по дням.
        """
        sorted_schedule = {}
        for entry in schedule_data:
            date = entry["date"]
            if date not in sorted_schedule:
                sorted_schedule[date] = []
            sorted_schedule[date].append(entry)
        return sorted_schedule

    def __init__(self, schedule_fetcher):
        """Инициализация объекта ScheduleManager.

        Args:
            schedule_fetcher (ScheduleFetcher): Объект для получения расписания.
        """
        self.schedule_fetcher = schedule_fetcher

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
        end_of_week = start_of_week + datetime.timedelta(days=6)
        return [
            (start_of_week + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(7)
        ]
