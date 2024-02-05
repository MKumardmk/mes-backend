from django.db import models

# Create your models here.
from mes.utils.models import BaseModel

class GlobalUnit(BaseModel):
    name=models.CharField(max_length=50)
    imperial=models.CharField(max_length=10)
    metric=models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.id