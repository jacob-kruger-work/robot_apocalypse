from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django import template
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .db import *
from .apocalypse_models import *
from robot_apocalypse.actions import robots
from robot_apocalypse.actions import survivors
import json, time, os
import sys, traceback


def list_robots(request):
    """return a listing of all known robots"""
    bl_good, l_robots, s_msg = (False, [], "")
    t_robots = robots.list_robots()
    if t_robots[0]==True:
        l_robots = t_robots[1]
        bl_good = True
    else:
        s_msg = t_robots[2]
    if bl_good:
        return JsonResponse({"robots": l_robots}, status=200)
    else:
        return HttpResponse(s_msg, status=503)
    #return JsonResponse(response_data, json_dumps_params={'indent': 4}, safe=False)
# end of list_robots view function



@csrf_exempt
def add_survivor(request):
    """function/view to handle submitting data for a new survivor record"""
    bl_good, o_survivor, s_msg = (False, None, "")
    if request.method == "POST":
        if "name" in request.POST and "age" in request.POST and "gender" in request.POST and "id_number" in request.POST:
            try:
                s_name = request.POST.get("name", "")
                i_age = int(request.POST.get("age", 0))
                s_gender = str(request.POST.get("gender", "unknown"))
                s_id_number = str(request.POST.get("id_number", ""))
                f_latitude = float(request.POST.get("latitude", 0.0))
                f_longitude = float(request.POST.get("longitude", 0.0))
                s_inventory = str(request.POST.get("inventory", ""))
                if s_name!="" and s_id_number!="":
                    d_inventory = {}
                    l_inventory = s_inventory.split("||") if s_inventory!="" else []
                    for I in range(len(l_inventory)):
                        l_inventory[I] = str(l_inventory[I]).split("|")
                        d_inventory[l_inventory[I][0]] = int(l_inventory[I][1])
                    # end of looping through possible inventory entries
                    t_survivor = survivors.add_survivor(s_name, i_age, s_gender, s_id_number, f_latitude, f_longitude, d_inventory)
                    if t_survivor[0]==True:
                        bl_good = True
                        s_msg = "new survivor record captured"
                    else:
                        s_msg = t_survivor[2]
                else:
                    s_msg = "empty values are not permitted for name and ID number"
            except:
                s_msg = "data validation issues"
        else:
            s_msg = "values that are required are name, age, gender and id_number"
        # end of checking for required fields
    # end of checking for post request method
    # generate response content
    resp = HttpResponse(s_msg, status=400)
    if bl_good:
        resp = JsonResponse({"msg": s_msg}, status=200)
    # end of checking bl_good
    return resp
# end of add_survivor function


@csrf_exempt
def list_survivors(request):
    """return a listing of all known survivors with calculated figures"""
    bl_good, d_survivors, s_msg = (False, {}, "")
    s_name = str(request.POST.get("name", "")) if request.method == "POST" else ""
    t_survivors = survivors.list_survivors(s_name)
    if t_survivors[0]==True:
        d_survivors = t_survivors[1]
        bl_good = True
        s_msg = "survivors retrieved"
    else:
        s_msg = t_survivors[2]
    resp = HttpResponse(s_msg, status=400)
    if bl_good:
        resp = JsonResponse({"survivors": d_survivors}, status=200)
    # end of checking bl_good
    return resp
# end of list_survivors view function


@csrf_exempt
def flag_survivor(request):
    """flag a survivor as possibly infected"""
    bl_good, s_msg = (False, "attempting to process flagging")
    if request.method == "POST":
        s_reporting = str(request.POST.get("reporting", ""))
        s_infected = str(request.POST.get("infected", ""))
        if s_reporting!="" and s_infected!="":
            t_flag = survivors.flag_infected(s_reporting, s_infected)
            if t_flag[0]==True:
                bl_good = True
                s_msg = t_flag[1]
        else:
            s_msg = "ID numbers for both reporting and possibly infected must be supplied"
        # end of checking for both field values
    # end of checking if POST method
    resp = HttpResponse(s_msg, status=400)
    if bl_good:
        resp = JsonResponse({"msg": s_msg}, status=200)
    # end of checking bl_good
    return resp
# end of flag_survivor view funtion


@csrf_exempt
def gps_coordinates(request):
    """update GPS coordinates for a survivor"""
    bl_good, s_msg = (False, "updating GPS coordinates for an existing survivor record")
    if request.method == "POST":
        s_id_number = str(request.POST.get("id_number", ""))
        f_latitude = float(request.POST.get("latitude", 0.0))
        f_longitude = float(request.POST.get("longitude", 0.0))
        if s_id_number!="":
            t_gps = survivors.update_coordinates(s_id_number, f_latitude, f_longitude)
            if t_gps[0]==True:
                bl_good = True
                s_msg = t_gps[1]
        else:
            s_msg = "ID numbers must be supplied to look up survivor record"
        # end of checking for ID number value
    # end of checking if POST method
    resp = HttpResponse(s_msg, status=400)
    if bl_good:
        resp = JsonResponse({"msg": s_msg}, status=200)
    # end of checking bl_good
    return resp
# end of gps_coordinates view funtion


