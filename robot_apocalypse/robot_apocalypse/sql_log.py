import sqlite3
import time
import sys, os
import robot_apocalypse

s_path = robot_apocalypse.settings.PROJECT_PATH
s_log_db = f"{s_path}/logs/logging.db"
#print(s_log_db)

initial_sql = """CREATE TABLE IF NOT EXISTS log(
    timestamp TEXT,
    type TEXT,
    details TEXT,
    location TEXT
    );
"""

insertion_sql = """INSERT INTO log(
    timestamp,
    type,
    details,
    location)
    VALUES (
    '{0}',
    '{1}',
    '{2}',
    '{3}');
"""

def write_log(s_why, s_what, s_where):
    """write a log entry to default file name sqlite3 database"""
    global s_log_db, initial_sql, insertion_sql
    try:
        conn = sqlite3.connect(s_log_db)
        # create table if does not exist
        cur = conn.execute(initial_sql)
        conn.commit()
        s_when = time.strftime("%Y-%m-%d %H:%M:%S")
        s_insert = insertion_sql.format(s_when, s_why, s_what, s_where)
        curi = conn.execute(s_insert)
        conn.commit()
    except Exception as exc:
        s_log_dump = s_log_db.replace(".db", ".exc")
        f = open(s_log_dump, "w")
        f.write(str(sys.exc_info()))
        f.close()
    return True
# end of write_log function
