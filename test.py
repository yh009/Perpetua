from smartPlaylist import SmartPlaylist

myPlayList = SmartPlaylist("Pots and Pans", '12832752fc79e94b205e24b1a5bf7a4d')
#print(myPlayList.stopWords)
#print(myPlayList.getTrackQueue())
print(myPlayList.getPlayed())

print(myPlayList.MostFreqWordsTest())
new = myPlayList.trackFinished()
print(new['track_id'])

#print(myPlayList.getTrackQueue())
print(myPlayList.getPlayed())

print(myPlayList.MostFreqWordsTest())
new = myPlayList.trackFinished()
print(new['track_id'])

print(myPlayList.MostFreqWordsTest())
#print(myPlayList.getTrackQueue())
print(myPlayList.getPlayed())