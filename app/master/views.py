from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Master
from .serializers import MasterSerializer
from rest_framework.views import APIView

@api_view(["GET"])
@permission_classes((AllowAny,))
def master_list(request):
    if request.method == "GET":
        categories = ['TIMEZONE','LANGUAGE','UNITSYSTEM','CURRENCY','PRODUCT','POWERDELIVERY','ELECTRODES','PRODUCTSTATE','PRODUCTTYPE','PRODUCTCODE','SILICAFUMEDEFAULTMATERIAL', 'SLAGPRODUCTDEFAULTMATERIAL','REMELT', 'SAND', 'AI', 'LIME', 'SLAG', 'SKULL','CORE','PASTE','CASING']

        array = []
        for category in categories:
            res = Master.master_procedure(category)

            for i in res:
                array.append(i)
        # serializer = MasterSerializer(res, many = True)
        return Response(array)
    
class MasterListView(APIView):
    
    def get(self,request):
     categories = ['TIMEZONE','LANGUAGE','UNITSYSTEM','CURRENCY','PRODUCT','STEPS','ADDITIVES','CONTROLPARAMETERS','WORKSHOPNO','POWERDELIVERY','ELECTRODES','PRODUCTSTATE','PRODUCTTYPE','PRODUCTCODE','SILICAFUMEDEFAULTMATERIAL', 'SLAGPRODUCTDEFAULTMATERIAL','REMELT', 'SAND', 'AI', 'LIME', 'SLAG', 'SKULL','CORE','PASTE','CASING']
     array = []
     for category in categories:
         data= Master.objects.filter(category = category)
         serializer=MasterSerializer(data,many = True)
         array.extend(serializer.data)

     return Response(array)
    