
from rest_framework import serializers
from . import models as master_model
from mes.users.serializers import RolePermissionSerializer



class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_model.Master
        fields = '__all__'


class FunctionSerializer(serializers.ModelSerializer):
    permissions=RolePermissionSerializer(many=True,read_only=True,source="function_permissions")

    class Meta:
        model = master_model.Function
        # fields = ['id', 'module', 'function_name', 'description', 'record_status', 'created_at', 'modified_at','permissions']
        fields="__all__"
        read_only_fields = ['id', 'created_at', 'modified_at']


class ModuleSerializer(serializers.ModelSerializer):
    module_functions = FunctionSerializer(many=True, read_only=True)
    class Meta:
        model = master_model.Module
        fields = ['id', 'module_name', 'description', 'record_status','module_functions', ]
        read_only_fields = ['id', 'created_at',]