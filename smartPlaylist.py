import json
import random
import collections
from nltk.corpus import stopwords
from myOwnMusixmatch import myOwnMusixmatch
from musixmatch import Musixmatch


class SmartPlaylist():

    # Assumption: at the beginning, find any track contain category text in their lyrics
    def __init__(self, categoryText, apiKey):
        self.trackQueue = []
        self.played = []
        self.musixmatch = Musixmatch(apiKey)
        self.mymusixmatch = myOwnMusixmatch(apiKey)
        self.fetchTrackAPICall(categoryText)
        self.fetchTrackAPICall(categoryText)
        self.stopWords = set(stopwords.words("english"))
        
    #apiKey1 = '12832752fc79e94b205e24b1a5bf7a4d'


    # getter for current queue
    def getTrackQueue(self):
        return self.trackQueue

    def getPlayed(self):
        return self.played

    # get a new track given the played track
    def fetchTrack(self, trackObj):
        # if no lyrics, just stop fetching
        if trackObj['lyrics'] == None:
            return done()
        #find 5 random words from track
        tmpWords = self.getMostFreqWords(trackObj['lyrics'])
        #tmpWords = self.getRandomWords(trackObj['lyrics'])

        #track_search, check if already played. Otherwise append queue and return in JSON
        return self.fetchTrackAPICall(tmpWords)

    # conduct API call to get track, given 5 keywords
    def fetchTrackAPICall(self, lyrics):
        res = {}
        # return 10 tracks in case some already played
        tracks = self.mymusixmatch.track_search(q_lyrics = lyrics, page_size=10, page=1, s_track_rating='desc')
        for track in tracks['message']['body']['track_list']:
            tmpId = track['track']['track_id']
            tmpTrackName = track['track']['track_name']
            tmpArtistName = track['track']['artist_name']
            if tmpId in self.played:
                continue 
            else:
                res['track_id'] = tmpId
                # append the track_id to played list 
                self.played.append(tmpId)
                tmpLyrics = self.getLyrics(int(tmpId))
                res['lyrics'] = tmpLyrics
                res['track_name'] = tmpTrackName
                res['artist_name'] = tmpArtistName
                self.trackQueue.append(res)
                return res



    # Always finish the first one in queue
    def trackFinished(self):
        if len(self.trackQueue) != 0:
            # Pop the head of the queue
            tmpTrack = self.trackQueue.pop(0)
            # Fetch the next track
            return self.fetchTrack(tmpTrack)
        else:
            return self.done()


    def done(self):
        print("we are done")
        return "Done!"


    # Get the lyrics given trackId
    def getLyrics(self, trackId):
        lyrics = self.musixmatch.track_lyrics_get(track_id = trackId)
        return lyrics['message']["body"]['lyrics']["lyrics_body"]
                                

    # return 5 random words from the track  
    def getRandomWords(self, lyrics):
        myList = set(lyrics.split())
        n = len(myList)
        res = []
        for i in range(5):
            while True:
                myRan = random.randint(0,n)
                tmpWord = lyrics[myRan].lower()
                if (tmpWord not in res) and (tmpWord.isalpha()): # avoid repetition and non alpha words
                    res.append(tmpWord)
                    break
        return " ".join(res)

    # Bonus 1: instead of getting random words, get the top 5 words that appear most frequently, remove stop words
    def getMostFreqWords(self, lyrics):
        myList = lyrics.split()
        counter = collections.Counter(myList)
        tmpSorted = sorted(counter, key=counter.get, reverse=True)
        res = []
        for i in range(len(tmpSorted)):
            if len(res) == 5:
                break
            tmpWord = tmpSorted[i].lower()
            if (tmpWord not in res) and (tmpWord.isalpha()) and (tmpWord not in self.stopWords): # avoid repetition and non alpha words and stopWords.
                    res.append(tmpWord)

        return " ".join(res)

    # return the most freq words in the track currently playing
    def MostFreqWordsTest(self):
        trackObj = self.trackQueue[0]
        #find 5 random words from track
        return self.getMostFreqWords(trackObj['lyrics'])