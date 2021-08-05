"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name: str):
        self.playlist_name = playlist_name
        self.playlist_videos = []

    def __str__(self):
        return self.playlist_name
