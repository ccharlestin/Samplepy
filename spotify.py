import os
import sys 
import json
import spotipy
import webbrowser
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from json.decoder import JSONDecodeError
import configparser


def printUserStats(spotipyObj):
    userInfo = spotipyObj.me() # Get's basic user info
    print('')
    print(userInfo)
    


def printAllLikedSongs(spotipyObj):
    offset = 0 # Each offset indicates the next set of songs 
    limit = 50 # Max number of songs that can be in dictionary (result) at once 0-49
    count = 0
    results = spotipyObj.current_user_saved_tracks(limit, offset)
    while offset != 10000: # 10000 is max number of songs a playlist can contain (Not efficient, find better way to end while loop)
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(count, track['artists'][0]['name'], " – ", track['name'])
            count += 1
        offset += 50
        results = spotipyObj.current_user_saved_tracks(limit, offset)


def viewTrackInfo(spotipyObj):
    track_id = input("Please input the song ID (Copy Spotify URI): ")
    try:
        if 'spotify:track:' in track_id: #Removes the spotify:track prefix whe coppying the Spotify URI
            track_id.replace('spotify:track:','')
        track = spotipyObj.track(track_id)
        print(track)
    except:
        print('Invalid Playlist ID')

def viewPlaylistInfo(spotipyObj):
    playlist_id = input("Please input the playlist ID (Copy Spotify URI): ")
    try:
        if 'spotify:playlist:' in playlist_id: #Removes the spotify:track prefix whe coppying the Spotify URI
            playlist_id.replace('spotify:playlist:','')
        playlist = spotipyObj.playlist_items(playlist_id)
        print(playlist)
    except:
        print('Invalid Playlist ID')


def addSongToPlaylist(spotipyObj):
    playlist_id = input("Please input the playlist ID (Copy Spotify URI): ")
    track_id = input("Please input the song ID (Copy Spotify URI): ")
   
    try:
        if 'spotify:track:' in track_id: 
            track_id.replace('spotify:track:','')
        if 'spotify:playlist:' in playlist_id: #Removes the spotify:track prefix whe coppying the Spotify URI
            playlist_id.replace('spotify:playlist:','')  
        arr = [track_id]
        spotipyObj.playlist_add_items(playlist_id, arr)
        print('Song added to playlist')
    except:
        print('Invalid Playlist or Track ID')
# spotify:playlist:0EL9UjBOx1DS369cmNl5Yl
# spotify:track:5HiSc2ZCGn8L3cH3qSwzBT
def menu():
      print('\n')
      print('What do you want to do')
      print('0. Quit Program')
      print('1. View user information')
      print('2. View like songs')
      print('3. View track information')
      print('4. View playlist information')
      print('5. Add song to playlist')
      

def main():
    client_id = 'd49574f411a24787a536c2e0b58a06ab'
    client_secret = '471996793fa841e695d07bf052305f5c' # Work on putting this in config file later (Config parser?)
    redirect_uri = 'https://www.google.com'
    scope = "user-library-read playlist-modify-public playlist-modify-private" # Look into more scopes later
    spotipyObj = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    
    loop = True
    while loop:
        menu()
        choice = input('Input here: ')
        if choice == '1':
            printUserStats(spotipyObj)
        elif choice == '2':
            printAllLikedSongs(spotipyObj)
        elif choice == '3':
            viewTrackInfo(spotipyObj)
        elif choice == '4':
            viewPlaylistInfo(spotipyObj)
        elif choice == '5':
            addSongToPlaylist(spotipyObj)
        elif choice == '0':
            loop = False


if __name__ == "__main__":
    main()