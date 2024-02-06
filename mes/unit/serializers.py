from . import models as unit_model
from rest_framework import serializers
from mes.plant.models import PlantConfig
from mes.utils.models import Master


class UnitSerializer(serializers.ModelSerializer):
    unit=serializers.SerializerMethodField()
    class Meta:
        model=unit_model.GlobalUnit
        fields=['id','name','unit']
    def get_unit(self,obj):
        plant=PlantConfig.objects.first()
        master=Master.objects.filter(pk=plant.unit_id).first()
        if master.value=='Metric System':
            return obj.metric
        else:
            return obj.imperial
        