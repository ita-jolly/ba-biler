import sqlite3
import os
import random
import string
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('DB_PATH')

bil_maerker = ["Toyota", "Ford", "BMW"]
abonnement_priser = [5499.00, 6699.00, 7999.00]

# Function to generate random nummerplader
def generate_nummerplade():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Generate 100 unique biler
def generate_biler(num_biler=100):
    biler = []
    nummerplader = set()

    while len(biler) < num_biler:
        nummerplade = generate_nummerplade()
        if nummerplade not in nummerplader:
            nummerplader.add(nummerplade)
            bil_type = random.choice(["Petrollium", "Diesel", "Elektrisk", "Hybrid"])
            maerke = random.choice(bil_maerker)
            udlejnings_status = random.choice([True, False])
            abonnement_pris = random.choice(abonnement_priser)

            biler.append((nummerplade, bil_type, maerke, udlejnings_status, abonnement_pris))
    return biler


def init():
    """Initialize the "biler" table if it doesn't exist."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS biler(
                    nummerplade TEXT PRIMARY KEY,
                    bil_type TEXT,
                    maerke TEXT,
                    udlejnings_status BOOLEAN,
                    abonnement_pris DOUBLE)
        ''')

        # Generate biler and insert them into the database
        biler = generate_biler(100)

        cur.execute('SELECT COUNT(*) FROM biler')
        row_count = cur.fetchone()[0]

        if row_count == 0:
            cur.executemany('''
                INSERT INTO biler (nummerplade, bil_type, maerke, udlejnings_status, abonnement_pris)
                VALUES (?, ?, ?, ?, ?)
            ''', biler)

    con.commit()


def get_biler():
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM biler')
        rows = cur.fetchall()

        all_biler = [{'nummerplade': row[0],
                      'bil_type': row[1],
                      'maerke': row[2],
                      'udlejnings_status': row[3],
                      'abonnement_pris': row[4]}
                      for row in rows]
        if len(all_biler) == 0:
            return None

        return all_biler


def get_udlejede_biler():
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM biler WHERE udlejnings_status = 1')
        rows = cur.fetchall()

        if len(rows) == 0:
            return None

        udlejede_biler = [{'nummerplade': row[0],
                           'bil_type': row[1],
                           'maerke': row[2],
                           'udlejnings_status': row[3],
                           'abonnement_pris': row[4]}
                           for row in rows]


        return udlejede_biler

def update_udlejnings_status(nummerplade, status):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(
            '''UPDATE biler 
                SET udlejnings_status = ? 
                WHERE nummerplade = ?''',
            (status, nummerplade)
        )
        con.commit()
        if cur.rowcount == 0:
            return None  # Nummerplade not found
    return True  # Update successful