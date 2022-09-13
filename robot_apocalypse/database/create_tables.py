# sql script to create database structures
# https://www.sqlitetutorial.net/sqlite-create-table/
# https://www.sqlite.org/datatype3.html
import sqlite3, os, json
import sys


l_sql = []
s_robots = """
CREATE TABLE IF NOT EXISTS main.tbl_robots (
    ID INTEGER PRIMARY KEY,
    v_model TEXT NOT NULL UNIQUE,
    v_serial_number TEXT NOT NULL UNIQUE,
    v_manufactured_date TEXT NOT NULL,
    v_category TEXT NOT NULL DEFAULT 'land'
);
"""
l_sql.append(s_robots)

s_survivors = """
CREATE TABLE IF NOT EXISTS main.tbl_survivors (
    ID INTEGER PRIMARY KEY,
    v_name TEXT NOT NULL DEFAULT '',
    i_age INTEGER DEFAULT 0,
    v_gender TEXT NOT NULL DEFAULT '',
    v_id_number TEXT NOT NULL UNIQUE,
    r_latitude REAL DEFAULT 0.0,
    r_longitude REAL DEFAULT 0.0
);
"""
l_sql.append(s_survivors)

s_infected = """
CREATE TABLE IF NOT EXISTS main.tbl_infected (
    ID INTEGER PRIMARY KEY,
    i_reporting_id INTEGER NOT NULL DEFAULT 0,
    i_infected_id INTEGER NOT NULL DEFAULT 0
);
"""
l_sql.append(s_infected)

s_inventory = """
CREATE TABLE IF NOT EXISTS main.tbl_inventory (
    ID INTEGER PRIMARY KEY,
    i_survivor_id INTEGER NOT NULL DEFAULT 0,
    i_count INTEGER NOT NULL DEFAULT 0,
    v_description TEXT DEFAULT ''
);
"""
l_sql.append(s_inventory)

s_db_path = os.path.realpath(__file__).replace("create_tables.py", "apocalypse.db")
s_json_path = s_db_path.replace("apocalypse.db", "robots.json")
print(s_db_path)
print(s_json_path)
if os.path.exists(s_db_path): os.unlink(s_db_path)
cn = sqlite3.connect(s_db_path)
cur = cn.cursor()

# create tables
for s_sql in l_sql:
    cur.execute(s_sql)
    cn.commit()

# populate robots data
s_robot_data = open(s_json_path, "r").read()
l_robots = json.loads(s_robot_data)
i_total = len(l_robots)
i_count = 0
for d_robot in l_robots:
    #print(list(d_robot.keys())); break
    i_count = i_count + 1
    s_robot_sql = "insert into tbl_robots (v_model, v_serial_number, v_manufactured_date, v_category) values ('{model}', '{serialNumber}', '{manufacturedDate}', '{category}');".format(**d_robot)
    cur.execute(s_robot_sql)
cn.commit()
print(f"{i_count} robot records inserted")
cur.close()
cn.close()
print("done!")
