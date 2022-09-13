"""robot_apocalypse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

#from rest_framework import routers
#router = routers.DefaultRouter()
#router.register(r'tbl_robots', views.RobotViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("robots", views.list_robots, name="list_robots"),
    path("survivors", views.list_survivors, name="list_survivors"),
    path("add", views.add_survivor, name="add_survivor"),
    path("flag", views.flag_survivor, name="flag_survivor"),
    path("gps", views.gps_coordinates, name="gps_coordinates"),
]
