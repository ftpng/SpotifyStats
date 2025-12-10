from dataclasses import dataclass
from datetime import datetime


@dataclass
class ListeningEntry:
    """
    Represents a single recorded listening entry.

    :param id: Unique identifier of the listening entry.
    :param timestamp: Timestamp when the entry was recorded.
    :param track_name: Name of the track being listened to.
    :param artist_name: Name of the artist associated with the track.
    :param duration: Duration listened during this entry, in seconds.
    """
    id: int
    timestamp: datetime
    track_name: str
    artist_name: str
    duration: int



@dataclass
class TimeSummary:
    """
    Represents a summary of total listening time.

    :param total_seconds: Total number of seconds listened in the measured period.
    """
    total_seconds: int



@dataclass
class TopArtist:
    """
    Represents an artist ranked by total listening time.

    :param artist_name: Name of the artist.
    :param total_seconds: Total seconds listened to this artist.
    """
    artist_name: str
    total_seconds: int



@dataclass
class TopTrack:
    """
    Represents a track ranked by total listening time.

    :param track_name: Name of the track.
    :param total_seconds: Total seconds listened to this track.
    """
    track_name: str
    total_seconds: int