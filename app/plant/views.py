from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import TimeZone,Language,Unit,Currency,Product,Function,ERP,PlantConfig,FurnaceConfig,PlantConfigProduct,PlantConfigWorkshop,FurnaceElectrode,FurnaceProduct
from .serializers import TimeZoneSerializer,LanguageSerializer,UnitSerializer,CurrencySerializer,ProductSerializer,FunctionSerializer,ERPSerializer,PlantConfigSerializer,FurnaceConfigSerializer
from rest_framework import status ,viewsets ,generics 
import json
from datetime import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404    
from . import serializers as se 
from . import models as plant_model
from django.db.models import Q

@api_view(["GET"])
@permission_classes((AllowAny,))
def time_zone_list(request):
    if request.method == "GET":
        # res = TimeZone.time_zone_procedure('TIMEZONE')
        res = TimeZone.get_time_zone('TIMEZONE')
        # serializer = TimeZoneSerializer(res, many = True)
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def language_list(request):
    if request.method == "GET":
        res = Language.language_procedure('LANGUAGE')
        # serializer = LanguageSerializer(res, many = True)
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def unit_list(request):
    if request.method == "GET":
        res = Unit.unit_procedure('UNITSYSTEM')
        # serializer = UnitSerializer(res, many = True)
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def currency_list(request):
    if request.method == "GET":
        res = Currency.currency_procedure('CURRENCY')
        # serializer = CurrencySerializer(res, many = True)
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def product_list(request):
    if request.method == "GET":
        res = Product.Product_procedure('PRODUCT')
        # serializer = ProductSerializer(res, many = True)
        return Response(res)
    

@api_view(["GET"])
@permission_classes((AllowAny,))
def function_list(request):
    if request.method == "GET":
        res = Function.function_procedure()
        # serializer = FunctionSerializer(res, many = True)
        return Response(res)
    
@api_view(["GET"])
@permission_classes((AllowAny,))
def erp_list(request):
    if request.method == "GET":
        res = ERP.objects.all()
        serializer = ERPSerializer(res, many = True)
        return Response(serializer.data)
    
@api_view(["GET"])
@permission_classes((AllowAny,))
def plant_config_get(request):
    if request.method == "GET":
        print("calld get")
        res = PlantConfig.plant_config_get_procedure(1000)
        # serializer = PlantConfigSerializer(res, many = True)
        return Response(res)

