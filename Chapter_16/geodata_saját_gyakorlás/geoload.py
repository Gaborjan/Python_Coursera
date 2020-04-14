
import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys
import re

api_key = False #Ha van saját API akkor ez True
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'

if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"
    


# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Locations')

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (cim TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("Allomasok.csv")
count = 0
for line in fh:
    cs_data = line.split(";") #.cs fájl szétdarabolása
    if (cs_data[4]=="Elő"): address=cs_data[7] # Csak az élőkkel foglalkozunk
    else: continue
    if re.match("[0-9][0-9][0-9][0-9][0-9]",address): #Ha 5 db számjeggyel kezdődik a cím, ez az irányítószám
        cim=address[:4]+address[5:] #Az irányítószám utolsó jegyét le kell venni, mert 5 hosszúra egészíti ki a forrás rendszer
    else: #Nem szabványos cím, vélhetően külföldi cím
        cim=address
    cur.execute("SELECT geodata FROM Locations WHERE cim= ?",
        (memoryview(cim.encode()), )) #Megnézzük van-e már ilyen cím a táblában?
    
    try:
        data = cur.fetchone()[0] #Ha van már ilyen címünk
        print("Found in database ",address)
        continue
    except:
        pass
 
    parms = dict()
    parms["address"] = cim
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms) #A google maps számára összeállítjuk a szükséges lekérdező URL-t
 
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx) #Lekérdezés
    data = uh.read().decode() #Megkaptuk az eredményt, eltesszök a data stringbe
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1
 
    try:
        js = json.loads(data) #json adattá alakítjuk a lekérdezés eredményét
    except:
        print(data)  # We print in case unicode causes an error
        continue
 
    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('==== Failure To Retrieve ====')
        print(data)
        break
 
    cur.execute('''INSERT INTO Locations (cim, geodata)
            VALUES ( ?, ? )''', (memoryview(cim.encode()), memoryview(data.encode()) ) ) #cím és google lekérdezés eredményét elmentjük az adatbázisba 
    print(js['results'][0]['formatted_address'])
    conn.commit()
print(count,'different locations found.')     
print("Run geodump.py to read the data from the database so you can vizualize it on a map.")
print(type(js))
print(type(cim))




