#!/usr/bin/python3
import json, sys, traceback
from robot_apocalypse import db
from robot_apocalypse.apocalypse_models import *
from robot_apocalypse.sql_log import write_log
from sqlalchemy import func


def add_survivor(s_name, i_age, s_gender, s_id_number, f_latitude, f_longitude, d_inventory={}):
    """capture data for a new survivor entry"""
    bl_good, i_id, s_msg = (False, 0, "")
    try:
        engine, session = db.do_connect()
        # check if there is already a record with matching v_id_number - just in case
        qry = session.query(tbl_survivors.ID).filter(tbl_survivors.v_id_number==s_id_number)
        if qry.count()>0:
            session.close(); engine.dispose()
            s_msg = "issue - already an existing survivor record with same ID number"
        else:
            o_survivor = tbl_survivors(v_name=s_name, i_age=i_age, v_gender=s_gender, v_id_number=s_id_number, r_latitude=f_latitude, r_longitude=f_longitude)
            session.add(o_survivor)
            session.commit()
            if o_survivor.ID>0:
                i_id = o_survivor.ID
                s_msg = "new survivor entry captured"
                if len(d_inventory)>0:
                    for s_key in d_inventory:
                        session.add(tbl_inventory(i_survivor_id=i_id, i_count=d_inventory[s_key], v_description=s_key))
                    # end of looping through inventory items
                    session.commit()
                    s_msg = s_msg + " - inventory items captured"
                # end of checking length of d_inventory
                session.close(); engine.dispose()
                bl_good = True
            # end of making sure survivor record was recorded
        # end of checking for prior record with same ID number
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        s_tb = traceback.format_exc()
        s_tb = s_tb.replace("\n  File", "\n----\n  File").replace("'", "|")
        s_why = s_tb
        s_where = "capturing initial survivor entry"
        s_msg = f"{s_where} - {s_tb}"
        s_what = str(exc_type).replace("'", "|")
        try:
            write_log(s_why, s_what, s_where)
        except:
            pass
    # end of outer try-except
    return (bl_good, i_id, s_msg)
# end of add_survivor function


def update_coordinates(s_id_number="", f_latitude=0.0, f_longitude=0.0):
    """update GPS coordinates for an existing survivor record"""
    bl_good, s_msg = (False, "")
    try:
        engine, session = db.do_connect()
        o_survivor = None
        qry = session.query(tbl_survivors).filter(tbl_survivors.v_id_number==s_id_number)
        if qry.count()>0:
            o_survivor = qry.first()
        # end of checking if s_id_number worked for lookup
        if o_survivor is not None:
            o_survivor.r_latitude = f_latitude
            o_survivor.r_longitude = f_longitude
            session.commit()
            s_msg = "GPS coordinates updated"
            bl_good = True
        else:
            s_msg = "issue looking up prior entry"
        # end of checking if could look up prior record
        session.close(); engine.dispose()
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        s_tb = traceback.format_exc()
        s_tb = s_tb.replace("\n  File", "\n----\n  File").replace("'", "|")
        s_why = s_tb
        s_where = "updating survivor record GPS coordinates"
        s_msg = f"{s_where} - {s_tb}"
        s_what = str(exc_type).replace("'", "|")
        try:
            write_log(s_why, s_what, s_where)
        except:
            pass
    # end of outer try-except
    return (bl_good, s_msg)
# end of update_coordinates function


def flag_infected(s_reporting="", s_infected=""):
    """add infected reporting flag from a survivor for a survivor"""
    bl_good, s_msg = (False, "")
    try:
        engine, session = db.do_connect()
        o_reporting, o_infected = (None, None)
        qry = session.query(tbl_survivors).filter(tbl_survivors.v_id_number==s_reporting)
        if qry.count()>0:
            o_reporting = qry.first()
        # end of checking if s_reporting worked for lookup
        qry = session.query(tbl_survivors).filter(tbl_survivors.v_id_number==s_infected)
        if qry.count()>0:
            o_infected = qry.first()
        # end of checking if s_infected worked for lookup
        if o_reporting is not None and o_infected is not None:
            i_reporting, i_infected = (o_reporting.ID, o_infected.ID)
            # first make sure this survivor has not already reported the same survivor infected
            qry_already = session.query(tbl_infected.ID).filter(tbl_infected.i_reporting_id==i_reporting, tbl_infected.i_infected_id==i_infected)
            if qry_already.count()<1:
                o_flag = tbl_infected(i_reporting_id=i_reporting, i_infected_id=i_infected)
                session.add(o_flag)
                session.commit()
            # end of checking against a prior matching record
            s_msg = "infected flag record captured if had not already been recorded"
            bl_good = True
        else:
            s_msg = "issue looking up reporting and infected survivors"
        # end of checking if could look up survivor record
        session.close(); engine.dispose()
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        s_tb = traceback.format_exc()
        s_tb = s_tb.replace("\n  File", "\n----\n  File").replace("'", "|")
        s_why = s_tb
        s_where = "inserting infected flag records"
        s_msg = f"{s_where} - {s_tb}"
        s_what = str(exc_type).replace("'", "|")
        try:
            write_log(s_why, s_what, s_where)
        except:
            pass
    # end of outer try-except
    return (bl_good, s_msg)
