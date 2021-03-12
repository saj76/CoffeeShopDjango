# Generated by Django 3.1.7 on 2021-03-09 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CoffeeShopTask', '0006_auto_20210309_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customization',
            name='options',
        ),
        migrations.CreateModel(
            name='CustomizationOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.CharField(max_length=50)),
                ('Customization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', related_query_name='options', to='CoffeeShopTask.customization')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='customization_options',
            field=models.ManyToManyField(related_name='orders', to='CoffeeShopTask.CustomizationOptions'),
        ),
    ]
