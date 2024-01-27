from rest_framework import serializers
from . import models

from app.master.models import FunctionMaster,ModuleMaster

class RoleSerializer(serializers.ModelSerializer):

    total_functions=serializers.SerializerMethodField()
    class Meta:
        model = models.Role
        fields = '__all__'
    def get_total_functions(self,obj):
        pass


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

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RolePermission
        fields = '__all__'



class UserDetailSerializer(serializers.ModelSerializer[models.User]):
    # user_roles = RoleSerializer(many=True, read_only=True, )
    # user_permissions = RolePermissionSerializer(many=True, read_only=True,)
    roles=RoleSerializer(many=True,read_only=True)

    class Meta:
        model=models.User
        exclude=['password','created_at','modified_at','row_guid','department','created_by','modified_by']
        # fields=[
        #     "first_name",
        #     "last_name",
        #     "username",
        #     "roles",
        #     "phone",
        #     "email",
        #     "is_active",
        #     "is_active",
        #     "is_superuser",
        # ]

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

