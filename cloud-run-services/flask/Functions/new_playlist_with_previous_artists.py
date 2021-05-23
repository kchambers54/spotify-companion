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
def get_artist_top_track_ids_from_track(sp, artist, number_of_songs_per_artist):
    topTrackIds = [track['id'] for track in sp.artist_top_tracks(artist)['tracks']]
    return topTrackIds[0:number_of_songs_per_artist]
        

def execute(token: str, source_playlist_name: str, number_of_songs_per_artist: int = 10) -> None:

    # TODO Need to add Logging code at some point instead of print statements

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        current_user_playlists = sp.current_user_playlists(limit=50)
        found_playlist = False
        playlist_exists = False
        playlist_id = 0
        
        #Check to make sure playlist doesn't already exist, if so delete songs from it
        for playlist in current_user_playlists['items']:
            if playlist['name'] == "Top Artist Tracks from " + source_playlist_name:
                print("Top Artist Tracks Playlist has already been created, deleting and replacing")
                playlist_id = playlist['id']
                playlist_exists = True
                clear_previous_playlist(sp, playlist)
                

        #search through all user playlists and find the one with same name as the argument provided
        for playlist in current_user_playlists['items']:
            if playlist['name'] == source_playlist_name:
                found_playlist = True
                #grab correct playlist out of currentUserPlaylists
                source_playlist = sp.playlist(playlist['id'], fields="tracks,next")
                #print(sp.current_user())
                if playlist_exists == False:
                    print("creating new playlist")
                    new_playlist = sp.user_playlist_create(sp.current_user()['id'], "Top Artist Tracks from " + source_playlist_name)
                    playlist_id = new_playlist['id']
                #get the songs from the playlist into the for loop
                top_artist_list = []  # A list of artist dicts
                top_tracks_list = []  # A list of track dicts
                tracks = source_playlist['tracks']
                for track in tracks['items']:
                    #get the artist out of the track
                    if track['track']['artists'][0]['id'] in top_artist_list:
                        print("An Artist was skipped over because they were already included")
                    else:
                        top_artist_list.append(track['track']['artists'][0]['id'])
                #Go to next page of songs if more than 100, since we can only get 100 at a time
                while tracks['next'] is not None:
                    tracks = sp.next(tracks)
                    for track in tracks['items']:
                        #get the artist out of the track
                        if track['track']['artists'][0]['id'] in top_artist_list:
                            print("An Artist was skipped over because they were already included")
                        else:
                            top_artist_list.append(track['track']['artists'][0]['id'])

                for artist in top_artist_list:
                    topTracks = get_artist_top_track_ids_from_track(sp, artist, number_of_songs_per_artist)
                    top_tracks_list.extend(topTracks)
                                
                #add all songs to playlist
                i = 0
                print("Number of songs to be added to the playlist is " + str(len(top_tracks_list)))
                while i*100 < len(top_tracks_list):
                    sp.user_playlist_add_tracks(sp.current_user()['id'], playlist_id, top_tracks_list[0+(i*100) : 99+(i*100)] )
                    i= i+1

        if found_playlist == False:
            print("We were unable to find a playlist with the name specified")
            return {
                'status': 404,
                'message': 'Unable to find a playlist with the name specified'
            }

        else:
            return {
                'status': 201,
                'message': 'Playlist created',
                'artists': sp.artists(top_artist_list),
                'tracks': sp.tracks(top_tracks_list)
            }

    else:
        print("No token provided for: ", username)
        return {
            'status': 401,
            'message': 'Unauthorized, please sign in'
        }
