"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)
        self._flag = False
        self._flag_reason = "Not currently flagged"

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    @property
    def flag(self) -> bool:
        """Marks if a video is flagged. True if flagged."""
        return self._flag

    @property
    def flag_reason(self) -> str:
        """Returns the reason a video is flagged"""
        return self._flag_reason

    def tags_string(self) -> str:
        return ' '.join(self.tags)

    def __str__(self):
        vid_info = f'{self.title} ({self.video_id}) [{self.tags_string()}]'

        return vid_info
