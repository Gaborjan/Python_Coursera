import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

#Kigyűjtjük az összes olyan oldal id-ját, amelyről van induló link (ismétlődéseket kiszedve)
#pl.: from_ids    <class 'list'>: [1, 39, 4, 82, 51]    
cur.execute('''SELECT DISTINCT from_id FROM Links''')
from_ids = list()
for row in cur: 
    from_ids.append(row[0])

# Kigyűjtjük a linkeket, csak azok a linkek kerülnek rá a links() listára, amelyek esetén legalább egy 
# oda-vissza mutató link is van.
to_ids = list() # az összes link amire van mutató valamely oldalról
links = list() # azok a linkek amelyeknél igaz az, hogy kölcsönösség áll fennt, tehát adott oldalról
#oda-vissza legalább egy hivatkozás van
# pl.: links    <class 'list'>: [
#(1, 4), (1, 39), (1, 51), 
#(39, 1), (39, 82), (39, 4), 
#(4, 1), (4, 39), (4, 82), (4, 51), 
#(82, 1), (82, 4), (82, 39), 
# (51, 1), (51, 4)] 
#to_ids    <class 'list'>: [4, 39, 51, 1, 82]    

cur.execute('''SELECT DISTINCT from_id, to_id FROM Links''')
for row in cur:
    from_id = row[0]
    to_id = row[1]
    if from_id == to_id : continue
    if from_id not in from_ids : continue
    if to_id not in from_ids : continue
    links.append(row)
    if to_id not in to_ids : to_ids.append(to_id)

# A prev_ranks-ba kigyűjtjük az oldalak aktuális rankját, ami kezdetben 1.0
prev_ranks = dict()
for node in from_ids:
    cur.execute('''SELECT new_rank FROM Pages WHERE id = ?''', (node, ))
    row = cur.fetchone()
    prev_ranks[node] = row[0]

sval = input('How many iterations:')
many = 1
if ( len(sval) > 0 ) : many = int(sval)

# Sanity check
if len(prev_ranks) < 1 : 
    print("Nothing to page rank.  Check data.")
    quit()

# Lets do Page Rank in memory so it is really fast
for i in range(many):
    next_ranks = dict(); # ebben lesznek az algoritmus lefutása utáni új rank értékek
    total = 0.0 # a régi oldal rank-ok összege
    for (node, old_rank) in list(prev_ranks.items()): # kiszámítjuk a korábbi rankok összegét, az új rankot 0-ra állítjuk
        total = total + old_rank
        next_ranks[node] = 0.0
    
    # Ez az algoritmus lényegi része. Fontos, hogy annyi pontszámot kell felosztanunk, ahány elemű
    # a from_ids lista, vagyis ahány olyan oldal van, amelyről legalább 1 link indul. A példánkban
    #ez 5. Végigmegyünk az összes oda-vissza linken (links lista elemei). Megszámoljuk az aktuális
    #oldalról hány link indul, ezeknek az oldalaknak "adni" kell valamennyi ranget, de mivel az összes
    #oda-vissza linket végigmegyünk "kapni" is fogunk ranget. Az algortimus során azok az oldalak kapnak
    #majd magasabb ranget, amelyekre több bejövő hivatkozás van, mint kimenő.
    #Pl. a 39-es oldal 3-nak ad, 3-tól kap, az 1-es oldal 3-nak ad, 4-től kap.
    for (node, old_rank) in list(prev_ranks.items()): #node: a vizsgált oldal
        # print node, old_rank
        give_ids = list() # ebbe a listába kerülnek azoknak az oldalaknak a id-ja amelyre a node-oldalról hivatkozás van
        for (from_id, to_id) in links: #az összes linken végigmegyünk
            if from_id != node : continue # csak azokat nézzük amelyik node-on vagyunk
            if to_id not in to_ids: continue # ha a node-hoz tartozó to_id nem mutat egyik to_id-ra sem (nincs kapcsolat, pl. az 1. oldal nem mutat a 82-re
            give_ids.append(to_id) # a node-nak van kapcsolata az aktuális to_id-val, ezért eltesszük hová mutat
        if ( len(give_ids) < 1 ) : continue # ha az adott node-nak egyik to_id-vel sem volt kapcsolata
        amount = old_rank / len(give_ids) # a node aktuális rankját annyi felé osztjuk, ahány kimenő linket találtunk
        #ezeknek a linkeknek kell "adni"
        for id in give_ids: #a ciklusban ki is osztjuk a kimenő linkeknek járó rank egységet
            next_ranks[id] = next_ranks[id] + amount
                    
    newtot = 0
    for (node, next_rank) in list(next_ranks.items()): 
         newtot = newtot + next_rank # összegezzük mennyi új rankot adtunk ki összesen
    evap = (total - newtot) / len(next_ranks) # a régi és az új rankok között mindig van egy kis eltérés
    #Nagyon fontos ennek figyelembe vétele! Az eltérést egyenlően elosztjuk minden oldal rankjára.

    for node in next_ranks: # az eltéréssel minden oldal rankját korrigáljuk
        next_ranks[node] = next_ranks[node] + evap

    #összegezzük az új rankok értékét, amit már korrigáltunk az evap-pal
    newtot = 0 
    for (node, next_rank) in list(next_ranks.items()):
        newtot = newtot + next_rank

    #összegezzük a régi és új rankok között eltéréseket
    totdiff = 0
    for (node, old_rank) in list(prev_ranks.items()):
        new_rank = next_ranks[node]
        diff = abs(old_rank-new_rank)
        totdiff = totdiff + diff
    
    #kiszámoljuk az új és régi rankok eltéréseinek átlagát, ez az érték minél inkább közelít a 0-hoz
    #annál jobb, kiegyensúlyozottabb az értékelés, vagyis már nem lehet jobban szétosztani a rankokat.
    #Ez csak addig igaz, amíg nem jön be új, még nem rangsorolt oldal.    
    avediff = totdiff / len(prev_ranks)
    print(i+1, 'Adiff: ', avediff, 'Evap: ', evap)
    
   # újból kezdődik a rankok kiosztása, ezért az új rankokkal aktualizáljuk a régi rank listát
    prev_ranks = next_ranks
    print(list(next_ranks.items())[:5])
    
# Put the final ranks back into the database
#print(list(next_ranks.items())[:5])
cur.execute('''UPDATE Pages SET old_rank=new_rank''')
for (id, new_rank) in list(next_ranks.items()) :
    cur.execute('''UPDATE Pages SET new_rank=? WHERE id=?''', (new_rank, id))
conn.commit()

cur.execute('''SELECT COUNT(new_rank) FROM Pages WHERE Pages.new_rank>0 AND Pages.html IS NOT NULL''')
count_row = cur.fetchone()
print('Counted rows:', count_row[0])
cur.execute('''SELECT SUM(new_rank) FROM Pages WHERE Pages.new_rank>0 AND Pages.html IS NOT NULL''')
sum_row = cur.fetchone()
print('Sum of ranks: ', sum_row[0])
print('Difference between sum and counted: ', float(count_row[0])-sum_row[0])
cur.close()

