import sys
import spotipy
import spotipy.util as util

def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(
            "   %d %32.32s %s" %
            (i, track['artists'][0]['name'], track['name']))

def get_artist_top_tracks_from_track(track):
    artist = track['track']['artists'][0]['id']
    topTracks = sp.artist_top_tracks(artist)
    return topTracks;
        


scope = 'playlist-modify-public playlist-read-private'

if len(sys.argv) > 2:
    username = sys.argv[1]
    sourcePlaylist = sys.argv[2]
else:
    print("Usage: %s username sourcePlaylist" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.current_user_playlists(limit=50)
    for i, item in enumerate(results['items']):
        if item['name'] == sourcePlaylist:
            playlist = sp.playlist(item['id'], fields="tracks,next")
            #print(sp.current_user())
            newPlaylist = sp.user_playlist_create(sp.current_user()['id'], "Top Artist Tracks from " + sourcePlaylist)
            for track in playlist['tracks']['items']:
                print(track['track']['artists'][0]['id'])
                topTracks = get_artist_top_tracks_from_track(track);
                topTracksList = []
                for artistTrack in topTracks['tracks']:
                    print(artistTrack)
                    topTracksList.append(artistTrack['id'])

                sp.user_playlist_add_tracks(sp.current_user()['id'], newPlaylist['id'], topTracksList)

else:
    print("Can't get token for", username)
