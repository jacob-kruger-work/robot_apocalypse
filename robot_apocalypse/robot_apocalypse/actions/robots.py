#!/usr/bin/python3
import requests, json, sys, traceback
from robot_apocalypse import db, settings
from robot_apocalypse.apocalypse_models import *
from robot_apocalypse.sql_log import write_log


# URL to possibly retrieve listing of robots
s_url = "https://robotstakeover20210903110417.azurewebsites.net/robotcpu"
# otherwise a local version of said file
s_file = "robots.json"


def populate_robots():
    """retrieve either a remote list of robots or populate from local file"""
    global s_url, s_file
    bl_good, s_msg = (False, "")
    s_json = ""
    # retrieve either remote or local json contents
    try:
        resp = requests.get(s_url)
        if resp.status_code==200:
            s_json = str(resp.text)
            s_msg = "populated from remote source"
        else:
            s_json = open(f"{settings.PROJECT_PATH}\\database\\robots.json", "r").read()
            s_msg = "populated from local source"
        # end of retrieving json from either remote or local file
        if s_json=="": raise Exception("issue retrieving list of robots from external source")
        engine, session = db.do_connect()
        # first retrieve list of serial keys already in database
        l_serials = [t[0] for t in session.query(tbl_robots.v_serial_number).all()]
        l_robots = json.loads(s_json)
        for d_robot in l_robots:
            # ['model', 'serialNumber', 'manufacturedDate', 'category']
            # v_model, v_serial_number, v_manufactured_date, v_category
            if l_serials.count(d_robot["serialNumber"])<1:
                session.add(tbl_robots(v_model=d_robot["model"], v_serial_number=d_robot["serialNumber"], v_manufactured_date=d_robot["manufacturedDate"], v_category=d_robot["category"]))
                session.commit()
        # end of looping through imported robot entries
        session.close(); engine.dispose()
        bl_good = True
        s_msg = "new robot records populated"
    except Exception as exc:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        s_tb = traceback.format_exc()
        s_tb = s_tb.replace("\n  File", "\n----\n  File").replace("'", "|")
        s_why = s_tb
        s_where = "retrieving robots listing"
        s_msg = f"{s_where} - {s_tb}"
        s_what = str(exc_type).replace("'", "|")
        try:
            write_log(s_why, s_what, s_where)
        except:
            pass
    # end of outer try-except
    return (bl_good, s_msg)
# end of populate_robots function


def list_robots(s_category=""):
    """retrieve a listing of robots"""
    bl_good, l_robots, s_msg = (False, [], "")
    try:
        engine, session = db.do_connect()
        qry = session.query(tbl_robots.ID, tbl_robots.v_model, tbl_robots.v_serial_number, tbl_robots.v_manufactured_date, tbl_robots.v_category)
        if s_category!="": qry = qry.filter(tbl_robots.v_category==s_category)
        l_qry = qry.all()
        session.close(); engine.dispose()
        for r in l_qry:
            l_robots.append(db.dict_row(r))
        bl_good = True
        s_msg = "current robot records retrieved"
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        s_tb = traceback.format_exc()
        s_tb = s_tb.replace("\n  File", "\n----\n  File").replace("'", "|")
        s_why = s_tb
        s_where = "retrieving robots listing"
        s_msg = f"{s_where} - {s_tb}"
        s_what = str(exc_type).replace("'", "|")
        try:
            write_log(s_why, s_what, s_where)
        except:
            pass
    # end of outer try-except
    return (bl_good, l_robots, s_msg)
# end of list_robots function

