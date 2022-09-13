#!/usr/bin/python3
"""sqlite3 database connection implementation using sqlalchemy"""
import sqlalchemy
from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import sessionmaker
from os import environ
import hashlib
from robot_apocalypse import settings
s_timezone = settings.TIME_ZONE.lower()

engine = None
session = None

def do_connect(s_path="apocalypse.db"):
    """create engine and session objects for sqlalchemy activities against sqlite3 database"""
    global s_timezone, engine, session
    # create an engine
    #s_full_path = f"{settings.PROJECT_PATH}/database/{s_path}".replace("\\", "/")
    s_sqlite3 = "sqlite:///./database/apocalypse.db"
    engine = create_engine(s_sqlite3)
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()
    return (engine, session)
#end of do_connect function


def dict_row(r_in):
    """render a dict collection for a database record"""
    d_out = {}
    l_keys = []
    if type(r_in)==sqlalchemy.engine.row.Row:
        l_keys = list(r_in.keys())
    else:
        l_keys = list(r_in.__dict__.keys())
        r_in = r_in.__dict__
    # end of type check on r_in
    for sk in l_keys:
        if not str(sk).startswith("_"): d_out[sk] = r_in[sk]
    return d_out
#end of dict_row function


def compute_md5_hash(data):
    """encrypt data into md5 encrypted string"""
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    return m.hexdigest()
# end of compute_md5_hash function


def merge_not_in(q_filter):
    l_out = []
    for t in list(q_filter):
        l_out.append(int(t[0]))
    return l_out
#end of merge_not_in
