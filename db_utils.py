import sqlite3
import os

DB_FILE = "il_ilce.db"

# Basit seed; orijinal büyük listeyi burada da kullanabilirsin.
SEED_IL_ILCE = {
    "Adana": ["Aladağ", "Ceyhan", "Çukurova", "Feke", "İmamoğlu"],
    "Ankara": ["Çankaya", "Keçiören", "Mamak", "Sincan"],
    "İstanbul": ["Avcılar", "Bakırköy", "Beşiktaş", "Kadıköy"],
    "İzmir": ["Konak", "Bornova", "Karşıyaka"]
}

def get_conn():
    return sqlite3.connect(DB_FILE)

def init_db_and_migrate(seed_dict=None):
    """
    Create DB if not exists and seed from seed_dict if tables empty.
    """
    if seed_dict is None:
        seed_dict = SEED_IL_ILCE
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS provinces(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )"""
    )
    cur.execute("""
    CREATE TABLE IF NOT EXISTS districts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        province_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        UNIQUE(province_id, name),
        FOREIGN KEY(province_id) REFERENCES provinces(id) ON DELETE CASCADE
    )"""
    )
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM provinces")
    count = cur.fetchone()[0]
    if count == 0:
        for prov, districts in seed_dict.items():
            cur.execute("INSERT INTO provinces(name) VALUES(?)", (prov,))
            pid = cur.lastrowid
            for d in districts:
                cur.execute("INSERT INTO districts(province_id, name) VALUES(?,?)", (pid, d))
        conn.commit()
    conn.close()

def query_provinces(search=""):
    conn = get_conn()
    cur = conn.cursor()
    if search:
        cur.execute("SELECT name FROM provinces WHERE name LIKE ? ORDER BY name", (f"%{search}%,"))
    else:
        cur.execute("SELECT name FROM provinces ORDER BY name")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def query_districts(province_name, search=""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM provinces WHERE name=", (province_name,))
    # safer query
    cur.execute("SELECT id FROM provinces WHERE name=?", (province_name,))
    row = cur.fetchone()
    if not row:
        conn.close(); return []
    pid = row[0]
    if search:
        cur.execute("SELECT name FROM districts WHERE province_id=? AND name LIKE ? ORDER BY name", (pid, f"%{search}%,"))
    else:
        cur.execute("SELECT name FROM districts WHERE province_id=? ORDER BY name", (pid,))
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def add_province(name):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO provinces(name) VALUES(?)", (name.strip(),))
    conn.commit(); conn.close()

def rename_province(old_name, new_name):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("UPDATE provinces SET name=? WHERE name=?", (new_name.strip(), old_name.strip()))
    conn.commit(); conn.close()

def delete_province(name):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("DELETE FROM provinces WHERE name=?", (name.strip(),))
    conn.commit(); conn.close()

def add_district(province_name, district_name):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT id FROM provinces WHERE name=?", (province_name,))
    r = cur.fetchone()
    if not r:
        conn.close(); raise ValueError("Province not found")
    pid = r[0]
    cur.execute("INSERT OR IGNORE INTO districts(province_id, name) VALUES(?,?)", (pid, district_name.strip()))
    conn.commit(); conn.close()

def rename_district(province_name, old_name, new_name):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT id FROM provinces WHERE name=?", (province_name,))
    r = cur.fetchone()
    if not r:
        conn.close(); raise ValueError("Province not found")
    pid = r[0]
    cur.execute("UPDATE districts SET name=? WHERE province_id=? AND name=?", (new_name.strip(), pid, old_name.strip()))
    conn.commit(); conn.close()

def delete_district(province_name, district_name):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT id FROM provinces WHERE name=?", (province_name,))
    r = cur.fetchone()
    if not r:
        conn.close(); raise ValueError("Province not found")
    pid = r[0]
    cur.execute("DELETE FROM districts WHERE province_id=? AND name=?", (pid, district_name.strip()))
    conn.commit(); conn.close()