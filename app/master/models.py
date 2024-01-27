from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import connection


from app.utils.models import TimeStampModel


class Master(models.Model):
    category =  models.CharField(_("master_category"), max_length=100)
    value = models.CharField(_("value"), max_length=100)
    description = models.TextField()
    recordStatus = models.BooleanField()


    def __str__(self) -> str:
        return self.id



    @classmethod
    def master_procedure(cls,p_master_category):
        with connection.cursor() as cursor:
            # Use CALL instead of SELECT
            cursor.execute('SELECT * FROM get_gbl_masterdata(%s)',[p_master_category])
            # Since the procedure doesn't return a result set, you can leave fetchall empty
            results = cursor.fetchall()   
            
        return results
    

class ModuleMaster(TimeStampModel):
    module_name=models.CharField(max_length=255)
    description = models.TextField(null=True)
    record_status = models.BooleanField(default=True)

    def __str__(self):
        return self.module_name
    

class FunctionMaster(TimeStampModel):
    module = models.ForeignKey(ModuleMaster,related_name="module_functions",max_length=255, null=False,on_delete=models.CASCADE)
    function_name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    record_status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.function_name