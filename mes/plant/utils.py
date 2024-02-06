
from mes.users.models import User,RolePermission

def set_first_user_permissions(plant_config,):
    user=User.objects.all()
    user_count=user.count()
    if user_count >1:
        return 
    
    functions=plant_config.plant_config_function.all()
    for item in functions:
        user=User.objects.first()
        role=user.roles.filter(role_name="SuperAdmin").first()
        role_permission=RolePermission.objects.filter(function_master_id=item.function.id).first()
        if not role_permission:
            RolePermission.objects.create(
                        function_master_id=item.function.id,
                        role_id=role.id,
                        view=True,
                        create=True,
                        edit=True,
                        delete=True,
                        created_by_id=user.id
                        )

       


    