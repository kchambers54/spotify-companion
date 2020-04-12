import sys
import spotipy
import spotipy.util as util

def main():

    #Need to add Logging code at some point instead of print statements
    scope = 'playlist-modify-public playlist-read-private'
    if len(sys.argv) > 2:
        username = sys.argv[1]
        sourcePlaylistString = sys.argv[2]
            
    else:
        print("Usage: %s username sourcePlaylist" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        currentUserPlaylists = sp.current_user_playlists(limit=50)
        foundPlaylist = False
        totalPopularity = 0
        totalSongsTracked = 0

        #search through all user playlists and find the one with same name as the argument provided
        for playlist in currentUserPlaylists['items']:
            if playlist['name'] == sourcePlaylistString:
                foundPlaylist = True
                #grab correct playlist out of currentUserPlaylists
                sourcePlaylist = sp.playlist(playlist['id'], fields="tracks,next")
                #get the songs from the playlist into the for loop
                tracks = sourcePlaylist['tracks']
                for track in tracks['items']:
                    #get the popularity
                    print(track['track']['popularity'])
                    totalPopularity = totalPopularity + track['track']['popularity']
                    totalSongsTracked = totalSongsTracked + 1

                #Go to next page of songs if more than 100, since we can only get 100 at a time
                while tracks['next'] is not None:
                    tracks = sp.next(tracks)
                    #get the popularity
                    print(track['track']['popularity'])
                    totalPopularity = totalPopularity + track['track']['popularity']
                    totalSongsTracked = totalSongsTracked + 1
                                
                #Print the average popularity
                print("Total Popularity: " + str(totalPopularity))
                print("Total Songs Analyzed: " + str(totalSongsTracked))
                print("Popularity Score: " + str(int(totalPopularity) / int(totalSongsTracked)))

        if foundPlaylist == False:
            print("We were unable to find a playlist with the name specified")
    else:
        print("Can't get token for", username)

if __name__ == "__main__":
    main()