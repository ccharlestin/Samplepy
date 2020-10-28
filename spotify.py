import os
import requests
import spotipy
import spotipy.util as util
import configparser
from spotipy.oauth2 import SpotifyOAuth



def printUserStats(spotipyObj):
    userInfo = spotipyObj.me() # Get's basic user info
    print('')
    print(userInfo)
    

def printAllLikedSongs(spotipyObj):
    # https://developer.spotify.com/documentation/web-api/reference/library/get-users-saved-tracks/ (Look at "next" key. It may help)
    offset = 0 # Each offset indicates the next set of songs 
    limit = 50 # Max number of songs that can be in dictionary (result) at once 0-49
    count = 0
    results = spotipyObj.current_user_saved_tracks(limit, offset)
    while offset <= results['total']:
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

def getSongURI(headers):
    title = input('Input title: ')
    artist = input('Input artist: ')
    #To get auth_header go here: https://github.com/plamere/spotipy/blob/master/spotipy/client.py
    BASE_URL = 'https://api.spotify.com/v1/'
    r = requests.get(BASE_URL + 'search?q={} {}&type=track&limit=1'.format(title, artist), headers=headers)
    print(r.json()['tracks']['items'][0]['uri'])


def createPlaylist(spotipyObj):
    playlist_name = input('What is name of the new playlist: ')
    userInfo = spotipyObj.me()
    caller_name =  userInfo['display_name']
    spotipyObj.user_playlist_create(caller_name, playlist_name)

def addToPlaylist(headers, spotipyObj):
    playlist_name = input('What is the name of the playlist you are adding to: ')
    BASE_URL = 'https://api.spotify.com/v1/'
    r = requests.get(BASE_URL + 'search?q={}&type=playlist&limit=1'.format(playlist_name), headers=headers)
    playlist_owner = r.json()['playlists']['items'][0]['owner']['display_name']
    userInfo = spotipyObj.me()
    caller_name =  userInfo['display_name']
    if playlist_owner == caller_name:
        print('You own this playlist, but I didn\'t create the functionality yet')
        #tracks = ['spotify:track:4wQFB68968Q08qP3iy5DMW', 'spotify:track:6IwKcFdiRQZOWeYNhUiWIv', 'spotify:track:07G9Dbpg14PlUFstgf32id', 'spotify:track:07G9Dbpg14PlUFstgf32id']
        #spotipyUser.user_playlist_add_tracks('ccharlestin', 'spotify:playlist:2aJDqNNgTqiEUlTjq8R9Mj', tracks)
    else:
        print('You can only motify playlists that you own')
    


def userAuthentication():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        username = config['SPOTIFY']['USERNAME']
        client_id = config['SPOTIFY']['CLIENT_ID']
        client_secret = config['SPOTIFY']['CLIENT_SECRET']
        redirect_uri = config['SPOTIFY']['REDIRECT_URI']
        scope = config['SPOTIFY']['SCOPE']
    except:
        print('Please create the config file \"config.ini\" and give it the following format:')
        print('[SPOTIFY]')
        print('USERNAME =')
        print('CLIENT_ID =')
        print('CLIENT_SECRET =')
        print('REDIRECT_URI =')
        print('SCOPE =')
        
    
    # https://github.com/plamere/spotipy/issues/194 (Blessed Post)
    token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        show_dialog=True,
        )
    #https://stackoverflow.com/questions/48883731/refresh-token-spotipy/48887478 (Also useful)
    spotipyUser = spotipy.Spotify(auth=token)
    return spotipyUser


def menu():
      print('\n')
      print('What do you want to do')
      print('0. Quit Program')
      print('1. View user information')
      print('2. View like songs')
      print('3. View track information')
      print('4. View playlist information')
      print('5. Get Song URI')
      print('6. Create Playlist')
      print('7. Add song(s) to playlist') #Needs work (Functionality needed)
      

# https://stmorse.github.io/journal/spotify-api.html (For access token help)
# https://github.com/rach-sharp/spotipy/commit/b051e2a164815dd5c966382d5f1b0ce05fafd36a (Use later)
def main():
    spotipyUser = userAuthentication()
 
    while True:
        menu()
        choice = input('Input here: ')
        if choice == '1':
            printUserStats(spotipyUser)
        elif choice == '2':
            printAllLikedSongs(spotipyUser)
        elif choice == '3':
            viewTrackInfo(spotipyUser)
        elif choice == '4':
            viewPlaylistInfo(spotipyUser)
        elif choice == '5':
            getSongURI(spotipyUser._auth_headers())
        elif choice == '6':
            createPlaylist(spotipyUser)
        elif choice == '7':
            addToPlaylist(spotipyUser._auth_headers(), spotipyUser)     
        elif choice == '0':
            exit()


if __name__ == "__main__":
    main()