from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import connection
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

from django.contrib.auth.models import User
from app.master.models import Master
from utils.models import AuditModel,TimeStampModel
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
    modified_by = models.IntegerField(null=True)
    created_by = models.IntegerField()

    class Meta:
        abstract=True


class Plant(TimeStampModel):
    name=models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.name


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

class Function(models.Model):
    
    @classmethod
    def function_procedure(cls,):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM get_function_module_data()')
            # If the stored procedure returns results, you can fetch them
            results = cursor.fetchall()

        return results



class ERP(models.Model):
    name = models.CharField(_("ERP"), max_length=100)



class PlantConfig(models.Model):
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
    

class PlantConfigProduct(models.Model):
    plant_config = models.ForeignKey(PlantConfig,related_name="plant_config_products", on_delete=models.CASCADE)
    product_id = models.IntegerField()
    created_by = models.IntegerField()
    modified_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'plant_config_product'

class PlantConfigWorkshop(models.Model):
    plant_config = models.ForeignKey(PlantConfig,related_name="plant_config_workshops", on_delete=models.CASCADE)
    workshop_id = models.IntegerField(unique=True)
    workshop_name = models.CharField(max_length=500)
    created_by = models.IntegerField()
    modified_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'plant_config_workshop'

class PlantConfigFunction(models.Model):
    plant_config = models.ForeignKey(PlantConfig,related_name="plant_config_function", on_delete=models.CASCADE,null=True,blank=True)
    module_id = models.IntegerField()
    function_id = models.IntegerField()
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ( 'module_id', 'function_id')


class FurnaceConfig(models.Model):
    plant_id = models.CharField(max_length=50)
    furnace_no = models.CharField(max_length=50,unique=True)
    furnace_description = models.CharField(max_length=500)
    workshop = models.ForeignKey(PlantConfigWorkshop,related_name="plant_furnace_workshop",on_delete=models.CASCADE)
    power_delivery = models.ForeignKey(Master,related_name="furnace_master_power_delivery",on_delete=models.CASCADE,null=True)
    electrode_type = models.ForeignKey(Master,related_name="furnace_master_electrode_type",on_delete=models.CASCADE,null=True)
    iron_losses = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    joule_losses_coeffient = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    default_epi_index = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    corrected_reactance_coefficient = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    design_mv = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    silica_fume_default_material = models.ForeignKey(Master,related_name="furnace_master_smdm",on_delete=models.CASCADE,null=True)
    slag_product_default_material = models.ForeignKey(Master,related_name="furnace_master_spdm",on_delete=models.CASCADE,null=True)
    silicon_fc = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    k_sic = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    shell_losses = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    default_moisture = models.BooleanField(default=False)
    remelt = models.ForeignKey(Master,related_name="furnace_master_remelt",on_delete=models.CASCADE,null=True)
    sand = models.ForeignKey(Master,related_name="furnace_master_sand",on_delete=models.CASCADE,null=True)
    ai = models.ForeignKey(Master,related_name="furnace_master_ai",on_delete=models.CASCADE,null=True)
    lime = models.ForeignKey(Master,related_name="furnace_master_lime",on_delete=models.CASCADE,null=True)
    slag = models.ForeignKey(Master,related_name="furnace_master_slag",on_delete=models.CASCADE,null=True)
    skull = models.ForeignKey(Master,related_name="furnace_master_skull",on_delete=models.CASCADE,null=True)
    is_draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
    modified_by = models.IntegerField(null=True)
    created_by = models.IntegerField()
    record_status = models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)

class FurnaceProduct(models.Model):
    furnace_config = models.ForeignKey(FurnaceConfig,related_name="furnace_config_products",on_delete=models.CASCADE,null=True,blank=True)
    product_state = models.ForeignKey(Master,related_name="master_furnace_product_state",on_delete=models.CASCADE,null=True)
    product_type = models.ForeignKey(Master,related_name="master_furnace_product_type",on_delete=models.CASCADE,null=True)
    product_code = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
    modified_by = models.IntegerField(null=True)
    created_by = models.IntegerField()
    record_status = models.BooleanField(default=True)



class FurnaceElectrode(models.Model):
    furnace_config = models.ForeignKey(FurnaceConfig,related_name="furnace_config_electrodes",on_delete=models.CASCADE,null=True,blank=True)
    electrode_type_id = models.IntegerField(null=True)
    type_name = models.CharField(max_length=50)
    core = models.ForeignKey(Master,related_name="master_furnace_electrode",on_delete=models.CASCADE,null=True)
    core_mass_length = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    paste = models.ForeignKey(Master,related_name="master_electrode_paste",on_delete=models.CASCADE,null=True)
    paste_mass_length = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    casing = models.ForeignKey(Master,related_name="master_electrode_casing",on_delete=models.CASCADE,null=True)
    casing_mass_length = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
    modified_by = models.IntegerField(null=True)
    created_by = models.IntegerField()
    record_status = models.BooleanField(default=True)


class FurnaceConfigStep(models.Model):
    furnace=models.ForeignKey(FurnaceConfig,related_name="furnace_config_step",on_delete=models.CASCADE)
    step=models.CharField(max_length=10)
    order=models.SmallIntegerField()
    record_status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.step
    
    class Meta:
        ordering=['-order']

    def __str__(self) -> str:
        return self.step

class ControlParameter(models.Model):
    furnace_config_step=models.ForeignKey(FurnaceConfigStep,related_name="furnace_control_params",on_delete=models.CASCADE,null=True,blank=True)
    param=models.CharField(max_length=50)
    value=models.FloatField()
    is_mandatory=models.BooleanField(default=True)
    record_status = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.param
    
class Additives(models.Model):
    furnace_config_step=models.ForeignKey(FurnaceConfigStep,related_name="furnace_additives",on_delete=models.CASCADE,blank=True,null=True)
    material=models.CharField(max_length=50)
    quantity=models.FloatField()
    record_status = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.material
    

# class FurnaceProductType(models.Model):
#     name=models.CharField(max_length=50)

#     def __str__(self) -> str:
#         return self.name
    
# # class FurnaceProductCode(models.Model):
# #     code=models.CharField(max_length=50)
# #     def __str__(self) -> str:
# #         return self.code


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