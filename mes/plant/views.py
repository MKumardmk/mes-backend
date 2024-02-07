from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status 
from rest_framework.views import APIView
from .models import TimeZone,Language,Unit,Currency,Product,Function,ERP,PlantConfig,PlantConfigProduct,PlantConfigWorkshop,PlantConfigFunction
from mes.furnace.models import FurnaceConfig,FurnaceConfigStep,FurnaceElectrode,FurnaceProduct,ControlParameter,Additive
from .serializers import ERPSerializer,PlantConfigSerializer,FurnaceConfigSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404    
from . import serializers as se 
from . import models as plant_model
from django.db.models import Q
from mes.utils.models  import Module
from .utils import set_first_user_permissions
from mes.utils.serializers import ModuleSerializer


@api_view(["GET"])
@permission_classes((AllowAny,))
def time_zone_list(request):
    if request.method == "GET":
        res = TimeZone.get_time_zone('TIMEZONE')
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def language_list(request):
    if request.method == "GET":
        res = Language.language_procedure('LANGUAGE')
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def unit_list(request):
    if request.method == "GET":
        res = Unit.unit_procedure('UNITSYSTEM')
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def currency_list(request):
    if request.method == "GET":
        res = Currency.currency_procedure('CURRENCY')
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def product_list(request):
    if request.method == "GET":
        res = Product.Product_procedure('PRODUCT')
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def function_list(request):
    if request.method == "GET":
        res = Function.function_procedure()
        return Response(res)
class FunctionListView(APIView):
    def get(self,request,):
        data=Module.objects.filter(record_status=True)
        serializer=ModuleSerializer(data,many=True)
        return Response(serializer.data)
    
@api_view(["GET"])
@permission_classes((AllowAny,))
def erp_list(request):
    if request.method == "GET":
        res = ERP.objects.all()
        serializer = ERPSerializer(res, many = True)
        return Response(serializer.data)
    

