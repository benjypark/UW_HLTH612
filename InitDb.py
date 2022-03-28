import sqlite3

connection = sqlite3.connect('sql/ecgai.db')

with open('sql/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO reports (patientId, content, originalImage, resultImage) VALUES (?, ?, ?, ?)",
            ('12345678', '95.01%', 'input01.png', 'output01.png')
            )

cur.execute("INSERT INTO reports (patientId, content, originalImage, resultImage) VALUES (?, ?, ?, ?)",
            ('12345678', '90.50%', 'input01.png', 'output01.png')
            )

cur.execute("INSERT INTO reports (patientId, content, originalImage, resultImage) VALUES (?, ?, ?, ?)",
            ('11223344', '84.00%', 'input01.png', 'output01.png')
            )

connection.commit()
connection.close()