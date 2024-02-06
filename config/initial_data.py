from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import IntegrityError
from rest_framework.views import APIView
from mes.users.models import User,Role,RolePermission
from rest_framework import status
from mes.users import serializers as se
from mes.utils.models import Master,Module,Function
from mes.unit.models import GlobalUnit
module_data=[
    'User Access Control',
    'Master Data',
    'Core Process',
    'Lab Analysis',
    'Reports',
    "System Admin",
    ]
function_data=[
(1, 'Users'),
(1, 'Roles'),
(2, 'Furnace Material Maintenance'),
(2, 'Additive Maintenance'),
(2, 'By Products'),
(2, 'WIP Maintenance'),
(2, 'Standard BOM'),
(2, 'Active Furnace List'),
(2, 'Customer Specifications'),
(3, 'Heat Maintenance'),
(3, 'Bin Content'),
(3, 'Production Schedule'),
(3, 'Silicon Grade Material Maintenance'),
(3, 'Silicon Grade Heat Maintenance'),
(4, 'Heat Analysis'),
(4, 'Ladle additive Analysis'),
(4, 'Ladle Product'),
(4, 'Furnace Mix & Fume Analysis'),
(4, ' Spout (Tap) Analysis'),
(4, 'Furnace Mix Lab Analysis'),
(5, 'Primary Heat Report'),
(5, 'Prod Schedule Analysis'),
(6,'Plant Configuration'),
(6,'Furnace Configuration')
]
master=[
    ('UNITSYSTEM',    'Metric System'),
    ('UNITSYSTEM',    'Imperial System'  ),
    ('CURRENCY',  'United States Dollar ($)' ),
    ('CURRENCY',  'Pound Sterling (£)'),
    ('CURRENCY',  'Euro (€)'),
    ('CURRENCY',  'Canadian Dollar (C$)'),
    ('CURRENCY',  'South African Rand (ZAR)'),
    ('CURRENCY',  'Argentine Peso (Arg$)'),
    ('CURRENCY',  'Norwegian Krone (NOK)'),
    ('CURRENCY',  'Venezuelan bolívar (Bs)'),
    ('CURRENCY',  'Chinese Yuan (¥)' ),
    ('LANGUAGE',  'English'),
    ('LANGUAGE',  'Spanish'),
    ('LANGUAGE',  'French'),
    ('TIMEZONE',  '(UTC - 05:00) Eastern Time (US & Canada)'),
    ('TIMEZONE',  '(UTC - 06:00) Central Time (US & Canada)'),
    ('TIMEZONE',  '(UTC - 07:00) Mountain Time (US & Canada)'),
    ('TIMEZONE',  '(UTC - 08:00) Pacific Time (US & Canada)'),
    ('TIMEZONE',  '(UTC + 01:00) Central European Time'),
    ('TIMEZONE',  '(UTC - 03:00) Argentina Time'),
    ('TIMEZONE',  '(UTC - 04:00) Venezuelan Standard Time'),
    ('TIMEZONE',  '(UTC + 08:00) China Standard Time'),
    ('PRODUCT',   'Silica Fume'),
    ('PRODUCT',   'Metallurgical Si'),
    ('PRODUCT',   'Si Fines/Hyperfines'),
    ('PRODUCT',   'Si Dross' ),
    ('PRODUCT',   'FeSi'),
    ('POWERDELIVERY', 'Arc'  ),
    ('ELECTRODES',    'Pre-Baked'),
    ('ELECTRODES',    'Soderberg'),
    ('ELECTRODES',    'Composite'),
    ('PRODUCTSTATE',  'Molten'   ),
    ('PRODUCTSTATE',  'WIP'),
    ('PRODUCTTYPE',   'FeSi' ),
    ('PRODUCTTYPE',   'Si'),
    ('PRODUCTCODE',   'FeSi_50_Molten'),
    ('PRODUCTCODE',   'FeSi_65_Molten'),
    ('PRODUCTCODE',   'FeSi_75_Molten'),
    ('SILICAFUMEDEFAULTMATERIAL', '4400689 - MMG1 50 lb Bag' ),
    ('SLAGPRODUCTDEFAULTMATERIAL',    '5501370 - SiMe Alloy Cast DOW Sinking Slag'),
    ('REMELT',    '4400061 - MgFeSi Off Grade Remelts'),
    ('SAND',  '3AA9 - Silica Sand' ),
    ('AI',    '3300001 - Aluminum'),
    ('LIME',  '3301824 - Dolomite Quicklime Fines' ),
    ('SLAG',  'D020 - Silicon Slag'  ),
    ('SKULL', '6605124 - Screen Visor Wire Skullgard HAT 8X17-1/2'),
    ('CORE',  '3300300 - Electrode 1146mm Yonvey'),
    ('PASTE', '3300300 - Electrode 1146mm Yonvey'),
    ('CASING',    '3300300 - Electrode 1146mm Yonvey'),
    ('WORKSHOPNO',    '1'),
    ('CONTROLPARAMETERS', 'Temp' ),
    ('CONTROLPARAMETERS', 'Time' ),
    ('CONTROLPARAMETERS', 'O2 Flow'  ),
    ('CONTROLPARAMETERS', 'Air Flow' ),
    ('CONTROLPARAMETERS', 'N Flow'),
    ('CONTROLPARAMETERS', 'O2 Pressure'),
    ('CONTROLPARAMETERS', 'Air Pressure' ),
    ('CONTROLPARAMETERS', 'N Pressure'   ),
    ('ADDITIVES', '3AA9 - Silica Sand'   ),
    ('ADDITIVES', 'RM39 - Sime Dust (Fines)' ),
    ('STEPS', 'Wait'),
    ('STEPS', 'Fill'),
    ('STEPS', 'Refine'),
    ('STEPS', 'Settle'),
    ('STEPS', 'Cast'),
    ('STEPS', 'De-slag'),
    ('STEPS', 'Purge')
 
]


