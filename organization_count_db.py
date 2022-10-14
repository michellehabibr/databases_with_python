#Michelle Habib Oct-14-2022
#Counts the number of emails from each organization
# if none, it adds a new column with the organization and count = 1
import sqlite3

conn = sqlite3.connect('orgdb2.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''') #schema

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split('@')
    org = pieces[1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    #The ? in org is a placeholder to avoid an SQL injection
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()
    # this forces everything to be written to disk (slow process)

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
