import sqlite3

# Connect to your database
conn = sqlite3.connect('missing_persons.db')
cur = conn.cursor()

# Update the created_at field to the correct format
cur.execute("UPDATE user SET created_at = REPLACE(SUBSTR(created_at, 1, 19), 'T', ' ') WHERE created_at LIKE '%T%';")
conn.commit()
conn.close()

print("User created_at fields updated successfully.")
