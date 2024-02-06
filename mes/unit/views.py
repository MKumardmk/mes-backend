from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import UnitSerializer

from .models import GlobalUnit
# Create your views here.
class UnitViewSet(ModelViewSet):
    serializer_class=UnitSerializer
    queryset=GlobalUnit.objects.all()