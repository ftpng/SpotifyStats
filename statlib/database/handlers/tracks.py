from statlib.database import Cursor, ensure_cursor, TopArtist, TopTrack


class TracksHandler:
    """
    Provides ranking data for tracks and artists.
    """


    @staticmethod
    @ensure_cursor
    def get_top_tracks(limit: int = 5, *, cursor: Cursor = None) -> list[TopTrack]:
        """
        Retrieve the most listened-to tracks of all time.

        :param limit: Number of tracks to return.
        :param cursor: Database cursor.
        :return: List of TopTrack instances.
        """
        cursor.execute(
            """
            SELECT track_name, SUM(duration)
            FROM listening_data
            GROUP BY track_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopTrack(track_name=row[0], total_seconds=row[1]) for row in rows]



    @staticmethod
    @ensure_cursor
    def get_top_artists(limit: int = 5, *, cursor: Cursor = None) -> list[TopArtist]:
        """
        Retrieve the most listened-to artists of all time.

        :param limit: Number of artists to return.
        :param cursor: Database cursor.
        :return: List of TopArtist instances.
        """
        cursor.execute(
            """
            SELECT artist_name, SUM(duration)
            FROM listening_data
            GROUP BY artist_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopArtist(artist_name=row[0], total_seconds=row[1]) for row in rows]



    @staticmethod
    @ensure_cursor
    def get_top_tracks_today(limit: int = 5, *, cursor: Cursor = None) -> list[TopTrack]:
        """
        Retrieve the most listened-to tracks for the current day.

        :param limit: Number of tracks to return.
        :param cursor: Database cursor.
        :return: List of TopTrack instances.
        """
        cursor.execute(
            """
            SELECT track_name, SUM(duration)
            FROM listening_data
            WHERE DATE(timestamp) = CURDATE()
            GROUP BY track_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopTrack(track_name=row[0], total_seconds=row[1]) for row in rows]



    @staticmethod
    @ensure_cursor
    def get_top_artists_today(limit: int = 5, *, cursor: Cursor = None) -> list[TopArtist]:
        """
        Retrieve the most listened-to artists for the current day.

        :param limit: Number of artists to return.
        :param cursor: Database cursor.
        :return: List of TopArtist instances.
        """
        cursor.execute(
            """
            SELECT artist_name, SUM(duration)
            FROM listening_data
            WHERE DATE(timestamp) = CURDATE()
            GROUP BY artist_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopArtist(artist_name=row[0], total_seconds=row[1]) for row in rows]
    

    @staticmethod
    @ensure_cursor
    def get_top_tracks_week(limit: int = 5, *, cursor: Cursor = None) -> list[TopTrack]:
        """
        Retrieve the most listened-to tracks for the current week.

        :param limit: Number of tracks to return.
        :param cursor: Database cursor.
        :return: A list of TopTrack instances representing weekly track rankings.
        """
        cursor.execute(
            """
            SELECT track_name, SUM(duration)
            FROM listening_data
            WHERE YEARWEEK(timestamp, 1) = YEARWEEK(CURDATE(), 1)
            GROUP BY track_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopTrack(track_name=row[0], total_seconds=row[1]) for row in rows]



    @staticmethod
    @ensure_cursor
    def get_top_artists_week(limit: int = 5, *, cursor: Cursor = None) -> list[TopArtist]:
        """
        Retrieve the most listened-to artists for the current week.

        :param limit: Number of artists to return.
        :param cursor: Database cursor.
        :return: A list of TopArtist instances representing weekly artist rankings.
        """
        cursor.execute(
            """
            SELECT artist_name, SUM(duration)
            FROM listening_data
            WHERE YEARWEEK(timestamp, 1) = YEARWEEK(CURDATE(), 1)
            GROUP BY artist_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopArtist(artist_name=row[0], total_seconds=row[1]) for row in rows]
    

    @staticmethod
    @ensure_cursor
    def get_top_tracks_month(limit: int = 5, *, cursor: Cursor = None) -> list[TopTrack]:
        """
        Retrieve the most listened-to tracks for the current month.

        :param limit: Number of tracks to return.
        :param cursor: Database cursor.
        :return: A list of TopTrack instances representing monthly track rankings.
        """
        cursor.execute(
            """
            SELECT track_name, SUM(duration)
            FROM listening_data
            WHERE YEAR(timestamp) = YEAR(CURDATE())
              AND MONTH(timestamp) = MONTH(CURDATE())
            GROUP BY track_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopTrack(track_name=row[0], total_seconds=row[1]) for row in rows]



    @staticmethod
    @ensure_cursor
    def get_top_artists_month(limit: int = 5, *, cursor: Cursor = None) -> list[TopArtist]:
        """
        Retrieve the most listened-to artists for the current month.

        :param limit: Number of artists to return.
        :param cursor: Database cursor.
        :return: A list of TopArtist instances representing monthly artist rankings.
        """
        cursor.execute(
            """
            SELECT artist_name, SUM(duration)
            FROM listening_data
            WHERE YEAR(timestamp) = YEAR(CURDATE())
              AND MONTH(timestamp) = MONTH(CURDATE())
            GROUP BY artist_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopArtist(artist_name=row[0], total_seconds=row[1]) for row in rows]
    

    @staticmethod
    @ensure_cursor
    def get_top_tracks_year(limit: int = 5, *, cursor: Cursor = None) -> list[TopTrack]:
        """
        Retrieve the most listened-to tracks for the current year.

        :param limit: Number of tracks to return.
        :param cursor: Database cursor.
        :return: A list of TopTrack instances representing yearly track rankings.
        """
        cursor.execute(
            """
            SELECT track_name, SUM(duration)
            FROM listening_data
            WHERE YEAR(timestamp) = YEAR(CURDATE())
            GROUP BY track_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopTrack(track_name=row[0], total_seconds=row[1]) for row in rows]



    @staticmethod
    @ensure_cursor
    def get_top_artists_year(limit: int = 5, *, cursor: Cursor = None) -> list[TopArtist]:
        """
        Retrieve the most listened-to artists for the current year.

        :param limit: Number of artists to return.
        :param cursor: Database cursor.
        :return: A list of TopArtist instances representing yearly artist rankings.
        """
        cursor.execute(
            """
            SELECT artist_name, SUM(duration)
            FROM listening_data
            WHERE YEAR(timestamp) = YEAR(CURDATE())
            GROUP BY artist_name
            ORDER BY SUM(duration) DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [TopArtist(artist_name=row[0], total_seconds=row[1]) for row in rows]


    @staticmethod
    @ensure_cursor
    def get_artist_totals(*, cursor: Cursor = None) -> list[tuple[str, int]]:
        """
        Return a list of (artist_name, total_seconds) sorted by total listening time.
        """
        cursor.execute(
            """
            SELECT artist_name, SUM(duration) AS total
            FROM listening_data
            GROUP BY artist_name
            ORDER BY total DESC
            """
        )
        return [(row[0], row[1]) for row in cursor.fetchall()]
