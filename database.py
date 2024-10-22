import sqlite3

def initialize_db():
    conn = sqlite3.connect('rules.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY,
            rule TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_rule(rule):
    try:
        conn = sqlite3.connect('rules.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO rules (rule) VALUES (?)', (rule,))
        conn.commit()
    except Exception as e:
        raise RuntimeError(f"Error inserting rule into database: {e}")
    finally:
        conn.close()

def fetch_rules():
    try:
        conn = sqlite3.connect('rules.db')
        cursor = conn.cursor()
        cursor.execute('SELECT rule FROM rules')
        rules = cursor.fetchall()
        return [r[0] for r in rules]
    except Exception as e:
        raise RuntimeError(f"Error fetching rules from database: {e}")
    finally:
        conn.close()
