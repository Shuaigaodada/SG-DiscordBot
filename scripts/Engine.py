"""
1.Spotify
2.Youtube
3.QQ Music(???)
"""
import abc as _abc
import spotipy as _spotipy
from typing import Any as _Any
from typing import List as _List
from typing import Dict as _Dict

class AudioData:
    def __init__(self, url: str) -> None:
        self.url: str = url

class Spotipy:
    def __init__(self) -> None:
        # TODO: load user name and TOKEN or API key
        self.clientId: str = None
        self.clientSecret: str = None
        self.redirect_uri = "http://google.com/callback/"

        # init
        
        oauth_object = _spotipy.SpotifyOAuth(self.clientId, self.clientSecret, self.redirect_uri) 
        token_dict = oauth_object.get_access_token() 
        token = token_dict['access_token'] 
        self.spotify = _spotipy.Spotify(auth=token) 
        self.username = self.spotify.current_user() 

    def search(self, query: str, max_results: int = 5) -> _List[AudioData]:
        results: _Dict[str, _Any] = self.spotify.search(query, max_results, 0, "track")
        songs_dict = results["tracks"] 
        song_items = songs_dict['items']
        songs_list: _List[AudioData] = [] 
        for song in song_items:
            # create AudioData
            songs_list.append(
                AudioData(
                    url = song["external_urls"]["spotify"]
                )
            )
        return songs_list