from rest_framework import serializers
from . import models
from django.db.models import Q

from app.master.models import FunctionMaster,ModuleMaster
from .utils import get_permission_union
class RolePermissionSerializer(serializers.ModelSerializer):
    # function_master = FunctionMasterSerializer(read_only=True)
    class Meta:
        model = models.RolePermission
        fields = '__all__'
class RoleSerializer(serializers.ModelSerializer):
    # total_functions = serializers.SerializerMethodField("get_total_functions")
    # total_users = serializers.SerializerMethodField("get_total_users")
    class Meta:
        model = models.Role
        fields = '__all__'
    # def get_total_users(self, obj):
    #     active_user_count = models.User.objects.filter(roles=obj, is_delete=False).count()
    #     inactive_user_count = models.User.objects.filter(roles=obj, is_delete=True).count()
    #     return {"active_user_count": active_user_count, "inactive_user_count": inactive_user_count}

    # def get_total_functions(self, obj):
    #     function_count = (
    #         models.RolePermission.objects.filter(role=obj)
    #         .filter(Q(view=True) | Q(create=True) | Q(edit=True) | Q(delete=True))
    #         .count()
    #     )
    #     return function_count
class RoleCreateSerializer(serializers.ModelSerializer):
    """permissions = serializers.SerializerMethodField("get_permissions")

    # @classmethod
    def get_permissions(self, obj):
        specs_new = create_permissions(obj)
        return specs_new"""

    class Meta:
        model = models.Role
        # fields = "__all__"
        fields = ["role_name", "url", "is_superuser"]

        extra_kwargs = {
            "url": {"view_name": "api:role-detail", "lookup_field": "pk"},
        }
    def create(self, validated_data):
        role = models.Role.objects.create(**validated_data )
        request=self.context.get('request',None)
        permission_list = request.data.get("permission_list")
        for  permissions in permission_list:
            models.RolePermission.objects.create(
                function_master_id=permissions.get('function_master_id'),
                role=role,
                view=permissions.get('view', False),
                create=permissions.get('create', False),
                edit=permissions.get('edit', False),
                created_by_id=1
                    )
        return role
class UserDetailSerializer(serializers.ModelSerializer[models.User]):
    role = RoleSerializer(many=True, read_only=True)
    permission_list = serializers.SerializerMethodField("get_permission_list")

    class Meta:
        model=models.User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "role",
            "phone",
            "email",
            "is_delete",
            "permission_list",
            "is_superuser",
        ]

    def get_permission_list(self, obj):
        role_list = []
        for role in obj.role.all():
            role_list.append(role.id)
        permission_list = get_permission_union(role_list)
        return permission_list

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields="__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        username=attrs.get('username','')
        print(username,"asdlkjashdflkjashdflkjhasdflkjh")
        if models.User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError({"username":"Username is already registered"})
        return super().validate(attrs)
    

    def create(self, validated_data):
        roles = self.context.get('request').data.get('role',[])
        print(validated_data,'validated_data')
        user = models.User.objects.create_user(**validated_data)
        # user.role.add(*roles)
        return user
    


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Function
        fields = '__all__'

