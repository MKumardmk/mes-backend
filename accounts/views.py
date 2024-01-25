from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from . import models as account_model
from . import serializers as se


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
                print(user.is_active,"user is acitve")
                if  not user.is_active:
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
class RolesView(APIView):
    def get(self,request):
        return Response({"data"})
    def post(self,request):
        print(request.user,"userasd;lfkhjas;dlfkj")
        try:
            role_name = request.data.get("role_name")
            permission_list = request.data.get("permission_list",{})
            response = {}
            existing_role = account_model.Role.objects.filter(role_name__iexact=role_name).first()
            if existing_role:
                return Response({"message": "Role with the same name already exists"}, status=status.HTTP_400_BAD_REQUEST)
            role = account_model.Role.objects.create(role_name=role_name,created_by_id=1 )
            for module_name, functions_list in permission_list.items():
                for function, permissions in functions_list.items():
                    role_permission = account_model.RolePermission.objects.create(
                        function_id=permissions["id"],
                        role=role,
                        read=permissions["view"],
                        create=permissions["create"],
                        edit=permissions["edit"],
                        delete=permissions["delete"],
                    )
            # response["permission_list"] = get_permissions_list(role.id)
            response["role"] = se.RoleSerializer(role, context={"request": request}).data
            return Response(response, status=status.HTTP_200_OK)
        
        except IntegrityError as e:
            print("exception>>>>>>>", e)
            return Response({"error": "Role with the same name already exists...."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        try:
            role_name = request.data.get("role_name")
            role_id = request.data.get("role_id")
            permission_list = request.data.get("permission_list")
            is_superuser = request.data.get("is_superuser")
            response={}
            existing_role = account_model.Role.objects.exclude(pk=role_id).filter(role_name__iexact=role_name).first()
            if existing_role:
                return Response({"message": "Role with the same name already exists"}, status=status.HTTP_400_BAD_REQUEST)
            role = account_model.Role.objects.get(id=role_id)
            role.role_name = role_name
            role.modified_by_id=1
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
        except IntegrityError as e:
            return Response({"error": "Role with the same name already exists"}, status=status.HTTP_400_BAD_REQUEST)



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

    user_obj = account_model.User.objects.filter(roles__id=role_id, is_delete=False)
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