@api_view(["POST"])
@permission_classes((AllowAny,))
def plant_config(request):
    if request.method == 'POST':
        data = request.data
        datas = {
            'plant_name': data.get('plantName', ''),
            'area_code': data.get('areaCode', ''),
            'plant_address': data.get('plantAddress', ''),
            'timezone_id': data.get('timeZone', ''),
            'language_id': data.get('language', ''),
            'unit_id': data.get('unitSystem', ''),
            'currency_id': data.get('currency', ''),
            'shift1_from': data.get('shift1', {}).get('from', ''),
            'shift1_to': data.get('shift1', {}).get('to', ''),
            'shift2_from': data.get('shift2', {}).get('from', ''),
            'shift2_to': data.get('shift2', {}).get('to', ''),
            'shift3_from': data.get('shift3', {}).get('from', ''),
            'shift3_to': data.get('shift3', {}).get('to', ''),
            'created_by': '10',
            'modified_by':  '10',
            'products_json': data.get('productName', []),
            'workshops_json': data.get('workshops', []),
            'function_json': data.get('function',[])
        }

        serializer = PlantConfigSerializer(data=datas)

        if serializer.is_valid():
            # Assuming PlantConfig.plant_config_insert_procedure() requires these arguments
            products_json = json.dumps(datas['products_json'])
            workshops_json = json.dumps(datas['workshops_json'])
            function_json = json.dumps(datas['function_json'])

    # Assuming PlantConfig.plant_config_insert_procedure() requires these arguments
            PlantConfig.plant_config_insert_procedure(
                1000,
            datas['plant_name'],
            datas['area_code'],
            datas['plant_address'],
            datas['timezone_id'],
            datas['language_id'],
            datas['unit_id'],
            datas['currency_id'],
            datetime.strptime(datas['shift1_from'], "%H:%M"),
            datetime.strptime(datas['shift1_to'], "%H:%M"),
            datetime.strptime(datas['shift2_from'], "%H:%M"),
            datetime.strptime(datas['shift2_to'], "%H:%M"),
            datetime.strptime(datas['shift3_from'], "%H:%M"),
            datetime.strptime(datas['shift3_to'], "%H:%M"),
            datas['created_by'],
            datas['modified_by'],
            products_json,
            workshops_json,
            function_json
        )

            response_data = {'message': 'Plant configuration successfully processed.'}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Return serializer errors in the response
            error_data = {'error': 'Invalid data provided.', 'errors': serializer.errors}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    # Handle the case when the request method is not POST
    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
    def post(self,request,pk=None):
        data= request.data
        plant_config_products=data.pop('products_json')
        plant_config_workshops=data.pop('workshops_json')
        function_json=data.pop('function_json')
        serializer = PlantConfigSerializer(data=data)
        if serializer.is_valid():
            plant_config=serializer.save()
            for plant_config_product in plant_config_products:
                PlantConfigProduct.objects.create(plant_config=plant_config,**plant_config_product,created_by=1)
            for plant_config_workshop in plant_config_workshops:
                PlantConfigWorkshop.objects.create(plant_config=plant_config,**plant_config_workshop,created_by=1)
            for function in function_json:
                plant_model.PlantConfigFunction.objects.create(plant_config=plant_config,**function,created_by=1)

            response_data = {'message': 'Plant configuration successfully processed.'}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            error_data = {'error': 'Invalid data provided.', 'errors': serializer.errors}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
   
    
    def put(self, request, pk=None):
        data=request.data
        plant_config_products=data.pop('products_json')
        plant_config_workshops=data.pop('workshops_json')
        plant_functions=data.pop('function_json')
        plant_config = self.get_object(pk=pk)
        print(request.data['plant_name'])
        serializer = PlantConfigSerializer(plant_config, data=request.data,partial=True)
        if serializer.is_valid():
            plant_config=serializer.save()
            for plant_product in plant_config_products:
                PlantConfigProduct.objects.filter(pk=plant_product.pop('id'),plant_config=plant_config).update(**plant_product)
            for plant_workshop in plant_config_workshops:
                PlantConfigWorkshop.objects.filter(pk=plant_workshop.pop('id'),plant_config=plant_config).update(**plant_workshop)
            for plant_function in plant_functions:
                PlantConfigWorkshop.objects.filter(pk=plant_workshop.pop('id'),plant_config=plant_config).update(**plant_function)
            
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
    def get(self, request,plant_id=None, pk=None):
        if pk and plant_id:
            furnace_config = get_object_or_404(FurnaceConfig, plant_id=plant_id, pk=pk)
            serializer = FurnaceConfigSerializer(furnace_config)
        elif pk:
            furnace_config = get_object_or_404(FurnaceConfig, pk=pk)
            serializer = FurnaceConfigSerializer(furnace_config)
        elif plant_id:
            furnace_configs = FurnaceConfig.objects.filter(plant_id=plant_id)
            serializer = FurnaceConfigSerializer(furnace_configs, many=True)
        else:return Response({"error": "Please provide the plant id "}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def post(self, request,plant_id=None, pk=None):
        data=request.data
        # print(request.data,"data in post furnace ")
        electrode_data_json=data.pop('electrodes')
        product_data_json=data.pop('products')
        # serializer = FurnaceConfigSerializer(data=request.data)
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
        # print(new_product_data_json,'new_product_data_json')
        # print(new_electrode_data_json,'new_electrode_data_json')
        # if serializer.is_valid():
        workshop_id=data.pop('workshop',None)
        furnace_config=plant_model.FurnaceConfig.objects.create(workshop_id=workshop_id,**data)
            # furnace_config = serializer.save(power_delivery_id=request.data['power_delivery_id'],electrode_type_)
        for electrode_data_json in new_electrode_data_json:
            data_json = {}
            for key,value in electrode_data_json.items():
                if value  : data_json[key] = value
            FurnaceElectrode.objects.create(furnace_config=furnace_config,**data_json,created_by=1,electrode_type_id=data.get('electrode_type_id'))
        for furnace_product in new_product_data_json:
            FurnaceProduct.objects.create(furnace_config=furnace_config,**furnace_product,created_by=1)
        return Response({"message":"Furnace added Successfully","id":furnace_config.id}, status=status.HTTP_201_CREATED)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk=None, *args, **kwargs):
        data=request.data
        furnace_electrode_data=data.pop('electrodes')
        furnace_product_data=data.pop('products')
        furnace_config = FurnaceConfig.objects.get(pk=pk)
        serializer = FurnaceConfigSerializer(furnace_config, data=request.data)

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
                id = product.get('id', None)
                product_type = product['productType']['value']
                product_code = product['productCode']['value']
                record_status = product.get('record_status', True)
                new_item = {'id':id,'product_state_id': product_state, 'product_type_id': product_type, 'product_code': product_code, 'record_status':record_status}
                new_product_data_json.append(new_item)

        if serializer.is_valid():
            furnace_config=serializer.save()
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
        is_active=request.data.get('is_active',True)
        furnace_config = get_object_or_404(FurnaceConfig, pk=pk)
        furnace_config.is_active = not furnace_config.is_active
        furnace_config.save()
        return Response({"message": f"Furnace is {'Activated' if furnace_config.is_active else 'Deactivated'} SuccessFully"})

