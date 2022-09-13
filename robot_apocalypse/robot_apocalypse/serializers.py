from rest_framework import serializers

from .apocalypse_models import tbl_robots

class RobotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tbl_robots
        fields = ("ID", "v_model", "v_serial_number", "v_manufactured_date", "v_category")