units=[
    {
        "name":"Temp",
        "imperial":"⁰ F",
        "metric":"⁰C"
    },
    {
        "name":"Time",
        "imperial":"mins",
        "metric":"mins"
    },
    {
        "name":"O2 Flow",
        "imperial":"mins",
        "metric":"mins"
    },
    {
        "name":"Air Flow",
        "imperial":"mins",
        "metric":"mins"
    },
    {
        "name":"N Flow",
        "imperial":"mins",
        "metric":"mins"
    },
    {
       "name":" O2 Pressure",
        "imperial":"psi",
        "metric":"Pa"
    },
    {
        "name":"Air Pressure",
        "imperial":"psi",
        "metric":"Pa"
    },
    {
        "name": "N Pressure",
        "imperial":"psi",
        "metric":"Pa"
    },
    {
        "name":"Paste Mass/Length",
        "imperial":"lb/in",
        "metric":"kg/cm"
    },
    {
        "name":"Casing Mass/Length",
        "imperial":"lb/in",
        "metric":"kg/cm"
    },
    {
        "name":"Iron Losses",
        "imperial":"%",
        "metric":"%"
    },
    {
        "name":"Joule Losses Coefficient",
        "imperial":"%",
        "metric":"%"
    },
    {
        "name":"Default EPI Index",
        "imperial":"%",
        "metric":"%"
    },
    {
        "name":"Corrected Reactance Coefficient",
        "imperial":"%",
        "metric":"%"
    },
    {
        "name":"Design MW",
         "imperial":"hp",
        "metric":"MW"
    },
    {
        "name":"Silicon FC",
        "imperial":"%",
        "metric":"%"
    },
    {
        "name":"K SIC",
        "imperial":"%",
        "metric":"%"
    },
    {
        "name":"Shell Losses",
        "imperial":"%",
        "metric":"%"
    }
]
class CreateSuperUserView(APIView):
    def post(self,request):
        data=request.data
        for item in units:
            g_unit=GlobalUnit.objects.filter(name=item.get('name'))
            if not g_unit.exists():
                GlobalUnit.objects.create(**item)
        serializer=se.CreateSuperAdminUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data=serializer.data
            plant_id=data.pop('plant_id','')
            area_code=data.pop('area_code','')
            plant_name= data.pop('plant_name','')
            plant_count=Plant.objects.all().count()
            plant=Plant.objects.filter(plant_name__iexact=plant_name,plant_id__iexact=plant_id,area_code__iexact=area_code,)
            if not plant.exists() and plant_count<=0:
                Plant.objects.create(plant_name=plant_name,plant_id=plant_id,area_code=area_code,created_by=1)
            for item in master:
                existing_master=Master.objects.filter(category__iexact=item[0],value__iexact=item[1])
                if not existing_master:
                    Master.objects.create(category=item[0],value=item[1],record_status=True)
            for item in module_data:
                module=Module.objects.filter(module_name__iexact=item)
                if not module.exists():
                    Module.objects.create(module_name=item)
            for item in function_data:
                func=Function.objects.filter(function_name__iexact=item[1])
                if not func.exists():
                    Function.objects.create(module_id=item[0],function_name=item[1])
            role_name = request.data.get("role_name","SuperAdmin")
        existing_role = Role.objects.filter(role_name__iexact=role_name).first()
        role=existing_role
        if not existing_role:
            role = Role.objects.create(role_name=role_name, is_superuser=True,)
        user=User.objects.filter(username__iexact=data['username'])
        if not user.exists():
            plant_id=data.pop('plant_id','')
            area_code=data.pop('area_code','')
            plant_name= data.pop('plant_name','')
            user=User.objects.create_superuser(**data,roles=[role.id])
        else:
             user=user.first()
        for item in Function.objects.all():
            try:
                function=RolePermission.objects.filter(function_master_id=item.id)
                if item.module.module_name=='System Admin' and item.function_name=='Plant Configuration':
                    if not function.exists():
                        RolePermission.objects.create(
                                    function_master_id=item.id,
                                    role_id=role.id,
                                    view=True,
                                    create=True,
                                    edit=True,
                                    delete=True,
                                    created_by_id=user.id
                                )
            except Exception as e:
                return Response({"error":str(e)})
        return Response({"message":"SUccessFully Created"})