# class FurnaceProductDeactivateView(APIView):
#     def post(self,request,pk=None):
#         is_active=request.data.get('is_active',True)
#         furnace_config = get_object_or_404(FurnaceConfigPr, pk=pk)
#         furnace_config.is_active = not furnace_config.is_active
#         furnace_config.save()
#         return Response({"message": f"Furnace is {'Activated' if furnace_config.is_active else 'Deactivated'} SuccessFully"})
class FurnaceConfigStepListAPIView(APIView):
    def post(self,request,furnace_id=None):
        print("called inside post inFurnaceConfigStepListAPIView ",request.data)
        data=request.data.get('step_data')
        # furnace_id = self.kwargs.get('furnace_id')

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
          furnace_config_step = plant_model.FurnaceConfigStep.objects.create(furnace_id=furnace_id,order=index,**item)

          for control_param_data in control_parameters:
            # plant_model.ControlParameter.objects.create(furnace_config_step=furnace_config_step, **control_param_data)
            plant_model.ControlParameter.objects.create(furnace_config_step=furnace_config_step, **control_param_data)
        for additive_data in additives_data:
            plant_model.Additives.objects.create(furnace_config_step=furnace_config_step, **additive_data)
        return Response({"message":"Furnace Details added Successfully"}, status=201, )
    def get(self,request,furnace_id):
        data=plant_model.FurnaceConfigStep.objects.filter(furnace_id=furnace_id)
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
            #   order = item.pop('order', 0)
            control_parameters=  item.pop('control_parameters', [])
            additives_data=item.pop('additives', [])
            print(type(pk_id))
            if pk_id:
                furnace_config_step = plant_model.FurnaceConfigStep.objects.filter(Q(pk=pk_id), furnace_id=furnace_id).update( **item)
                furnace_config_step= plant_model.FurnaceConfigStep.objects.filter(pk=pk_id).first()
            else:
                furnace_config_step = plant_model.FurnaceConfigStep.objects.create(furnace_id=furnace_id,**item)
                print("else called")


            if furnace_config_step:ids.append(furnace_config_step.id)

            print(type(furnace_config_step),furnace_config_step,"test")

            for control_param_data in control_parameters:
                
                id=control_param_data.pop('id', None)

                print("control_param_data",control_param_data)
                
                if id:
                    plant_model.ControlParameter.objects.filter(furnace_config_step=furnace_config_step, pk=id).update(**control_param_data)
                else:
                    plant_model.ControlParameter.objects.create(furnace_config_step=furnace_config_step, **control_param_data)
            for additive_data in additives_data:
                print(type(furnace_config_step))
                
                id=additive_data.pop('id',None)
                
                if id:
                    plant_model.Additives.objects.filter(furnace_config_step=furnace_config_step,pk=id).update(**additive_data)
                else:
                    plant_model.Additives.objects.create(furnace_config_step=furnace_config_step, **additive_data)
        print(ids,"ids in put")
        plant_model.FurnaceConfigStep.objects.filter(furnace_id=furnace_id).exclude(id__in=ids).delete()
        return Response({"message":"SuccessFully Updated"})
    def delete(self,request,furnace_id=None):
        try:
            furnace_step=plant_model.FurnaceConfigStep.objects.filter(pk=furnace_id).first()
            furnace_step.delete()
        except AttributeError :
            pass
        return Response({"message":"Item Deleted SuccessFully",})
