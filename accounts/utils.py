from .models import Role,Module,RolePermission,Function


def get_permissions_list(role_id=None, is_clone=False):
    module_list = Module.objects.all()
    module_dict = {}
    for module in module_list:
        function_dict = {}
        function_list = Function.objects.filter(module=module)
        permission_dict = {}
        for function in function_list:
            if role_id:
                role = Role.objects.get(id=role_id)
                try:
                    role_permission = RolePermission.objects.get(function=function, role=role)
                    if is_clone:
                        permission_dict = {
                            "view": role_permission.read,
                            "create": role_permission.create,
                            "edit": role_permission.edit,
                            "delete": role_permission.delete,
                            "id": function.id,
                        }

                    else:
                        permission_dict = {
                            "view": role_permission.read,
                            "create": role_permission.create,
                            "edit": role_permission.edit,
                            "delete": role_permission.delete,
                            "id": role_permission.id,
                        }

                    function_dict.update({role_permission.function.function_name: permission_dict})
                except RolePermission.DoesNotExist:
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
                permission_dict = {"view": True, "create": False, "edit": False, "delete": False, "id": function.id}
                function_dict.update({function.function_name: permission_dict})
        module_dict.update({module.module_name: function_dict})
    return module_dict
