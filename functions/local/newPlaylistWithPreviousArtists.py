import sys
import spotipy
import spotipy.util as util

def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(
            "   %d %32.32s %s" %
            (i, track['artists'][0]['name'], track['name']))

#takes a song provided, and goes and pulls the first artist credited out
def get_artist_top_tracks_from_track(track):
    artist = track['track']['artists'][0]['id']
    topTracks = sp.artist_top_tracks(artist)
    return topTracks
        

#Need to add Logging code at some point instead of print statements
scope = 'playlist-modify-public playlist-read-private'

if len(sys.argv) > 2:
    username = sys.argv[1]
    sourcePlaylist = sys.argv[2]
    if len(sys.argv) > 3:
        try:
            int(sys.argv[3])
            numOfSongsPerArtist = sys.argv[3]
        except:
            print("%s is not a valid number between 0 and 10, defaulting to 10", sys.argv[3])
            numOfSongsPerArtist = 10
        
else:
    print("Usage: %s username sourcePlaylist numOfSongsPerArtist(max 10)" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.current_user_playlists(limit=50)
    foundPlaylist = False
    playlistExists = False
    oldPlaylistID = 0
    
    #Check to make sure playlist doesn't already exist, if so delete songs from it
    for i, item in enumerate(results['items']):
        if item['name'] == "Top Artist Tracks from " + sourcePlaylist:
            print("Top Artist Tracks Playlist has already been created, deleting and replacing")
            oldPlaylistID = item['id']
            playlistExists = True
            oldPlaylist = sp.playlist(item['id'], fields="tracks,next")
            #print(oldPlaylist['tracks']['items'])
            tracksToDelete = []
            for track in oldPlaylist['tracks']['items']:
                tracksToDelete.append(track['track']['id'])
            sp.user_playlist_remove_all_occurrences_of_tracks(sp.current_user()['id'], item['id'], tracksToDelete)
    #search through all user playlists and find the one with same name as the argument provided
    for i, item in enumerate(results['items']):
        if item['name'] == sourcePlaylist:
            foundPlaylist = True
            #grab correct playlist out of results
            playlist = sp.playlist(item['id'], fields="tracks,next")
            #print(sp.current_user())
            if playlistExists == False:
                print("creating new playlist")
                newPlaylist = sp.user_playlist_create(sp.current_user()['id'], "Top Artist Tracks from " + sourcePlaylist)
            #get the songs from the playlist into the for loop
            topTracksList = []
            for track in playlist['tracks']['items']:
                #print(track['track']['artists'][0]['id'])
                topTracks = get_artist_top_tracks_from_track(track);
                #grab each track from the top tracks of a specific artist
                for i, artistTrack in enumerate(topTracks['tracks']):
                    #print(artistTrack)
                    #put into list that will be all added to a playlist at once
                    if(i < int(numOfSongsPerArtist)):
                        if artistTrack['id'] in topTracksList:
                            print("song already in list, not including")
                        else:
                            topTracksList.append(artistTrack['id'])
            #add all songs to playlist
            if playlistExists == True:
                sp.user_playlist_add_tracks(sp.current_user()['id'], oldPlaylistID, topTracksList)
            else:
                sp.user_playlist_add_tracks(sp.current_user()['id'], newPlaylist['id'], topTracksList)
    if foundPlaylist == False:
        print("We were unable to find a playlist with the name specified")

else:
    print("Can't get token for", username)
