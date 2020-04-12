import sys
import spotipy
import spotipy.util as util

# clears out the songs from a prior version of our playlist
def clear_previous_playlist(sp, playlist):
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

#takes a song provided, and goes and pulls the first artist credited out
def get_artist_top_track_ids_from_track(sp, artist, numOfSongsPerArtist):
    topTrackIds = [track['id'] for track in sp.artist_top_tracks(artist)['tracks']]
    return topTrackIds[0:numOfSongsPerArtist]
        



def main():

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
        PlaylistID = 0
        
        #Check to make sure playlist doesn't already exist, if so delete songs from it
        for playlist in currentUserPlaylists['items']:
            if playlist['name'] == "Top Artist Tracks from " + sourcePlaylistString:
                print("Top Artist Tracks Playlist has already been created, deleting and replacing")
                PlaylistID = playlist['id']
                playlistExists = True
                clear_previous_playlist(sp, playlist)
                

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
                    PlaylistID = newPlaylist['id']
                #get the songs from the playlist into the for loop
                topArtistList = []  # A list of artist dicts
                topTracksList = []  # A list of track dicts
                tracks = sourcePlaylist['tracks']
                for track in tracks['items']:
                    #get the artist out of the track
                    if track['track']['artists'][0]['id'] in topArtistList:
                        print("An Artist was skipped over because they were already included")
                    else:
                        topArtistList.append(track['track']['artists'][0]['id'])
                #Go to next page of songs if more than 100, since we can only get 100 at a time
                while tracks['next'] is not None:
                    tracks = sp.next(tracks)
                    for track in tracks['items']:
                        #get the artist out of the track
                        if track['track']['artists'][0]['id'] in topArtistList:
                            print("An Artist was skipped over because they were already included")
                        else:
                            topArtistList.append(track['track']['artists'][0]['id'])

                for artist in topArtistList:
                    topTracks = get_artist_top_track_ids_from_track(sp, artist, numOfSongsPerArtist)
                    topTracksList.extend(topTracks)
                                
                #add all songs to playlist
                i = 0
                print("Number of songs to be added to the playlist is " + str(len(topTracksList)))
                while i*100 < len(topTracksList):
                    sp.user_playlist_add_tracks(sp.current_user()['id'], PlaylistID, topTracksList[0+(i*100) : 99+(i*100)] )
                    i= i+1

        if foundPlaylist == False:
            print("We were unable to find a playlist with the name specified")
    else:
        print("Can't get token for", username)

if __name__ == "__main__":
    main()