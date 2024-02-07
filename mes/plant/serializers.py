from rest_framework import serializers
from .models import TimeZone,Language,Unit,Currency,Product,Function,ERP,PlantConfig, PlantConfigProduct, PlantConfigWorkshop,PlantConfigFunction
from . import models as m
from mes.furnace.models import FurnaceConfig,FurnaceConfigStep,FurnaceElectrode,FurnaceProduct,ControlParameter,Additive



class TimeZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeZone
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = '__all__'


class PlantConfigProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantConfigProduct
        fields = '__all__'

class PlantConfigWorkshopSerializer(serializers.ModelSerializer):
    is_deactivate=serializers.SerializerMethodField()
    class Meta:
        model = PlantConfigWorkshop
        fields = '__all__'

    def get_is_deactivate(self,obj):
        furnace=FurnaceConfig.objects.filter(workshop=obj)
        if furnace.exists():
            return False
        else:return True

class PlantConfigFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantConfigFunction
        fields = '__all__'


class PlantConfigSerializer(serializers.ModelSerializer):
    products_json = PlantConfigProductSerializer(many=True,read_only=True,source="plant_config_products")
    workshops_json = PlantConfigWorkshopSerializer(many=True,read_only=True,source="plant_config_workshops")
    function_json = PlantConfigFunctionSerializer(many=True,read_only=True,source="plant_config_function")
    
    class Meta:
        model = PlantConfig
        fields = '__all__'


    def create(self, validated_data):
        plant_config= PlantConfig.objects.create(**validated_data)
        return plant_config

class ERPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ERP
        fields = '__all__'


class FurnaceElectrodeSerializer(serializers.ModelSerializer):
    core = serializers.SerializerMethodField(read_only=True)  
    core_value = serializers.SerializerMethodField(read_only=True)  
    paste = serializers.SerializerMethodField(read_only=True)  
    paste_value = serializers.SerializerMethodField(read_only=True)
    casing = serializers.SerializerMethodField(read_only=True)  
    casing_value = serializers.SerializerMethodField(read_only=True)    
    class Meta:
        model = FurnaceElectrode
        fields = '__all__'

    def get_core(self,obj):
        return getattr(obj.core, 'id', None)
    def get_core_value(self,obj):
        return getattr(obj.core, 'value', None)
    def get_paste(self,obj):
        return getattr(obj.paste, 'id', None)
    def get_paste_value(self,obj):
        return getattr(obj.paste, 'value', None)
    
    def get_casing(self,obj):
        return getattr(obj.casing, 'id', None)
    def get_casing_value(self,obj):
        return getattr(obj.casing, 'value', None)

        

class FurnaceProductSerializer(serializers.ModelSerializer):
    product_state_value =serializers.SerializerMethodField(read_only=True) 
    product_type_value =serializers.SerializerMethodField(read_only=True) 
    product_type=serializers.SerializerMethodField(read_only=True)
    product_state=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = FurnaceProduct
        fields = '__all__'

    def get_product_type(self,obj):
        return getattr(obj.product_type, 'id', None)
    def get_product_type_value(self,obj):
        return getattr(obj.product_type, 'value', None)
    def get_product_state_value(self,obj):
        return getattr(obj.product_state, 'value', None)
    def get_product_state(self,obj):
        return getattr(obj.product_state, 'id', None)



class ControlParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlParameter
        fields = '__all__'

class AdditivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additive
        fields = '__all__'

class FurnaceConfigStepSerializer(serializers.ModelSerializer):
    control_parameters = ControlParameterSerializer(many=True,read_only=True,source="furnace_control_params" )
    additives = AdditivesSerializer(many=True,read_only=True,source="furnace_additives")

    class Meta:
        model = FurnaceConfigStep
        fields = '__all__'


class FurnaceConfigSerializer(serializers.ModelSerializer):
    furnace_products = FurnaceProductSerializer(many=True, read_only=True,source="furnace_config_products")
    furnace_electrodes=FurnaceElectrodeSerializer(many=True,read_only=True,source="furnace_config_electrodes")
    step2=FurnaceConfigStepSerializer(many=True,read_only=True,source="furnace_config_step")
    workshop_value=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = FurnaceConfig
        fields = '__all__'
    def get_workshop_value(self,obj):
        print(obj,"work shop value in serializer")
        return obj.workshop.workshop_name
    

    def create(self, validated_data):
        print(validated_data,"validated data in serializer")
        furnace_config = FurnaceConfig.objects.create(**validated_data)
        return furnace_config
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        return super().to_representation(instance)




class CreateSuperAdminUserSerializer(serializers.Serializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    phone=serializers.CharField(required=True)
    email=serializers.EmailField(required=False)
    department=serializers.CharField(required=False)
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    plant_name=serializers.CharField(required=True)
    plant_id=serializers.CharField(required=True)
    area_code=serializers.CharField(required=True)
