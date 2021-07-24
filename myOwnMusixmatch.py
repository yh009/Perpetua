import json

import requests

# borrowed from https://github.com/hudsonbrendon/python-musixmatch/blob/master/musixmatch/musixmatch.py
# with modification done to track_search()
class myOwnMusixmatch(object):
    def __init__(self, apikey):
        """Define objects of type Musixmatch.
        Parameters:
        apikey - For get your apikey access: https://developer.musixmatch.com
        """
        self.__apikey = apikey
        self.__url = "http://api.musixmatch.com/ws/1.1/"

    def _get_url(self, url):
        return f"{self.__url}{url}&apikey={self.__apikey}"

    @property
    def _apikey(self):
        return self.__apikey

    def _request(self, url):
        request = requests.get(url)
        return request.json()

    def _set_page_size(self, page_size):
        if page_size > 100:
            page_size = 100
        elif page_size < 1:
            page_size = 1
        return page_size

    def track_search(
        self, q_lyrics, page_size, page, s_track_rating, f_has_lyrics = True, _format="json"
    ):
        """Search for track in our database.
        Parameters:
        q_track - The song title.
        q_artist - The song artist.
        q_lyrics - Any word in the lyrics.
        f_artist_id - When set, filter by this artist id.
        f_music_genre_id - When set, filter by this music category id.
        f_lyrics_language - Filter by the lyrics language (en,it,..).
        f_has_lyrics - When set, filter only contents with lyrics.
        f_track_release_group_first_release_date_min - When set, filter
        the tracks with release date newer than value, format is YYYYMMDD.
        f_track_release_group_first_release_date_max - When set, filter
        the tracks with release date older than value, format is YYYYMMDD.
        s_artist_rating - Sort by our popularity index for artists (asc|desc).
        s_track_rating - Sort by our popularity index for tracks (asc|desc).
        quorum_factor - Search only a part of the given query string.
        Allowed range is (0.1 – 0.9).
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results.
        Range is 1 to 100.
        callback - jsonp callback.
        format - Decide the output type json or xml (default json).
        Note: This method requires a commercial plan.
        """
        data = self._request(
            self._get_url(
                "track.search?"
                "q_lyrics={}&f_has_lyrics={}"
                "&page_size={}"
                "&page={}"
                "&s_track_rating={}&format={}".format(
                    q_lyrics,
                    f_has_lyrics,
                    page_size,
                    page,
                    s_track_rating,
                    _format,
                )
            )
        )
        return data
