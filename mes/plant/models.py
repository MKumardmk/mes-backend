from django.db import models

from django.utils.translation import gettext_lazy as _
from django.db import connection
from mes.utils.models import BaseModel,Module,Function
# Create your models here.

class Plant(BaseModel):
    plant_name=models.CharField(max_length=100,default="")
    plant_id=models.CharField(max_length=20,default="")
    area_code=models.CharField(max_length=20,default="")

    def __str__(self) -> str:
        return self.plant_name
    
class TimeZone(models.Model):
    module_name = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    record_status = models.BooleanField(default=True)
    created_by = models.IntegerField(default=0)
    modified_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    modified_at = models.DateTimeField(null=True, blank=True)
    @classmethod
    def time_zone_procedure(cls,p_master_category):
        with connection.cursor() as cursor:
            # Use CALL instead of SELECT
            cursor.execute('SELECT * FROM get_gbl_masterdata(%s)',[p_master_category])
            # Since the procedure doesn't return a result set, you can leave fetchall empty
            results = cursor.fetchall()   
            
        return results
    @classmethod
    def get_time_zone(self,p_master_category):
      return  self.objects.filter(module_name=p_master_category)
    


class Language(models.Model):



    @classmethod
    def language_procedure(cls,p_master_category):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM get_gbl_masterdata(%s)',[p_master_category])
            # If the stored procedure returns results, you can fetch them
            results = cursor.fetchall()

        return results

class Unit(models.Model):



    @classmethod
    def unit_procedure(cls,p_master_category):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM get_gbl_masterdata(%s)',[p_master_category])
            # If the stored procedure returns results, you can fetch them
            results = cursor.fetchall()

        return results

class Currency(models.Model):



    @classmethod
    def currency_procedure(cls,p_master_category):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM get_gbl_masterdata(%s)',[p_master_category])
            # If the stored procedure returns results, you can fetch them
            results = cursor.fetchall()

        return results

class Product(models.Model):


    @classmethod
    def Product_procedure(cls,p_master_category):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM get_gbl_masterdata(%s)',[p_master_category])
            # If the stored procedure returns results, you can fetch them
            results = cursor.fetchall()

        return results

# class Function(models.Model):
    
#     @classmethod
#     def function_procedure(cls,):
#         with connection.cursor() as cursor:
#             cursor.execute('SELECT * FROM get_function_module_data()')
#             # If the stored procedure returns results, you can fetch them
#             results = cursor.fetchall()

#         return results



class ERP(models.Model):
    name = models.CharField(_("ERP"), max_length=100)


class PlantConfig(BaseModel):
    plant_id=models.CharField(max_length=50,unique=True,null=True,blank=True)
    plant_name = models.CharField(_("plant_config_name"), max_length=100)
    area_code = models.CharField(_("plant_config_area_code"), max_length=100)
    plant_address = models.CharField(_("plant_config_address"), max_length=100)
    # timezone = models.ForeignKey(TimeZone, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("plant_config_language"))
    # language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    timezone_id = models.IntegerField(_("plant_config_language"), )
    language_id = models.IntegerField()
    unit_id = models.IntegerField()
    currency_id = models.IntegerField()
    shift1_from = models.CharField(_("plant_config_shift1_from"), max_length=100)
    shift1_to = models.CharField(_("plant_config_shift1_to"), max_length=100)
    shift2_from = models.CharField(_("plant_config_shift2_from"), max_length=100)
    shift2_to = models.CharField(_("plant_config_shift2_to"), max_length=100)
    shift3_from = models.CharField(_("plant_config_shift3_from"), max_length=100)
    shift3_to = models.CharField(_("plant_config_shift3_to"), max_length=100)
    created_by = models.CharField(_("plant_config_created_by"), max_length=100)
    modified_by = models.CharField(_("plant_config_modified_by"), max_length=100)


    @classmethod
    def plant_config_insert_procedure(cls,
    p_plant_id,
    p_plant_name ,
    p_area_code ,
    p_plant_address ,
    p_timezone_id ,
    p_language_id ,
    p_unit_id ,
    p_currency_id ,
    p_shift1_from ,
    p_shift1_to ,
    p_shift2_from ,
    p_shift2_to ,
    p_shift3_from ,
    p_shift3_to ,
    p_created_by ,
    p_modified_by ,
    p_products_json ,
    p_workshops_json,
    p_function_json 
):
        with connection.cursor() as cursor:
            cursor.execute('CALL insert_plant_configuration(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', [p_plant_id, p_plant_name ,
    p_area_code ,
    p_plant_address ,
    p_timezone_id ,
    p_language_id ,
    p_unit_id ,
    p_currency_id ,
    p_shift1_from ,
    p_shift1_to ,
    p_shift2_from ,
    p_shift2_to ,
    p_shift3_from ,
    p_shift3_to ,
    p_created_by ,
    p_modified_by ,
    p_products_json ,
    p_workshops_json,
    p_function_json])
            # If the stored procedure returns results, you can fetch them
            results = None

        return results
    
    @classmethod
    def plant_config_get_procedure(cls,p_plant_id):
        with connection.cursor() as cursor:
            # Use CALL instead of SELECT
            cursor.execute('SELECT * FROM get_plant_config_data(%s)',[p_plant_id])
            # Since the procedure doesn't return a result set, you can leave fetchall empty
            results = cursor.fetchall() 

        return results

    @classmethod
    def plant_config_update_procedure(cls,
    p_plant_id,
    p_plant_address ,
    p_language_id ,
    p_shift1_from ,
    p_shift1_to ,
    p_shift2_from ,
    p_shift2_to ,
    p_shift3_from ,
    p_shift3_to ,
    p_modified_by ,
    p_products_json ,
    p_workshops_json,
     p_function_json ):
        with connection.cursor() as cursor:
            cursor.execute('CALL update_plant_configuration(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', [
     p_plant_id,
    p_plant_address ,
    p_language_id ,
    p_shift1_from ,
    p_shift1_to ,
    p_shift2_from ,
    p_shift2_to ,
    p_shift3_from ,
    p_shift3_to ,
    p_modified_by ,
    p_products_json ,
    p_workshops_json,
     p_function_json ])
            # If the stored procedure returns results, you can fetch them
            results = None

        return results
    

class PlantConfigProduct(BaseModel):
    plant_config = models.ForeignKey(PlantConfig,related_name="plant_config_products", on_delete=models.CASCADE)
    product_id = models.IntegerField()
    
    class Meta:
        db_table = 'plant_config_product'

class PlantConfigWorkshop(BaseModel):
    plant_config = models.ForeignKey(PlantConfig,related_name="plant_config_workshops", on_delete=models.CASCADE)
    workshop_id = models.IntegerField(unique=True)
    workshop_name = models.CharField(max_length=500)
    

    class Meta:
        db_table = 'plant_config_workshop'

class PlantConfigFunction(BaseModel):
    plant_config = models.ForeignKey(PlantConfig,related_name="plant_config_function", on_delete=models.CASCADE,null=True,blank=True)
    module = models.ForeignKey(Module,related_name="plant_config_modules",on_delete=models.CASCADE)
    function = models.ForeignKey(Function,related_name="plant_config_functions",on_delete=models.CASCADE)

    class Meta:
        unique_together = ( 'module', 'function')
