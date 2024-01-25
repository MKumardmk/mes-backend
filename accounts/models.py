from typing import Any
import uuid
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.translation import gettext_lazy as _


from utils.models import AuditModel

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username: str, password: str = None, **extra_fields):
        # extra_fields.setdefault("is_staff", False)
        # extra_fields.setdefault("is_superuser", False)
        user=self.model(username=username,**extra_fields)
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        return self.create_user( username, password, **extra_fields)

class Module(AuditModel):
    module_name = models.CharField(_("Module Name"), null=True, blank=True,max_length=255)
    def __str__(self):
        return self.module_name
    

class User(AbstractBaseUser):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    email=models.EmailField(null=True,blank=True)
    department=models.CharField(max_length=50,null=True,blank=True)
    login_type=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True,verbose_name=_("UserName"))
    is_active=models.BooleanField(default=True)
    record_status=models.BooleanField(default=True)
    created_by=models.IntegerField(null=True,blank=True)
    modified_by=models.IntegerField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now_add=True)
    row_guid=models.UUIDField(default=uuid.uuid4, editable=False)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]   

    objects=UserManager()


class PlantUser(models.Model):
    plant=models.CharField(max_length=20)
    user=models.ForeignKey("User",on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.id
    
# class UserRole():
#     plant_user=models.ForeignKey(PlantUser,on_delete=models.CASCADE)
#     role=models.ForeignKey(PlantUser,on_delete=models.CASCADE)
class Function(AuditModel):
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING, null=True, blank=True)
    function_name = models.CharField(_("Name of Role"), max_length=100)
    description = models.TextField(_("Description"), null=True, blank=True)

    def __str__(self):
        return self.function_name
    

class Role(models.Model):
    role_name = models.CharField(verbose_name=_("Name of Role"), blank=True, max_length=255)
    created_by=models.ForeignKey(User,related_name="role_created_by",on_delete=models.CASCADE)
    modified_by=models.ForeignKey(User,related_name="role_modified_by",on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    record_status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.role_name


class RolePermission(models.Model):
    role=models.ForeignKey(Role,related_name="role_permissions",on_delete=models.CASCADE)
    plant_id=models.CharField(max_length=10)
    function=models.CharField(max_length=255)
    create=models.CharField(max_length=50)
    edit=models.CharField(max_length=50)
    delete=models.CharField(max_length=50)
    created_by=models.ForeignKey(User,related_name="permission_created_by",on_delete=models.CASCADE)
    modified_by=models.ForeignKey(User,related_name="permission_modified_by",on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    record_status = models.BooleanField(default=True)
    

    def __str__(self) -> str:
        return self.function
