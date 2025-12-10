from datetime import date
from statlib.database import Cursor, ensure_cursor, TimeSummary


class StatsHandler:
    """
    Provides listening statistics for daily, weekly, and monthly periods.
    """


    @staticmethod
    @ensure_cursor
    def get_today(*, cursor: Cursor = None) -> TimeSummary:
        """
        Retrieve total listening time for today.

        :param cursor: Database cursor.
        :return: TimeSummary containing total seconds.
        """
        cursor.execute(
            """
            SELECT COALESCE(SUM(duration), 0)
            FROM listening_data
            WHERE DATE(timestamp) = CURDATE()
            """
        )
        (total,) = cursor.fetchone()
        return TimeSummary(total_seconds=total)



    @staticmethod
    @ensure_cursor
    def get_yesterday(*, cursor: Cursor = None) -> TimeSummary:
        """
        Retrieve total listening time for yesterday.

        :param cursor: Database cursor.
        :return: TimeSummary containing total seconds.
        """
        cursor.execute(
            """
            SELECT COALESCE(SUM(duration), 0)
            FROM listening_data
            WHERE DATE(timestamp) = CURDATE() - INTERVAL 1 DAY
            """
        )
        (total,) = cursor.fetchone()
        return TimeSummary(total_seconds=total)



    @staticmethod
    @ensure_cursor
    def get_this_week(*, cursor: Cursor = None) -> TimeSummary:
        """
        Retrieve total listening time for the current week.

        :param cursor: Database cursor.
        :return: TimeSummary containing total seconds.
        """
        cursor.execute(
            """
            SELECT COALESCE(SUM(duration), 0)
            FROM listening_data
            WHERE YEARWEEK(timestamp, 1) = YEARWEEK(CURDATE(), 1)
            """
        )
        (total,) = cursor.fetchone()
        return TimeSummary(total_seconds=total)



    @staticmethod
    @ensure_cursor
    def get_last_week(*, cursor: Cursor = None) -> TimeSummary:
        """
        Retrieve total listening time for the previous week.

        :param cursor: Database cursor.
        :return: TimeSummary containing total seconds.
        """
        cursor.execute(
            """
            SELECT COALESCE(SUM(duration), 0)
            FROM listening_data
            WHERE YEARWEEK(timestamp, 1) = YEARWEEK(CURDATE(), 1) - 1
            """
        )
        (total,) = cursor.fetchone()
        return TimeSummary(total_seconds=total)



    @staticmethod
    @ensure_cursor
    def get_this_month(*, cursor: Cursor = None) -> TimeSummary:
        """
        Retrieve total listening time for the current month.

        :param cursor: Database cursor.
        :return: TimeSummary containing total seconds.
        """
        cursor.execute(
            """
            SELECT COALESCE(SUM(duration), 0)
            FROM listening_data
            WHERE YEAR(timestamp) = YEAR(CURDATE())
              AND MONTH(timestamp) = MONTH(CURDATE())
            """
        )
        (total,) = cursor.fetchone()
        return TimeSummary(total_seconds=total)



    @staticmethod
    @ensure_cursor
    def get_last_month(*, cursor: Cursor = None) -> TimeSummary:
        """
        Retrieve total listening time for the previous month.

        :param cursor: Database cursor.
        :return: TimeSummary containing total seconds.
        """
        cursor.execute(
            """
            SELECT COALESCE(SUM(duration), 0)
            FROM listening_data
            WHERE YEAR(timestamp) = YEAR(CURDATE() - INTERVAL 1 MONTH)
              AND MONTH(timestamp) = MONTH(CURDATE() - INTERVAL 1 MONTH)
            """
        )
        (total,) = cursor.fetchone()
        return TimeSummary(total_seconds=total)
    

    @staticmethod
    @ensure_cursor
    def get_this_year(*, cursor: Cursor = None) -> TimeSummary:
        """
        Retrieve total listening time for the current year.

        :param cursor: Database cursor.
        :return: A TimeSummary containing total seconds listened in the year.
        """
        cursor.execute(
            """
            SELECT COALESCE(SUM(duration), 0)
            FROM listening_data
            WHERE YEAR(timestamp) = YEAR(CURDATE())
            """
        )
        (total,) = cursor.fetchone()
        return TimeSummary(total_seconds=total)
    

    @staticmethod
    @ensure_cursor
    def get_today_hourly_breakdown(*, cursor: Cursor = None) -> list[int]:
        """
        Return a list of 24 integers representing minutes listened per hour today.
        Index 0 = 00:00–00:59, index 23 = 23:00–23:59.
        """
        cursor.execute(
            """
            SELECT HOUR(timestamp) AS hour, SUM(duration)
            FROM listening_data
            WHERE DATE(timestamp) = CURDATE()
            GROUP BY hour
            ORDER BY hour
            """
        )

        results = cursor.fetchall()

        hours = [0] * 24
        for hour, seconds in results:
            hours[hour] = round(seconds / 60)

        return hours


    @staticmethod
    @ensure_cursor
    def get_this_week_daily_breakdown(*, cursor: Cursor = None) -> list[int]:
        """
        Retrieve daily listening totals for the current week.

        Returns a list of 7 integers, representing:
        [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]

        :param cursor: Database cursor.
        :return: List of minutes listened each day.
        """
        cursor.execute(
            """
            SELECT 
                WEEKDAY(timestamp) AS day_index,
                SUM(duration) AS total_seconds
            FROM listening_data
            WHERE YEARWEEK(timestamp, 1) = YEARWEEK(CURDATE(), 1)
            GROUP BY WEEKDAY(timestamp)
            ORDER BY day_index
            """
        )

        rows = cursor.fetchall()

        result = [0] * 7
        for day_index, total_seconds in rows:
            result[day_index] = round(total_seconds / 60)

        return result
    

    @staticmethod
    @ensure_cursor
    def get_this_month_daily_breakdown(*, cursor: Cursor = None) -> list[int]:
        """
        Returns a list of daily listening minutes for the current month.

        Each index represents a day of the month (1–31 depending on month length).
        Values are rounded minutes listened.
        
        :param cursor: Database cursor (automatically injected by ensure_cursor)
        :return: List of integers representing minutes listened per day.
        """
        cursor.execute("""
            SELECT 
                DAY(timestamp) AS day,
                SUM(duration) AS total_seconds
            FROM listening_data
            WHERE 
                YEAR(timestamp) = YEAR(CURRENT_DATE())
                AND MONTH(timestamp) = MONTH(CURRENT_DATE())
            GROUP BY day
            ORDER BY day;
        """)

        rows = cursor.fetchall()
        days = {day: total for day, total in rows}

        from datetime import datetime
        import calendar

        now = datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]

        result = []
        for d in range(1, days_in_month + 1):
            result.append(round(days.get(d, 0) / 60))

        return result
    

    @staticmethod
    @ensure_cursor
    def get_this_year_monthly_breakdown(*, cursor: Cursor = None) -> list[int]:
        """
        Retrieve monthly listening totals for the current year.

        Returns a list of 12 integers, representing:
        [January, February, March, April, May, June,
         July, August, September, October, November, December]

        :param cursor: Database cursor.
        :return: List of minutes listened each month.
        """
        cursor.execute("""
            SELECT 
                MONTH(timestamp) AS month,
                SUM(duration) AS total_seconds
            FROM listening_data
            WHERE YEAR(timestamp) = YEAR(CURRENT_DATE())
            GROUP BY month
            ORDER BY month;
        """)

        rows = cursor.fetchall()
        months = {month: total for month, total in rows}

        result = []
        for m in range(1, 13):
            result.append(round(months.get(m, 0) / 60))

        return result
    

