# Generated by Django 5.0.1 on 2024-01-25 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_design_mv_furnaceconfig_design_mw'),
    ]

    operations = [
        migrations.RenameField(
            model_name='furnaceconfig',
            old_name='design_mw',
            new_name='design_mv',
        ),
    ]