# class FurnaceConfigStepListAPIView(generics.ListCreateAPIView):
#     serializer_class = se.FurnaceConfigStepSerializer

#     def create(self, request, *args, **kwargs):
#         furnace_id = self.kwargs.get('furnace_id')
#         request.data['furnace']=furnace_id
#         data=request.data['step_data']
#         # for item in data:
#         serializer = self.get_serializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response({"message":"Furnace Details added Successfully"}, status=201, headers=headers)
#     def get_queryset(self):
#         furnace_id = self.kwargs.get('furnace_id')
#         queryset = plant_model.FurnaceConfigStep.objects.filter(furnace_id=furnace_id)
#         return queryset
    
# class FurnaceConfigStepDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = plant_model.FurnaceConfigStep.objects.all()
#     serializer_class = se.FurnaceConfigStepSerializer
#     permission_classes= [AllowAny]

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response({"message": "Item delete SuccessFully"}, status=status.HTTP_204_NO_CONTENT)

class FurnaceConfigChangeOrder(APIView):
    def post(self,request):
        data=request.data.get('data',[])
        for item in data:
            furnace_step=plant_model.FurnaceConfigStep.objects.filter(pk=item.pop("id")).update(**item)
        return Response({"message":"Furnace Config Updated Successfully"})


@api_view(["PUT"])
@permission_classes((AllowAny,))
def plant_config_update(request):
    if request.method == 'PUT':
        try:
            plant_instance = PlantConfig.plant_config_get_procedure(1000)
        except PlantConfig.DoesNotExist:
            return Response({"error": "Plant not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        
        datas = {
            'plant_name': data.get('plantName', ''),
            'area_code': data.get('areaCode', ''),
            'plant_address': data.get('plantAddress', ''),
            'timezone_id': data.get('timeZone', ''),
            'language_id': data.get('language', ''),
            'unit_id': data.get('unitSystem', ''),
            'currency_id': data.get('currency', ''),
            'shift1_from': data.get('shift1', {}).get('from', ''),
            'shift1_to': data.get('shift1', {}).get('to', ''),
            'shift2_from': data.get('shift2', {}).get('from', ''),
            'shift2_to': data.get('shift2', {}).get('to', ''),
            'shift3_from': data.get('shift3', {}).get('from', ''),
            'shift3_to': data.get('shift3', {}).get('to', ''),
            'created_by': '10',
            'modified_by':  '10',
            'products_json': data.get('productName', []),
            'workshops_json': data.get('workshops', []),
            'function_json': data.get('function',[])
        }
        
        serializer = PlantConfigSerializer(data=datas)

        if serializer.is_valid():
              # Assuming PlantConfig.plant_config_insert_procedure() requires these arguments
            products_json = json.dumps(datas['products_json'])
            workshops_json = json.dumps(datas['workshops_json'])
            function_json = json.dumps(datas['function_json'])

    # Assuming PlantConfig.plant_config_insert_procedure() requires these arguments
            PlantConfig.plant_config_update_procedure(
                1000,
            datas['plant_address'],
            datas['language_id'],
            datetime.strptime(datas['shift1_from'], "%H:%M"),
            datetime.strptime(datas['shift1_to'], "%H:%M"),
            datetime.strptime(datas['shift2_from'], "%H:%M"),
            datetime.strptime(datas['shift2_to'], "%H:%M"),
            datetime.strptime(datas['shift3_from'], "%H:%M"),
            datetime.strptime(datas['shift3_to'], "%H:%M"),
            datas['modified_by'],
            products_json,
            workshops_json,
            function_json
            )

            response_data = {'message': 'Plant configuration modified successfully.'}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Unsupported method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    