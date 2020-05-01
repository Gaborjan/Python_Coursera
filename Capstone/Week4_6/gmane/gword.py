import sqlite3
import time
import zlib
import string

HOW_MANY_WORDS=100
BIG_SIZE=80
SMALL_SIZE=20

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, subject FROM Subjects')
subjects = dict()
for message_row in cur :
    subjects[message_row[0]] = message_row[1]

# cur.execute('SELECT id, guid,sender_id,subject_id,headers,body FROM Messages')
cur.execute('SELECT subject_id FROM Messages')
counts = dict()
for message_row in cur :
    text = subjects[message_row[0]] # a soron következő üzenet tárgya
    text = text.translate(str.maketrans('','',string.punctuation)) #elválasztó karakterek törlése
    text = text.translate(str.maketrans('','','1234567890')) #számok törlése
    text = text.strip() #bevezető és követő szóközök törlése
    text = text.lower() 
    words = text.split()
    for word in words:
        if len(word) < 4 : continue
        counts[word] = counts.get(word,0) + 1

x = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for k in x[:HOW_MANY_WORDS]:
    if highest is None or highest < counts[k] :
        highest = counts[k]
    if lowest is None or lowest > counts[k] :
        lowest = counts[k]
print('Range of counts:',highest,lowest)

# Spread the font sizes across 20-100 based on the count
fhand = open('gword.js','w')
fhand.write("gword = [")
first = True
for k in x[:HOW_MANY_WORDS]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * BIG_SIZE) + SMALL_SIZE)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to gword.js")
print("Open gword.htm in a browser to see the vizualization")
