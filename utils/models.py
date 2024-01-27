from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class AuditModel(models.Model):
    created_by = models.ForeignKey("User", related_name="%(app_label)s_%(class)s_created_by", on_delete=models.CASCADE)
    modified_by = models.ForeignKey("User", related_name="%(app_label)s_%(class)s_modified_by", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
   
    class Meta:
        abstract=True

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
    class Meta:
        abstract=True



