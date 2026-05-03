import webbrowser
import urllib.parse

def play_song(song_name):
    query = urllib.parse.quote(song_name)
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)