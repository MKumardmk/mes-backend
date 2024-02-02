from rest_framework import serializers
from . import models
from django.db.models import Q

from .models import Function,Module
from . import models as user_model
from .utils import get_permission_union
from mes.users.models import User as UserType
from django.contrib.auth.hashers import make_password

class RolePermissionSerializer(serializers.ModelSerializer):
    # function_master = FunctionMasterSerializer(read_only=True)
    class Meta:
        model = models.RolePermission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    total_functions = serializers.SerializerMethodField("get_total_functions")
    total_users = serializers.SerializerMethodField("get_total_users")
    class Meta:
        model = models.Role
        fields = '__all__'

    def get_total_users(self, obj):
        active_user_count = models.User.objects.filter(roles=obj, is_delete=False).count()
        inactive_user_count = models.User.objects.filter(roles=obj, is_delete=True).count()
        return {"active_user_count": active_user_count, "inactive_user_count": inactive_user_count}

    def get_total_functions(self, obj):
        function_count = (
            models.RolePermission.objects.filter(role=obj)
            .filter(Q(view=True) | Q(create=True) | Q(edit=True) | Q(delete=True))
            .count()
        )
        return function_count
    
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
    roles = RoleSerializer(many=True, read_only=True)
    permission_list = serializers.SerializerMethodField("get_permission_list")

    class Meta:
        model=models.User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "phone",
            "roles",
            "email",
            "login_type",
            "is_delete",
            "permission_list",
            "department",
            "is_superuser",
        ]

    def get_permission_list(self, obj):
        role_list = []
        for role in obj.roles.all():
            role_list.append(role.id)
        permission_list = get_permission_union(role_list)
        print(permission_list)
        return permission_list

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields="__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        username=attrs.get('username','')
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



class CreateSuperAdminUserSerializer(serializers.Serializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    phone=serializers.CharField(required=True)
    email=serializers.EmailField(required=False)
    department=serializers.CharField(required=False)
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    plant_name=serializers.CharField(required=True)
    plant_id=serializers.CharField(required=True)
    area_code=serializers.CharField(required=True)




class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = user_model.User
        fields = "__all__"
        # fields = ["id", "first_name", "last_name", "url", "username"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserListSerializer(serializers.ModelSerializer[UserType]):
    roles = RoleSerializer(many=True, required=False)

    class Meta:
        model = user_model.User
        # fields = "__all__"
        fields = ["id", "first_name", "last_name", "url", "username", "roles", "is_delete", "email", "phone"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserDetailSerializer(serializers.ModelSerializer[UserType]):
    roles = RoleSerializer(many=True, required=False)
    permission_list = serializers.SerializerMethodField("get_permission_list")
    # is_superuser = serializers.SerializerMethodField("get_is_superuser")

    def get_permission_list(self, obj):
        role_list = []
        for role in obj.roles.all():
            role_list.append(role.id)

        permission_list = get_permission_union(role_list)
        return permission_list

    # def get_is_superuser(self, obj):
    #     is_superuser = False
    #     for role in obj.roles.all():
    #         if role.is_superuser == True:
    #             is_superuser = True
    #     return is_superuser

    class Meta:
        model = user_model.User
        # fields = "__all__"
        fields = [
            "id",
            "first_name",
            "last_name",
            "url",
            "username",
            "roles",
            "phone",
            "email",
            "is_delete",
            "permission_list",
            "is_superuser",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserCreateSerializer(serializers.ModelSerializer):
    # roles = RoleSerializer(many=True)

    def validate(self, attrs):
        password = make_password(attrs.get("password"))
        attrs["password"] = password
        return attrs

    """def create(self, validated_data):
        print ("create called>>>>>>>>>>>>>>>>>>>>>>>")
        password = make_password(validated_data.get('password'))
        validated_data["password"] = password
        return validated_data"""

    class Meta:
        model = user_model.User
        # fields = "__all__"
        fields = ["id", "first_name", "last_name", "username", "password", "roles", "email", "phone"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserUpdateSerializer(serializers.ModelSerializer[UserType]):
    """def validate(self, attrs):
    password = make_password(attrs.get("password"))
    attrs["password"] = password
    return attrs"""

    class Meta:
        model = user_model.User
        # fields = "__all__"
        fields = ["id", "first_name", "last_name", "url", "username", "roles", "is_delete", "phone", "email"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UpdatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model.User
        fields = ["name", "first_name", "last_name"]
