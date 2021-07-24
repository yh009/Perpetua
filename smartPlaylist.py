import json
import random
from myOwnMusixmatch import myOwnMusixmatch
from musixmatch import Musixmatch

trackQueue = []
played = []
apiKey1 = '12832752fc79e94b205e24b1a5bf7a4d'


musixmatch = Musixmatch(apiKey1)
mymusixmatch = myOwnMusixmatch(apiKey1)

# This is the main interface for the API, where user input:
#   1. cateogry text
# Assumption: at the beginning, find any track contain category text in their lyrics
def init(categoryText):
    fetchTrackAPICall(categoryText)
    fetchTrackAPICall(categoryText)

# get a new track given the played track
def fetchTrack(trackObj):
    # if no lyrics, just stop fetching
    if trackObj['lyrics'] == None:
        return done()
    #find 5 random words from track
    tmpWords = getRandomWords(trackObj['lyrics'])

    #track_search, check if already played. Otherwise append queue and return in JSON
    fetchTrackAPICall(tmpWords)

# conduct API call to get track, given 5 keywords
def fetchTrackAPICall(lyrics):
    res = {}
    # return 10 tracks in case some already played
    tracks = mymusixmatch.track_search(q_lyrics = lyrics, page_size=10, page=1, s_track_rating='desc')
    for track in tracks['message']['body']['track_list']:
        tmpId = track['track']['track_id']
        tmpTrackName = track['track']['track_name']
        tmpArtistName = track['track']['artist_name']
        if tmpId in played:
            continue 
        else:
            res['track_id'] = tmpId
            # append the track_id to played list 
            played.append(tmpId)
            tmpLyrics = getLyrics(int(tmpId))
            res['lyrics'] = tmpLyrics
            res['track_name'] = tmpTrackName
            res['artist_name'] = tmpArtistName
            trackQueue.append(res)
            return



# Always finish the first one in queue
def trackFinished():
    if len(trackQueue) != 0:
        # Pop the head of the queue
        tmpTrack = trackQueue.pop(0)
        # Fetch the next track
        fetchTrack(tmpTrack)
    else:
        done()


def done():
    print("we are done")
    return


# Get the lyrics given trackId
def getLyrics(trackId):
    lyrics = musixmatch.track_lyrics_get(track_id = trackId)
    return lyrics['message']["body"]['lyrics']["lyrics_body"]
                            

# return 5 random words from the track  
def getRandomWords(lyrics):
    myList = set(lyrics.split())
    n = len(myList)
    res = []
    for i in range(5):
        while True:
            myRan = random.randint(0,n)
            tmpWord = lyrics[myRan]
            if (tmpWord not in res) and (tmpWord.isalpha()): # avoid repetition and non alpha words
                res.append(tmpWord)
                break
    return " ".join(res)


##################### Test #######################
#print(getLyrics(125424336))
init("Pots and Pans")
#print(trackQueue)
print(played)

trackFinished()
#print(trackQueue)
print(played)

trackFinished()
#print(trackQueue)
print(played)

print(len(trackQueue))