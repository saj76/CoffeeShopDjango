# Generated by Django 3.1 on 2021-03-11 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CoffeeShopTask', '0007_auto_20210310_0106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customizationoptions',
            old_name='Customization',
            new_name='customization',
        ),
    ]