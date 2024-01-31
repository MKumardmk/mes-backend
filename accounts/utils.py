from .models import Role,RolePermission
from app.master.models import FunctionMaster,ModuleMaster
from django.db.models import Q

def get_permissions_list(role_id=None, is_clone=False):
    module_list = ModuleMaster.objects.all()
    module_dict = {}
    for module in module_list:
        function_dict = {}
        function_list = FunctionMaster.objects.filter(module=module)
        permission_dict = {}
        for function in function_list:
            if role_id:
                role = Role.objects.get(id=role_id)
                try:
                    role_permission = RolePermission.objects.get(function_master=function, role=role)
                    if is_clone:
                        permission_dict = {
                            "view": role_permission.view,
                            "create": role_permission.create,
                            "edit": role_permission.edit,
                            "delete": role_permission.delete,
                            "id": function.id,
                        }

                    else:
                        permission_dict = {
                            "view": role_permission.view,
                            "create": role_permission.create,
                            "edit": role_permission.edit,
                            "delete": role_permission.delete,
                            "id": role_permission.id,
                        }

                    function_dict.update({role_permission.function_master.function_name: permission_dict})
                except RolePermission.DoesNotExist as e:
                    print(str(e))
                    # continue
                    permission_dict = {
                        "view": True,
                        "create": False,
                        "edit": False,
                        "delete": False,
                        "id": function.id,
                    }
                    function_dict.update({function.function_name: permission_dict})

            else:
                print("else called")
                permission_dict = {"view": True, "create": False, "edit": False, "delete": False, "id": function.id}
                function_dict.update({function.function_name: permission_dict})
            print(function_dict)
        module_dict.update({module.module_name: function_dict})
        # module_dict[module.module_name] =function_dict
    return module_dict




def get_user_permissions_list(role_list):
    print('get_user_permission_data')
    # import pudb
    # pudb.set_trace()
    module_list = ModuleMaster.objects.all()

    role_permission_list = []
    if role_list:
        
        for role_id in role_list:
            role_dict = {}
            role = Role.objects.get(id=role_id)
            module_dict = {}
            for module in module_list:
                function_dict = {}
                function_list = FunctionMaster.objects.filter(module=module)
                permission_dict = {}
                for function in function_list:
                    # function_dict = {}
                    role_permission = RolePermission.objects.get(Q(role=role),Q(function_master=function),)
                    permission_dict = {
                        "view": role_permission.view,
                        "create": role_permission.create,
                        "edit": role_permission.edit,
                        "delete": role_permission.delete,
                        # "id": role_permission.id,
                    }
                    print(permission_dict)
                    function_dict.update({role_permission.function_master.function_name: permission_dict})
                    # print(str(e),"error")
                    # # print(str(e),type(function),type(role))
                    # continue
                    # permission_dict = {"view": True, "create": False, "edit": False, "delete": False, "id": function.id}
                    # function_dict.update({function.function_name: permission_dict})

                module_dict.update({module.module_name: function_dict})
            role_dict.update({role.role_name: module_dict})
            # role_dict = {role.role_name: module_dict}
            role_permission_list.append(role_dict)
    # print(role_permission_list,'role_permission_list')
    return role_permission_list


def merge_with_priority(dict1, dict2):
    result = {}
    all_keys = set(dict1.keys()) | set(dict2.keys())

    for key in all_keys:
        value1 = dict1.get(key, {})
        value2 = dict2.get(key, {})

        if isinstance(value1, dict) and isinstance(value2, dict):
            result[key] = merge_with_priority(value1, value2)
        else:
            # Prioritize True values, if present in either dictionary
            result[key] = value1 if value1 is True else value2

    return result


def merge_with_priority_multiple(*dicts):
    user_dict = {}
    for user_permissions in dicts:
        for user_permission in user_permissions:
            for user, permissions in user_permission.items():
                if len(user_dict) == 0:
                    user_dict = permissions
                    continue
                for module, functions in permissions.items():
                    for key, function in functions.items():
                        for op_key, op_value in function.items():
                            if op_value:
                                user_dict[module][key][op_key] = op_value
    return user_dict


def get_permission_union(role_list):
    if not role_list:
        return {}

    users_permissions = get_user_permissions_list(role_list)


    merged_permissions = merge_with_priority_multiple(users_permissions)

    return merged_permissions


def get_user_permission_data(user=None):
    if user:
        roles=user.role.all()
        print(roles)
        module_list = ModuleMaster.objects.all()
        module_dict = {}
        for role in roles:
            role_permissions=role.role_permissions.all()
            for item in role_permissions:
                print(item.function_master,"item")
    
    return {}