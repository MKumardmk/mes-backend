# Generated by Django 5.0.1 on 2024-01-25 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_master_furnaceelectrode_core_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='additives',
            name='record_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='controlparameter',
            name='record_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='furnaceconfigstep',
            name='record_status',
            field=models.BooleanField(default=True),
        ),
    ]
