from rest_framework import serializers

from . models import FurnaceConfig


class FurnaceConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model=FurnaceConfig
        fields="__all__"