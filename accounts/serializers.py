from rest_framework import serializers
from . import models

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RolePermission
        fields = '__all__'



class UserDetailSerializer(serializers.ModelSerializer[models.User]):
    user_roles = RoleSerializer(many=True, read_only=True, )
    user_permissions = RolePermissionSerializer(many=True, read_only=True,)

    class Meta:
        model=models.User
        fields=[
            "first_name",
            "last_name",
            "phone",
            "username",
            "is_active",
            "user_roles",  # Include user roles
            "user_permissions",
            # "is_superuser",
        ]



