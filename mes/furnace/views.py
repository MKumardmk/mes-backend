from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from mes.furnace.models import FurnaceConfig,FurnaceElectrode,FurnaceProduct
from .serializers import FurnaceConfigSerializer
from rest_framework import status  
from django.http import Http404
from django.shortcuts import get_object_or_404    
from . import models as plant_model

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
        furnace_config=plant_model.FurnaceConfig.objects.create(workshop_id=workshop_id,**data)
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
  