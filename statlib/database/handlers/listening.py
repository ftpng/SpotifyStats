from statlib.database import Cursor, ensure_cursor, ListeningEntry


class ListeningHandler:
    """
    Handles raw listening entry inserts and retrieval.
    """

    @staticmethod
    @ensure_cursor
    def insert_entry(
        track_name: str,
        artist_name: str,
        duration: int,
        *,
        cursor: Cursor = None
    ) -> None:
        """
        Insert or merge a listening entry.

        Uses NOW(6) for microsecond precision and merges entries that collide
        with the UNIQUE KEY using ON DUPLICATE KEY UPDATE.

        :param track_name: Name of the track.
        :param artist_name: Name of the artist.
        :param duration: Duration listened in seconds.
        :param cursor: Database cursor.
        """
        cursor.execute(
            """
            INSERT INTO listening_data (timestamp, track_name, artist_name, duration)
            VALUES (NOW(6), %s, %s, %s)
            ON DUPLICATE KEY UPDATE duration = duration + VALUES(duration)
            """,
            (track_name, artist_name, duration)
        )

    @staticmethod
    @ensure_cursor
    def get_latest_entry(*, cursor: Cursor = None) -> ListeningEntry | None:
        """
        Retrieve the most recent listening entry.

        :param cursor: Database cursor.
        :return: ListeningEntry instance or None.
        """
        cursor.execute(
            "SELECT * FROM listening_data ORDER BY id DESC LIMIT 1"
        )
        row = cursor.fetchone()

        if not row:
            return None

        return ListeningEntry(
            id=row[0],
            timestamp=row[1],
            track_name=row[2],
            artist_name=row[3],
            duration=row[4]
        )
