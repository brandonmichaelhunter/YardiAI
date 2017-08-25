import DataManager

dm = DataManager.DataManager()
IsConnected = dm.IsConnected()
dbRecs = dm.GetRecentPosts()
print("Is connected {}.".format(IsConnected))
for item in dbRecs.each():
    print(item.key()) # Morty
    print(item.val()) # {name": "Mortimer 'Morty' Smith"}