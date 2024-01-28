from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import viewsets

from . import models as account_model
from . import serializers as se
from app.master import serializers as master_se
from app.master import models as master_models
from .utils import get_permissions_list

# Create your views here.
class SimpleUserLoginView(APIView):
    def post(self,request):
        data=request.data
        response={}
        username= data.get("username",'')
        password= data.get("password",'')
        if not username or not password:
            return Response({"message": "Username or password is empty"}, status=status.HTTP_400_BAD_REQUEST)
        try:
           user=account_model.User.objects.filter(username__iexact=username).first()
           user=authenticate(request=request,username=user.username,password=password)

           if user:
                if  user.is_delete:
                    response["message"] = "User is deactivated. Please contact admin"
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(response, status=status_code)
                token, created = Token.objects.get_or_create(user=user)
                
                status_code = status.HTTP_200_OK
                response["token"] = token.key
                serializer = se.UserDetailSerializer(user, context={"request": request})
                response["user"] = serializer.data
                response["message"] = "Login successfully"
                
                return Response(response, status=status_code)
           else:
               return Response({"message": "Password is not correct"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(str(e))
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

class SSOLoginView(APIView):
    def post(self,request,):
        return Response({"message":"Login Successfully using SSO "})
    

class DeactivateUser(APIView):
    def post(self,request,pk=None):
        user=account_model.User.objects.get(pk=pk)
        user.is_delete= not user.is_delete
        user.save()
        return Response({"message":f"User {"Deactivated" if  user.is_delete else "Activated"} SuccessFully"})
class RolesView(APIView):
    def get(self,request,pk=None):
        if pk:
            role=account_model.Role.objects.get(pk=pk)
            serializer=se.RoleSerializer(role)
            return Response({"result":serializer.data},status=status.HTTP_200_OK)
        roles=account_model.Role.objects.filter(record_status=True)
        serializer=se.RoleSerializer(roles,many=True)

        return Response({"results":serializer.data},status=status.HTTP_200_OK)
    def post(self,request):
        try:
            role_name = request.data.get("role_name")
            permission_list = request.data.get("permission_list",{})
            response = {}
            existing_role = account_model.Role.objects.filter(role_name__iexact=role_name).first()
            print(existing_role,"existing role")
            if existing_role:
                return Response({"message": "Role with the same name already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer= se.RoleSerializer(data=request.data,context={"request":request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message":"Role Added SuccessFully"})
            # role = account_model.Role.objects.create(role_name=role_name,created_by_id=1 )
            # for module_name, functions_list in permission_list.items():
            #     for function, permissions in functions_list.items():
            #         role_permission = account_model.RolePermission.objects.create(
            #             function_id=permissions["id"],
            #             role=role,
            #             read=permissions["view"],
            #             create=permissions["create"],
            #             edit=permissions["edit"],
            #             delete=permissions["delete"],
            #         )
            # # response["permission_list"] = get_permissions_list(role.id)
            # response["role"] = se.RoleSerializer(role, context={"request": request}).data
            return Response("response", status=status.HTTP_200_OK)
        
        except IntegrityError as e:
            print("exception>>>>>>>", e)
            return Response({"error": "Role with the same name already exists...."}, status=status.HTTP_400_BAD_REQUEST)

    # def put(self,request,pk=None):
    #     try:
    #         role_name = request.data.get("role_name")
    #         role_id = request.data.get("role_id")
    #         permission_list = request.data.get("permission_list")
    #         is_superuser = request.data.get("is_superuser")
    #         response={}
    #         existing_role = account_model.Role.objects.exclude(pk=role_id).filter(role_name__iexact=role_name).first()
    #         print(existing_role,"existing_role")
    #         if existing_role:
    #             return Response({"message": "Role with the same name already exists"}, status=status.HTTP_400_BAD_REQUEST)
    #         role = account_model.Role.objects.get(id=role_id)
    #         role.role_name = role_name
    #         role.modified_by_id=1
    #         # role.is_superuser = is_superuser
    #         role.save()
    #         for module_name, functions_list in permission_list.items():
    #             for function, permissions in functions_list.items():
    #                 role_permission = account_model.RolePermission.objects.get(id=permissions["id"])
    #                 role_permission.read = permissions["view"]
    #                 role_permission.create = permissions["create"]
    #                 role_permission.edit = permissions["edit"]
    #                 role_permission.delete = permissions["delete"]
    #                 role_permission.save()
    #         # response["permission_list"] = get_permissions_list(role.id)
    #         response["role"] = se.RoleSerializer(role, context={"request": request}).data
    #         return Response(response, status=status.HTTP_200_OK)
    #     except IntegrityError as e:
    #         return Response({"error": "Role with the same name already exists"}, status=status.HTTP_400_BAD_REQUEST)


class  UserView(APIView):
    def get(self,request,pk=None):
        if pk:
            user=account_model.User.objects.get(pk=pk)
            serializer=se.UserSerializer(user)
            return Response(serializer.data)
        users=account_model.User.objects.filter()
        serializer=se.UserSerializer(users,many=True)
        return Response({"results":serializer.data})
    def post(self,request,pk=None):
        serializer=se.UserSerializer(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            # user=account_model.User.objects.create_user(**data)
            return Response({"message":f'User {user.username} added SuccessFully'})
        
    def put(self,request,pk=None):
        data=request.data
        keys_to_remove = ['username', 'is_superuser', 'login_type']
        for key in keys_to_remove:
            data.pop(key, None)

        user=account_model.User.objects.filter(pk=pk).first()
        serializer=se.UserDetailSerializer(instance=user,data=data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"User Updated Successfully"})
        else :
            return Response({"message":serializer.errors})

@api_view(["POST"])
@permission_classes((AllowAny,))
def clone_role(request):
    role_name = request.data.get("role_name")
    role_id = request.data.get("role_id")
    permission_list = request.data.get("permission_list")
    response = {}
    role = account_model.Role.objects.get(id=role_id)
    role.role_name = role_name
    # role.is_superuser = is_superuser
    role.save()
    for module_name, functions_list in permission_list.items():
        for function, permissions in functions_list.items():
            role_permission = account_model.RolePermission.objects.get(id=permissions["id"])
            role_permission.read = permissions["view"]
            role_permission.create = permissions["create"]
            role_permission.edit = permissions["edit"]
            role_permission.delete = permissions["delete"]
            role_permission.save()
    # response["permission_list"] = get_permissions_list(role.id)
    response["role"] = se.RoleSerializer(role, context={"request": request}).data
    return Response(response, status=status.HTTP_200_OK)



@api_view(["POST"])
@permission_classes((AllowAny,))
def deactivate_role(request):
    role_id = request.data.get("role_id")
    response = {}
    try:
        role = account_model.Role.objects.get(id=role_id)
    except account_model.Role.DoesNotExist:
        return Response({"error": "Roles object not found"}, status=status.HTTP_404_NOT_FOUND)

    user_obj = account_model.User.objects.filter(role__id=role_id, is_delete=False)
    if user_obj:
        return Response({"error": "Users associated with this roles"}, status=status.HTTP_400_BAD_REQUEST)
    if role.is_delete == False:
        role_permissions = account_model.RolePermission.objects.filter(role=role)
        for permission in role_permissions:
            permission.is_delete = True
            permission.save()
        role.is_delete = True
        role.save()
        response["message"] = "Deactivated the Role"
    else:
        role_permissions = account_model.RolePermission.objects.filter(role=role)
        for permission in role_permissions:
            permission.is_delete = False
            permission.save()
        role.is_delete = False
        role.save()
        response["message"] = "Activated the Role"

    response["role"] = se.RoleSerializer(role, context={"request": request}).data
    return Response(response, status=status.HTTP_200_OK)



class FunctionViewSet(viewsets.ModelViewSet):
    queryset = master_models.FunctionMaster.objects.all()
    serializer_class = master_se.FunctionMasterSerializer

    def list(self, request, *args, **kwargs):
        response= super().list(request, *args, **kwargs)
        return response
    
    def create(self, request, *args, **kwargs):
        default_values = {
            'created_by': 1, 
        }
        data_with_defaults = {**request.data, **default_values}
        serializer = self.get_serializer(data=data_with_defaults)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    

from app.master.models import ModuleMaster
@api_view(['GET'])
def get_roles(request):
    data=[]
    module=ModuleMaster.objects.all()
    for i, item in enumerate(module):
        print(i)
        functions=item.module_functions.all()
        module_data={}
        module_data['id']=item.id
        module_data['module']=item.module_name
        module_data['functions']=[]
        for function in functions:
            module_data.get('functions').append({"id":function.id,"function_name":function.function_name})
            permissions=function.function_permissions.all()
            module_data['permissions']=[]
            for permission in permissions:
                permission_data={
                    "view":permission.view or False,
                    "create":permission.create or False,
                    "edit":permission.edit or False,
                    "delete":permission.delete or False,
                }
                module_data['permissions'].append(permission_data)
        data.append(module_data)
    return Response(data)

@api_view(["POST"])
@permission_classes((AllowAny,))
def get_permission_data(request):
    response = {}
    role_id = request.data.get("role_id")
    is_clone = request.data.get("is_clone", None)
    if role_id:
        role = account_model.Role.objects.get(id=role_id)
        response["role"] = se.RoleSerializer(role, context={"request": request}).data
    else:
        response["role"] = None
    permission_list = get_permissions_list(role_id, is_clone)
    response["permission_list"] = permission_list

    return Response(response, status=status.HTTP_200_OK)

