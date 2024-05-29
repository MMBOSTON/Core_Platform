import sqlite3

def create_sample_db(db_url):
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        hashed_password TEXT NOT NULL
    )
    ''')

    # Insert sample data
    cursor.executemany('''
    INSERT INTO users (username, password, hashed_password) VALUES (?, ?, ?)
    ''', [
        ('user1', 'password1', 'hashedpassword1'),
        ('user2', 'password2', 'hashedpassword2'),
        ('user3', 'password3', 'hashedpassword3')
    ])

    conn.commit()
    conn.close()

# Create sample databases
create_sample_db('./data_storage/dev.db')
create_sample_db('./data_storage/test.db')