# end of flag_infected function


def survivor_inventory(i_survivor_id):
    """retrieve inventory dict for specific survivor"""
    bl_good, d_inventory, s_msg = (False, {}, "")
    try:
        engine, session = db.do_connect()
        qry = session.query(tbl_inventory.i_count, tbl_inventory.v_description).filter(tbl_inventory.i_survivor_id==i_survivor_id)
        for r in qry.all():
            d_inventory[str(r.v_description)] = int(r.i_count)
        # end of looping through inventory rows returned
        session.close(); engine.dispose()
        bl_good = True
        s_msg = "inventory retrieved"
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        s_tb = traceback.format_exc()
        s_tb = s_tb.replace("\n  File", "\n----\n  File").replace("'", "|")
        s_why = s_tb
        s_where = "retrieving survivor inventory"
        s_msg = f"{s_where} - {s_tb}"
        s_what = str(exc_type).replace("'", "|")
        try:
            write_log(s_why, s_what, s_where)
        except:
            pass
    # end of outer try-except
    return (bl_good, d_inventory, s_msg)
# end of survivor_inventory function


def list_survivors(s_name=""):
    """retrieve a listing of survivors"""
    bl_good, l_survivors, d_survivors, s_msg = (False, [], {"i_total": 0, "i_not_infected": 0, "i_infected": 0, "s_not_infected_percentage": "0.00%", "s_infected_percentage": "0.00%", "l_all": [], "l_not_infected": [], "l_infected": []}, "")
    try:
        engine, session = db.do_connect()
        # would have used below, but sqlite3 seems to have issue with left outer join retrieving more than one record from left table
        # qry = session.query(tbl_survivors.ID, tbl_survivors.v_name, tbl_survivors.i_age, tbl_survivors.v_gender, tbl_survivors.v_id_number, tbl_survivors.r_latitude, tbl_survivors.r_longitude, func.count(tbl_infected.ID).label("i_infected_count")).join(tbl_infected, tbl_survivors.ID==tbl_infected.i_infected_id, isouter=True).order_by(tbl_survivors.v_name)
        qry = session.query(tbl_survivors.ID, tbl_survivors.v_name, tbl_survivors.i_age, tbl_survivors.v_gender, tbl_survivors.v_id_number, tbl_survivors.r_latitude, tbl_survivors.r_longitude)
        if s_name!="":
            s_search = f"%{s_name}%".lower()
            qry = qry.filter(tbl_survivor.v_name.like(s_search))
        qry = qry.order_by(tbl_survivors.v_name)
        l_qry = qry.all()
        for r in l_qry:
            l_survivors.append(db.dict_row(r))
            # fetch infected reporting count per survivor
            qry_infected = session.query(func.count(tbl_infected.ID)).filter(tbl_infected.i_infected_id==l_survivors[-1]["ID"])
            l_survivors[-1]["i_infected_count"] = qry_infected[0][0]
        session.close(); engine.dispose()
        # populate inventory per survivor
        for I in range(len(l_survivors)):
            l_survivors[I]["d_inventory"] = {}
            t_inventory = survivor_inventory(l_survivors[I]["ID"])
            if t_inventory[0]==True: l_survivors[I]["d_inventory"] = t_inventory[1]
        # end of looping through survivors list
        # group survivors by infection flagging and calculate percentages
        # {"i_total": 0, "i_not_infected": 0, "i_infected": 0, "s_not_infected_percentage": "0.00%", "s_infected_percentage": "0.00%", "l_all": [], "l_not_infected": [], "l_infected": []}
        l_not_infected, l_infected = ([], [])
        for d_survivor in l_survivors:
            if d_survivor["i_infected_count"]<3:
                l_not_infected.append(d_survivor)
            else:
                l_infected.append(d_survivor)
            # end of checking against infection flag count
        # end of looping through all survivor records
        # make calculations
        i_total = len(l_survivors)
        i_not_infected = len(l_not_infected)
        i_infected = len(l_infected)
        s_not_infected_percentage = "{:.2f}".format(float(i_not_infected)/float(i_total) * 100) + "%"
        s_infected_percentage = "{:.2f}".format(float(i_infected)/float(i_total) * 100) + "%"
        d_survivors["i_total"], d_survivors["i_not_infected"], d_survivors["i_infected"], d_survivors["s_not_infected_percentage"], d_survivors["s_infected_percentage"], d_survivors["l_all"], d_survivors["l_not_infected"], d_survivors["l_infected"] = (i_total, i_not_infected, i_infected, s_not_infected_percentage, s_infected_percentage, l_survivors, l_not_infected, l_infected)
        bl_good = True
        s_msg = "current survivor records retrieved and figures calculated"
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        s_tb = traceback.format_exc()
        s_tb = s_tb.replace("\n  File", "\n----\n  File").replace("'", "|")
        s_why = s_tb
        s_where = "retrieving survivors listing"
        s_msg = f"{s_where} - {s_tb}"
        s_what = str(exc_type).replace("'", "|")
        try:
            write_log(s_why, s_what, s_where)
        except:
            pass
    # end of outer try-except
    return (bl_good, d_survivors, s_msg)
# end of list_survivors function


