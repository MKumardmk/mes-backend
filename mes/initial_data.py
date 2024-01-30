from app.master.models import ModuleMaster,FunctionMaster
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User
from django.db import IntegrityError
module_data=[
    'User Control Access',
    'Master Data',
    'Core Process',
    'Lab Abalysis',
    'Reports'
    ]
function_data=[
(1, 'Users'),
(1,	'Roles'),
(2,	'Furnace Material Maintenance'),
(2,	'Additive Maintenance'),
(2,	'By Products'),
(2,	'WIP Maintenance'),
(2,	'Standard BOM'),
(2,	'Active Furnace List'),
(2,	'Customer Specification'),
(3,	'Heat Maintenance'),
(3,	'BIn Contents'),
(3,	'Production Schedule'),
(3,	'Silicon Grade Material Maintenance'),
(3,	'Silicon Grade Heat Maintenance'),
(4,	'Heat Analysis'),
(4,	'Ladle additive Analysis'),
(4,	'Ladle Product'),
(4,	'Furnace Mix & Fume Analysis'),
(4,	' Spout (Tap) Analysis'),
(4,	'Furnace Mix Lab Analysis'),
(5,	'Primary Heat Report'),
(5,	'Prod Schedule Analysis')
]

@api_view(['GET'])
def create_initial_data(request):
    for item in module_data:
        module=ModuleMaster.objects.filter(module_name__iexact=item)
        if not module.exists():
            ModuleMaster.objects.create(module_name=item)
    for item in function_data:
        func=FunctionMaster.objects.filter(function_name__iexact=item)
        if not func.exists():
            FunctionMaster.objects.create(module_id=item[0],function_name=item[1])
    # try:
    #     user=User.objects.create_user(username="mohan",password="123")
    # except IntegrityError:
    #     pass
    return Response({"message":"datas created Successfully"})
        