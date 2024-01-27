from rest_framework import serializers
from . import models as master_model
from accounts.serializers import RolePermissionSerializer


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_model.Master
        fields = '__all__'

class FunctionMasterSerializer(serializers.ModelSerializer):
    permissions=RolePermissionSerializer(many=True,read_only=True,source="function_permissions")

    class Meta:
        model = master_model.FunctionMaster
        # fields = ['id', 'module', 'function_name', 'description', 'record_status', 'created_at', 'modified_at','permissions']
        fields="__all__"
        read_only_fields = ['id', 'created_at', 'modified_at']

class ModuleMasterSerializer(serializers.ModelSerializer):
    module_functions = FunctionMasterSerializer(many=True, read_only=True)
    class Meta:
        model = master_model.ModuleMaster
        fields = ['id', 'module_name', 'description', 'record_status','module_functions', 'created_at', 'modified_at']
        read_only_fields = ['id', 'created_at', 'modified_at']