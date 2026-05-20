import mysql.connector
import csv
import sys
sys.path.insert(0, '.')
from config import DB_CONFIG, DATA_PATH, INSERT_LIMIT

COLUMNS = [
    "duration", "protocol_type", "service", "flag",
    "src_bytes", "dst_bytes", "land", "wrong_fragments",
    "urgent", "num_failed_logins", "logged_in",
    "num_compromised", "count", "srv_count", "label"
]

COL_INDICES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 22, 23, 41]

def load(limit=INSERT_LIMIT):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = f"""
        INSERT INTO connections ({', '.join(COLUMNS)})
        VALUES ({', '.join(['%s'] * len(COLUMNS))})
    """

    rows = []
    count = 0
    with open(DATA_PATH, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if count >= limit:
                break
            extracted = [row[i] for i in COL_INDICES]
            extracted[-1] = extracted[-1].rstrip(".")
            rows.append(extracted)
            count += 1

            if len(rows) == 1000:
                cursor.executemany(sql, rows)
                conn.commit()
                rows = []
                print(f"  inserted {count} rows...", end="\r")

    if rows:
        cursor.executemany(sql, rows)
        conn.commit()

    print(f"\nDone. {count} rows loaded.")
    cursor.close()
    conn.close()
