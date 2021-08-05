"""A video player class."""

import random
from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlist = {}
        self.current_video = ""
        self.play_state = "stopped"

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        for video in self._video_library.get_all_videos():
            if video.flag:
                print(f"{video} - FLAGGED (reason: {video.flag_reason})")
            else:
                print(video)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        try:
            video = self._video_library.get_video(video_id)
            title = video.title
        except AttributeError as error:
            print(f"Cannot play video: Video does not exist")
            return
        if video.flag:
            print(f"Cannot play video: Video is currently flagged (reason: {video.flag_reason})")
            return

        if self.play_state != "stopped":
            self.stop_video()

        self.current_video = self._video_library.get_video(video_id)
        self.play_state = "playing"
        print(f"Playing video: {self.current_video.title}")

    def stop_video(self):
        """Stops the current video."""
        if self.play_state != "stopped":
            self.play_state = "stopped"
            print(f"Stopping video: {self.current_video.title}")
            self.current_video = ""
        else:
            print(f"Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        ids = []
        for video in self._video_library.get_all_videos():
            if not video.flag:
                ids.append(video.video_id)
        if not ids:
            print("No videos available")
            return
        rand = random.randint(0, len(ids)-1)
        self.play_video(ids[rand])

    def pause_video(self):
        """Pauses the current video."""
        if self.play_state == "stopped":
            print(f"Cannot pause video: No video is currently playing")
        elif self.play_state == "paused":
            print(f"Video already paused: {self.current_video.title}")
        elif self.play_state == "playing":
            print(f"Pausing video: {self.current_video.title}")
            self.play_state = "paused"

    def continue_video(self):
        """Resumes playing the current video."""
        if self.play_state == "stopped":
            print(f"Cannot continue video: No video is currently playing")
        elif self.play_state == "paused":
            print(f"Continuing video: {self.current_video.title}")
            self.play_state = "playing"
        elif self.play_state == "playing":
            print(f"Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self.play_state == "playing":
            print(f"Currently playing: {self.current_video}")
        elif self.play_state == "paused":
            print(f"Currently playing: {self.current_video} - PAUSED")
        elif self.play_state == "stopped":
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lowercase_name = playlist_name.lower()
        if lowercase_name in self._playlist:
            print("Cannot create playlist: A playlist with the same name already exists")
            return

        self._playlist[lowercase_name] = Playlist(playlist_name)
        print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        #This checks the called playlist exists
        playlist = self._playlist.get(playlist_name.lower(), None)
        if playlist is None:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            return
        #This checks the mentioned video exists
        try:
            video = self._video_library.get_video(video_id)
            title = video.title
        except AttributeError:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return

        video = self._video_library.get_video(video_id)
        if video in playlist.playlist_videos:
            print(f"Cannot add video to {playlist_name}: Video already added")
            return

        if video.flag:
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flag_reason})")
            return
        playlist.playlist_videos.append(video)
        print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""

        if not self._playlist:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            playlists_sorted = sorted(self._playlist.values(), key=lambda p: p.playlist_name)

            for playlist in playlists_sorted:
                print(f"{playlist}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlist.get(playlist_name.lower(), None)
        if playlist is None:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return
        print(f"Showing playlist: {playlist_name}")
        if not playlist.playlist_videos:
            print("No videos here yet")
            return
        for video in playlist.playlist_videos:
            if video.flag:
                print(f"{video} - FLAGGED (reason: {video.flag_reason})")
            else:
                print(video)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self._playlist.get(playlist_name.lower(), None)
        if playlist is None:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return

        video = self._video_library.get_video(video_id)
        if not video:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return
        for v in playlist.playlist_videos:
            if video == v:
                playlist.playlist_videos.remove(video)
                print(f"Removed video from {playlist_name}: {video.title}")
                return
        print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlist.get(playlist_name.lower(), None)
        if playlist is None:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return
        print(f"Successfully removed all videos from {playlist_name}")
        playlist.playlist_videos = []

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlist.get(playlist_name.lower(), None)
        if playlist is None:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return
        playlist.playlist_videos = []
        self._playlist.pop(playlist_name.lower())
        print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        results = []
        for video in self._video_library.get_all_videos():
            if search_term.lower() in video.title.lower():
                if not video.flag:
                    results.append(video)
        self.display_search(results, search_term)

    def display_search(self, results, search_term):
        """Displays the search results from both video searches and tag searches

        Args:
            results: a list of the search results
            search_term: the term used for a search
        """

        if not results:
            print(f"No search results for {search_term}")
            return
        results = sorted(results, key=lambda x: x.title)

        print(f"Here are the results for {search_term}:")
        video_num = 1
        for v in results:
            print(f"{video_num}) {v}")
            video_num += 1

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")

        num = input()
        try:
            num = int(num)
        except ValueError:
            return

        if num <= 0:
            return
        try:
            chosen_vid = results[num-1]
        except IndexError:
            return
        self.play_video(chosen_vid.video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        results = []
        for video in self._video_library.get_all_videos():
            for tag in video.tags:
                if video_tag.lower() == tag.lower():
                    if not video.flag:
                        results.append(video)
        self.display_search(results, video_tag)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if not flag_reason:
            flag_reason = "Not supplied"

        video = self._video_library.get_video(video_id)
        if not video:
            print(f"Cannot flag video: Video does not exist")
            return
        if video.flag:
            print(f"Cannot flag video: Video is already flagged")
            return

        if video == self.current_video:
            self.stop_video()
        video._flag = True
        video._flag_reason = flag_reason
        print(f"Successfully flagged video: {video.title} (reason: {video.flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if not video:
            print(f"Cannot remove flag from video: Video does not exist")
            return
        if not video.flag:
            print(f"Cannot remove flag from video: Video is not flagged")
            return

        video._flag = False
        video._flag_reason = "Not currently flagged"
        print(f"Successfully removed flag from video: {video.title}")