class PlantConfigView(APIView):
    def get_object(self, pk):
        print(pk,"pk in plant config view")
        try:
            return PlantConfig.objects.get(plant_id=pk)
        except PlantConfig.DoesNotExist:
            raise Http404
    def get(self, request, pk=None):
        if pk:
            plant_config = self.get_object(pk=pk)
            serializer = PlantConfigSerializer(plant_config)
            return Response(serializer.data)
        else :
            return Response({"message":"The id of the plant is missing"},status=status.HTTP_404_NOT_FOUND)
        # else:
        #     plant_configs = PlantConfig.objects.all()
        #     serializer = PlantConfigSerializer(plant_configs, many=True)
    def post(self,request,):
        data= request.data
        print(data,"data")
        plant_config_products=data.pop('productName',[])
        plant_config_workshops=data.pop('workshops',[])
        function_json=data.pop('function',[])
        serializer = PlantConfigSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            plant_config=serializer.save()
            for plant_config_product in plant_config_products:
                print("plant_config_product")
                PlantConfigProduct.objects.create(plant_config=plant_config,**plant_config_product,created_by=1)
            for plant_config_workshop in plant_config_workshops:
                PlantConfigWorkshop.objects.create(plant_config=plant_config,**plant_config_workshop,created_by=1)
            for function in function_json:
                print(function,"print function")
                plant_model.PlantConfigFunction.objects.create(plant_config=plant_config,**function,created_by=1)
            response_data = {'message': 'Plant configuration successfully processed.'}
            set_first_user_permissions(plant_config)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            error_data = {'error': 'Invalid data provided.', 'errors': serializer.errors}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
   
    
    def put(self, request, pk=None):
        data=request.data
        plant_config_products=data.pop('productName')
        plant_config_workshops=data.pop('workshops')
        plant_functions=data.pop('function')
        plant_config = self.get_object(pk=pk)
        print(request.data['plant_name'])
        serializer = PlantConfigSerializer(plant_config, data=request.data,partial=True)
        if serializer.is_valid():
            plant_config=serializer.save()
            plant_product_ids=[]
            plant_function_ids=[]
            for plant_product in plant_config_products:
                pk_plant_product_id = plant_product.pop('id',None)
                if pk_plant_product_id:
                    PlantConfigProduct.objects.filter(pk=pk_plant_product_id,plant_config=plant_config).update(**plant_product)
                    product = PlantConfigProduct.objects.filter(pk=pk_plant_product_id,plant_config=plant_config).first()
                else:
                    product = PlantConfigProduct.objects.create(plant_config=plant_config,**plant_product,created_by=1)

                plant_product_ids.append(product.id)
            for plant_workshop in plant_config_workshops:
                pk_plant_workshop_id = plant_workshop.pop('id',None)
                workshop=FurnaceConfig.objects.filter(workshop_id=plant_workshop.get('workshop_id'))
                if workshop.exists():
                    plant_workshop.pop('record_status',None)
                plant_workshop.pop('is_deactivate',None)
                if pk_plant_workshop_id:
                    PlantConfigWorkshop.objects.filter(pk=pk_plant_workshop_id,plant_config=plant_config).update(**plant_workshop)
                else:
                    PlantConfigWorkshop.objects.create(plant_config=plant_config,**plant_workshop,created_by=1)

            for plant_function in plant_functions:
                pk_plant_function_id = plant_function.pop('id',None)
                if pk_plant_function_id:
                    PlantConfigFunction.objects.filter(pk=pk_plant_function_id,plant_config=plant_config).update(**plant_function)
                    functions = PlantConfigFunction.objects.filter(pk=pk_plant_function_id,plant_config=plant_config).first()
                else:
                    functions = plant_model.PlantConfigFunction.objects.create(plant_config=plant_config,**plant_function,created_by=1)

                plant_function_ids.append(functions.id)

            plant_model.PlantConfigProduct.objects.filter(plant_config=plant_config).exclude(id__in=plant_product_ids).delete()
            plant_model.PlantConfigFunction.objects.filter(plant_config=plant_config).exclude(id__in=plant_function_ids).delete()
            set_first_user_permissions(plant_config,)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        plant_config = self.get_object(pk=pk)
        print(plant_config,"plant config")
        plant_config.delete()
        return Response({"message": "Plant config deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
def change_key_names(d, key_mappings):
    return {key_mappings.get(k, k): v for k, v in d.items()}
    
class FurnaceConfigView(APIView):
    def get_object(self, pk):
        try:
            return FurnaceConfig.objects.get(plant_id=pk)
        except FurnaceConfig.DoesNotExist:
            raise Http404
    def get(self, request, pk=None):
        plant_id=request.query_params.get('plant_id',None)
        print(plant_id,"plant-id")
        if pk and plant_id:
            furnace_config = get_object_or_404(FurnaceConfig, plant_id=plant_id, pk=pk)
            serializer = FurnaceConfigSerializer(furnace_config)
        elif pk:
            furnace_config = get_object_or_404(FurnaceConfig, pk=pk)
            serializer = FurnaceConfigSerializer(furnace_config)
        elif plant_id:
            furnace_configs = FurnaceConfig.objects.filter(plant_id__istartswith=plant_id)
            print(furnace_configs,"furnace_config")
            serializer = FurnaceConfigSerializer(furnace_configs, many=True)
        else:return Response({"error": "Please provide the plant id "}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def post(self, request,plant_id=None, pk=None):
        data=request.data
        # print(request.data,"data in post furnace ")
        electrode_data_json=data.pop('electrodes')
        product_data_json=data.pop('products')
        key_mappings = {
        'type': 'type_name',
        'core': 'core_id',
        'coreMassLength': 'core_mass_length',
        'paste': 'paste_id',
        'pasteMassLength': 'paste_mass_length',
        'casing': 'casing_id',
        'casingMassLength': 'casing_mass_length'
}
        new_electrode_data_json = [change_key_names(item, key_mappings) for item in electrode_data_json]


        new_product_data_json = []

        for item in product_data_json:
            product_state = item['productState']['value']
            for product in item['products']:
                product_type = product['productType']['value']
                product_code = product['productCode']['value']
                new_item = {'product_state_id': product_state, 'product_type_id': product_type, 'product_code': product_code}
                new_product_data_json.append(new_item)
        workshop_id=data.pop('workshop',None)
        furnace_config=FurnaceConfig.objects.create(workshop_id=workshop_id,**data)
        for electrode_data_json in new_electrode_data_json:
            data_json = {}
            for key,value in electrode_data_json.items():
                if value  : data_json[key] = value
            FurnaceElectrode.objects.create(furnace_config=furnace_config,**data_json,created_by=1,electrode_type_id=data.get('electrode_type_id'))
        for furnace_product in new_product_data_json:
            FurnaceProduct.objects.create(furnace_config=furnace_config,**furnace_product,created_by=1)
        return Response({"message":"Furnace added Successfully","id":furnace_config.id}, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None, *args, **kwargs):
        data=request.data
        furnace_electrode_data=data.pop('electrodes')
        furnace_product_data=data.pop('products')
        furnace_config = FurnaceConfig.objects.get(pk=pk)
        serializer = FurnaceConfigSerializer(furnace_config, data=request.data)
        electrode_type_id=request.data.get('electrode_type_id',)
        print(electrode_type_id,"electrode_type_id")

        key_mappings = {
            'id':'id',
            'type': 'type_name',
            'core': 'core_id',
            'coreMassLength': 'core_mass_length',
            'paste': 'paste_id',
            'pasteMassLength': 'paste_mass_length',
            'casing': 'casing_id',
            'casingMassLength': 'casing_mass_length'
        }
        new_electrode_data_json = [change_key_names(item, key_mappings) for item in furnace_electrode_data]

        new_product_data_json = []

        for item in furnace_product_data:
            
            product_state = item['productState']['value']
            for product in item['products']:
                product_id = product.get('id', None)
                product_type = product['productType']['value']
                product_code = product['productCode']['value']
                record_status = product.get('record_status', True)
                new_item = {'id':product_id,'product_state_id': product_state, 'product_type_id': product_type, 'product_code': product_code, 'record_status':record_status}
                new_product_data_json.append(new_item)

        if serializer.is_valid():
            electrode_type_id=request.data.get('electrode_type_id',serializer.validated_data.get('electrode_type_id'))
            furnace_config=serializer.save()
            furnace_config.electrode_type_id=electrode_type_id
            furnace_config.save()
            for furnace_electrode in new_electrode_data_json:
                FurnaceElectrode.objects.filter(pk=furnace_electrode.pop('id'),furnace_config=furnace_config).update(**furnace_electrode)
            for product_data in new_product_data_json:
                if product_data.get('id',None):
                    FurnaceProduct.objects.filter(pk=product_data.pop('id'),furnace_config=furnace_config).update(**product_data)
                else:
                    FurnaceProduct.objects.create(furnace_config=furnace_config,**product_data,created_by=1)
            return Response({"message":"Furnace Details updated successfully",}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk=None):
        furnace_config = self.get_object(pk=pk)
        print(furnace_config,"plant config")
        furnace_config.delete()
        return Response({"message": "Plant config deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class FurnaceDeactivateView(APIView):
    def post(self,request,pk=None):
        furnace_config = get_object_or_404(FurnaceConfig, pk=pk)
        furnace_config.is_active = not furnace_config.is_active
        furnace_config.record_status=not furnace_config.record_status
        furnace_config.save()
        return Response({"message": f"Furnace is {'Activated' if furnace_config.is_active else 'Deactivated'} SuccessFully"})

class FurnaceConfigStepListAPIView(APIView):
    def post(self,request,furnace_id=None):
        print("called inside post inFurnaceConfigStepListAPIView ",request.data)
        data=request.data.get('step_data')

        output_data = []

        for item in data:
            transformed_item = {
                "control_parameters": [
                {
                "param": str(control_param['control_parameters']),
                "value": float(control_param['value']),
                "is_mandatory": control_param['isMandatory']
                }
                for control_param in item.get('controlParameters', [])
            ],
                "additives": [
                {
                "material": str(additive['material']),
                "quantity": float(additive['quantity'])
                }
                for additive in item.get('additives', [])
            ],
                "step": str(item['step'])
            }
            output_data.append(transformed_item)


        for index,item in enumerate(output_data,start=1):
          control_parameters=  item.pop('control_parameters', [])
          additives_data=item.pop('additives', [])
          furnace_config_step = FurnaceConfigStep.objects.create(furnace_id=furnace_id,order=index,**item)

          for control_param_data in control_parameters:
            # plant_model.ControlParameter.objects.create(furnace_config_step=furnace_config_step, **control_param_data)
            ControlParameter.objects.create(furnace_config_step=furnace_config_step, **control_param_data)
        for additive_data in additives_data:
            Additive.objects.create(furnace_config_step=furnace_config_step, **additive_data)
        return Response({"message":"Furnace Details added Successfully"}, status=201, )
    def get(self,request,furnace_id):
        data=FurnaceConfigStep.objects.filter(furnace_id=furnace_id)
        serializer=se.FurnaceConfigStepSerializer(data,many=True)
        return Response({"data":serializer.data})
    
    def put(self,request,furnace_id):
        data=request.data.get('step_data')

        output_data = []
        ids=[]
        for item in data:
            transformed_item = {
                "id":item.get('id', None),
                "order":item.get('order', None),
                "control_parameters": [
                {
                    "id":control_param.get('id', None),
                  
                "param": str(control_param['control_parameters']),
                "value": float(control_param['value']),
                "is_mandatory": control_param['isMandatory'],
                "record_status": control_param.get('record_status', True)
                }
                for control_param in item.get('controlParameters', [])
            ],
                "additives": [
                {
                    "id":additive.get('id', None),
                    
                "material": str(additive['material']),
                "quantity": float(additive['quantity']),
                "record_status": additive.get('record_status', True)
                }
                for additive in item.get('additives', [])
            ],
                "step": str(item['step'])
            }
            output_data.append(transformed_item)


        for index,item in enumerate(output_data,start=1):
            pk_id = item.get('id', None)
            print("item",item,pk_id)
            control_parameters=  item.pop('control_parameters', [])
            additives_data=item.pop('additives', [])
            print(type(pk_id))
            if pk_id:
                FurnaceConfigStep.objects.filter(Q(pk=pk_id), furnace_id=furnace_id).update( **item)
                furnace_config_step= FurnaceConfigStep.objects.filter(pk=pk_id).first()
            else:
                furnace_config_step = FurnaceConfigStep.objects.create(furnace_id=furnace_id,**item)
                print("else called")


            if furnace_config_step:ids.append(furnace_config_step.id)

            print(type(furnace_config_step),furnace_config_step,"test")

            for control_param_data in control_parameters:
                
                pk=control_param_data.pop('id', None)

                print("control_param_data",control_param_data)
                
                if pk:
                    ControlParameter.objects.filter(furnace_config_step=furnace_config_step, pk=pk).update(**control_param_data)
                else:
                    ControlParameter.objects.create(furnace_config_step=furnace_config_step, **control_param_data)
            for additive_data in additives_data:
                print(type(furnace_config_step))
                
                pk=additive_data.pop('id',None)
                
                if pk:
                    Additive.objects.filter(furnace_config_step=furnace_config_step,pk=pk).update(**additive_data)
                else:
                    Additive.objects.create(furnace_config_step=furnace_config_step, **additive_data)
        print(ids,"ids in put")
        FurnaceConfigStep.objects.filter(furnace_id=furnace_id).exclude(id__in=ids).delete()
        return Response({"message":"SuccessFully Updated"})
    def delete(self,request,furnace_id=None):
        try:
            furnace_step=FurnaceConfigStep.objects.filter(pk=furnace_id).first()
            furnace_step.delete()
        except AttributeError :
            pass
        return Response({"message":"Item Deleted SuccessFully",})

class FurnaceConfigChangeOrder(APIView):
    def post(self,request):
        data=request.data.get('data',[])
        for item in data:
            FurnaceConfigStep.objects.filter(pk=item.pop("id")).update(**item)
        return Response({"message":"Furnace Config Updated Successfully"})
