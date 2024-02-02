from django.db import models
from mes.plant.models import PlantConfigWorkshop
from mes.utils.models import Master,BaseModel

class FurnaceConfig(BaseModel):
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

class FurnaceProduct(BaseModel):
    furnace_config = models.ForeignKey(FurnaceConfig,related_name="furnace_config_products",on_delete=models.CASCADE,null=True,blank=True)
    product_state = models.ForeignKey(Master,related_name="master_furnace_product_state",on_delete=models.CASCADE,null=True)
    product_type = models.ForeignKey(Master,related_name="master_furnace_product_type",on_delete=models.CASCADE,null=True)
    product_code = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
    modified_by = models.IntegerField(null=True)
    created_by = models.IntegerField()
    record_status = models.BooleanField(default=True)



class FurnaceElectrode(BaseModel):
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


class FurnaceConfigStep(BaseModel):
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

class ControlParameter(BaseModel):
    furnace_config_step=models.ForeignKey(FurnaceConfigStep,related_name="furnace_control_params",on_delete=models.CASCADE,null=True,blank=True)
    param=models.CharField(max_length=50)
    value=models.FloatField()
    is_mandatory=models.BooleanField(default=True)
    record_status = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.param
    
class Additive(BaseModel):
    furnace_config_step=models.ForeignKey(FurnaceConfigStep,related_name="furnace_additives",on_delete=models.CASCADE,blank=True,null=True)
    material=models.CharField(max_length=50)
    quantity=models.FloatField()
    record_status = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.material