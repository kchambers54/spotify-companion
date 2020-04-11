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
def get_artist_top_track_ids_from_track(artist, numOfSongsPerArtist):
    topTrackIds = [track['id'] for track in sp.artist_top_tracks(artist)['tracks']]
    print(topTrackIds)
    return topTrackIds[0:numOfSongsPerArtist]
        

#Need to add Logging code at some point instead of print statements
scope = 'playlist-modify-public playlist-read-private'

if len(sys.argv) > 2:
    username = sys.argv[1]
    sourcePlaylistString = sys.argv[2]
    if len(sys.argv) > 3:
        try:
            numOfSongsPerArtist = int(sys.argv[3])
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
    currentUserPlaylists = sp.current_user_playlists(limit=50)
    foundPlaylist = False
    playlistExists = False
    oldPlaylistID = 0
    
    #Check to make sure playlist doesn't already exist, if so delete songs from it
    for playlist in currentUserPlaylists['items']:
        if playlist['name'] == "Top Artist Tracks from " + sourcePlaylistString:
            print("Top Artist Tracks Playlist has already been created, deleting and replacing")
            oldPlaylistID = playlist['id']
            playlistExists = True
            tracksToDelete = []
            oldPlaylist = sp.playlist(playlist['id'], fields="tracks,next")
            tracks = oldPlaylist['tracks']
            #print(oldPlaylist['tracks']['items'])
            for track in tracks['items']:
                tracksToDelete.append(track['track']['id'])
                
            while tracks['next'] is not None:
                tracks = sp.next(tracks)
                #print(oldPlaylist['tracks']['items'])
                for track in tracks['items']:
                    tracksToDelete.append(track['track']['id'])

            i = 0
            print("number of tracks to delete is " + str(len(tracksToDelete)))
            while i*100 < len(tracksToDelete):
                sp.user_playlist_remove_all_occurrences_of_tracks(sp.current_user()['id'], playlist['id'], tracksToDelete[0+(i*100) : 99+(i*100)] )
                i= i+1

    #search through all user playlists and find the one with same name as the argument provided
    for playlist in currentUserPlaylists['items']:
        if playlist['name'] == sourcePlaylistString:
            foundPlaylist = True
            #grab correct playlist out of currentUserPlaylists
            sourcePlaylist = sp.playlist(playlist['id'], fields="tracks,next")
            #print(sp.current_user())
            if playlistExists == False:
                print("creating new playlist")
                newPlaylist = sp.user_playlist_create(sp.current_user()['id'], "Top Artist Tracks from " + sourcePlaylistString)
            #get the songs from the playlist into the for loop
            topArtistList = []  # A list of artist dicts
            topTracksList = []  # A list of track dicts
            for track in sourcePlaylist['tracks']['items']:
                #get the artist out of the track
                if track['track']['artists'][0]['id'] in topArtistList:
                    print("Artist already included")
                else:
                    topArtistList.append(track['track']['artists'][0]['id'])

            for artist in topArtistList:

                topTracks = get_artist_top_track_ids_from_track(artist, numOfSongsPerArtist)
                topTracksList.extend(topTracks)
                
                #grab each track from the top tracks of a specific artist
                # for i, artistTrack in enumerate(topTracks['tracks']):
                #     #print(artistTrack)
                #     #put into list that will be all added to a playlist at once
                #     if(i < int(numOfSongsPerArtist)):
                #         topTracksList.append(artistTrack['id'])
                            
            #add all songs to playlist
            i = 0
            print("length of top tracks list is " + str(len(topTracksList)))
            while i*100 < len(topTracksList):
                if playlistExists == True:
                    sp.user_playlist_add_tracks(sp.current_user()['id'], oldPlaylistID, topTracksList[0+(i*100) : 99+(i*100)] )
                else:
                    sp.user_playlist_add_tracks(sp.current_user()['id'], newPlaylist['id'], topTracksList[0+(i*100) : 99+(i*100)] )
                i= i+1
    if foundPlaylist == False:
        print("We were unable to find a playlist with the name specified")

else:
    print("Can't get token for", username)
