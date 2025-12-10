from statlib.database import Cursor, ensure_cursor, TimeSummary, TopArtist, TopTrack


class OverviewHandler:
    """
    Provides data for the /overview command:
    yearly time, top artists, top tracks, and now playing.
    """


    @staticmethod
    @ensure_cursor
    def get_year_total(year: int, *, cursor: Cursor = None) -> TimeSummary:
        """
        Retrieve total listening time for a given year.

        :param year: Year to calculate totals for.
        :param cursor: Database cursor.
        :return: TimeSummary containing total seconds.
        """
        cursor.execute(
            """
            SELECT COALESCE(SUM(duration), 0)
            FROM listening_data
            WHERE YEAR(timestamp) = %s
            """,
            (year,)
        )
        (total,) = cursor.fetchone()
        return TimeSummary(total_seconds=total)



    @staticmethod
    @ensure_cursor
    def get_top_tracks(limit: int = 5, *, cursor: Cursor = None) -> list[TopTrack]:
        """
        Retrieve the top listened tracks of the entire database.

        :param limit: Number of tracks to return.
        :param cursor: Database cursor.
        :return: List of TopTrack.
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
        Retrieve the top listened artists of the entire database.

        :param limit: Number of artists to return.
        :param cursor: Database cursor.
        :return: List of TopArtist.
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