from rest_framework import serializers
from .models import TimeZone,Language,Unit,Currency,Product,Function,ERP,PlantConfig, PlantConfigProduct, PlantConfigWorkshop,FurnaceConfig,FurnaceProduct,PlantConfigFunction
from . import models as m

from app.master.serializers import MasterSerializer


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
    # def to_internal_value(self, data):
    #     # data['created_by'] = self.context['request'].user
    #     data['created_by'] = self.context['request'].user
    #     return super().to_internal_value(data)

class PlantConfigWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantConfigWorkshop
        fields = '__all__'

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
        print(validated_data,"validated data")
       

        plant_config= PlantConfig.objects.create(**validated_data)

       
        return plant_config
    
    # def update(self, instance, validated_data):
        # plant_config_products=validated_data.pop('')
        # plant_config_workshops=validated_data.pop('')
        # for plant_config_product in plant_config_products:
        #     id = plant_config_product.get('id',None)
        #     if id:
        #         config_product=PlantConfigProduct.objects.get(pk=id)
        #         config_product.plant_config=instance
        #         config_product.save()

        # for plant_config_workshop in plant_config_workshops:
        #     id = plant_config_workshop.get('id',None)
        #     if id:
        #         config_work_shop=PlantConfigWorkshop.objects.get(pk=id)
        #         config_work_shop.plant_config=instance
                # config_work_shop.save()
        # instance.save()
        # return instance
    




class ERPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ERP
        fields = '__all__'







# class PlantFunctionMasterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PlantFunctionMaster
#         fields = '__all__'


class FurnaceElectrodeSerializer(serializers.ModelSerializer):
    core = serializers.SerializerMethodField(read_only=True)  
    core_value = serializers.SerializerMethodField(read_only=True)  
    paste = serializers.SerializerMethodField(read_only=True)  
    paste_value = serializers.SerializerMethodField(read_only=True)
    casing = serializers.SerializerMethodField(read_only=True)  
    casing_value = serializers.SerializerMethodField(read_only=True)    
    class Meta:
        model = m.FurnaceElectrode
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
    # product_type = MasterSerializer(read_only=True,many=True,source="master_furnace_product_type")  
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
        model = m.ControlParameter
        fields = '__all__'

class AdditivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Additives
        fields = '__all__'

class FurnaceConfigStepSerializer(serializers.ModelSerializer):
    control_parameters = ControlParameterSerializer(many=True,read_only=True,source="furnace_control_params" )
    additives = AdditivesSerializer(many=True,read_only=True,source="furnace_additives")

    class Meta:
        model = m.FurnaceConfigStep
        fields = '__all__'
    def create(self, validated_data):
        data = self.context.get('request').data.get('step_data',[])
        print(data)
        # print(data,"daasdfasd;lfkj")
        # control_parameters_data = data.get('control_parameters', [])
        # additives_data = data.get('additives', [])
        # furnace_data=data.get('step_data',[])

        # furnace_config_step = m.FurnaceConfigStep.objects.create(furnace_data)
        # for control_param_data in control_parameters_data:
        #     m.ControlParameter.objects.create(furnace_config_step=furnace_config_step, **control_param_data)
        # for additive_data in additives_data:
        #     m.Additives.objects.create(furnace_config_step=furnace_config_step, **additive_data)
        # return furnace_config_step
        return ""


class FurnaceConfigSerializer(serializers.ModelSerializer):
    furnace_products = FurnaceProductSerializer(many=True, read_only=True,source="furnace_config_products")
    furnace_electrodes=FurnaceElectrodeSerializer(many=True,read_only=True,source="furnace_config_electrodes")
    step2=FurnaceConfigStepSerializer(many=True,read_only=True,source="furnace_config_step")
    workshop_value=serializers.SerializerMethodField(read_only=True)
    # power_delivery=serializers.SerializerMethodField(read_only=True,source="furnace_master_power_delivery")
    # power_delivery_value=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = FurnaceConfig
        fields = '__all__'
    def get_workshop_value(self,obj):
        print(obj,"work shop value in serializer")
        return obj.workshop.workshop_name
    # def get_power_delivery(self,obj):
    #     return obj.power_delivery.id
    # def get_power_delivery_value(self,obj):
    #     return obj.power_delivery.value
    

    def create(self, validated_data):
        print(validated_data,"validated data in serializer")
        furnace_config = FurnaceConfig.objects.create(**validated_data)
        return furnace_config
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        return super().to_representation(instance)


class FunctionMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.FunctionMaster
        fields = ['id', 'module', 'function_name', 'description', 'record_status', 'created_at', 'modified_at']
        read_only_fields = ['id', 'created_at', 'modified_at']

class ModuleMasterSerializer(serializers.ModelSerializer):
    module_functions = FunctionMasterSerializer(many=True, read_only=True)
    class Meta:
        model = m.ModuleMaster
        fields = ['id', 'module_name', 'description', 'record_status','module_functions', 'created_at', 'modified_at']
        read_only_fields = ['id', 'created_at', 'modified_at']


