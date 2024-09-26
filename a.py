import sqlite3

# Connect to the SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('customers.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table named 'customers' with id, name, email, and phone fields
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized and table created.")