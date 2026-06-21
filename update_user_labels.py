import psycopg2
from bdl_mirror import VARIABLES_MAP

DSN = "dbname=bdl_local user=bdl_user password=mocne_haslo host=localhost port=5432"

conn = psycopg2.connect(DSN)
cur = conn.cursor()

cur.execute("ALTER TABLE variables ADD COLUMN IF NOT EXISTS user_label TEXT")
conn.commit()

count = 0

for category, items in VARIABLES_MAP.items():
    for var_id, user_label in items:
        cur.execute("""
            UPDATE variables
            SET user_label = %s
            WHERE id = %s
        """, (user_label, var_id))
        count += cur.rowcount

conn.commit()
cur.close()
conn.close()

print(f"Zaktualizowano user_label dla {count} zmiennych.")
