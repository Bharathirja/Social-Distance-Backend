# Generated by Django 3.0.8 on 2020-10-12 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20201012_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='vehiclebrand',
            name='brand_name',
            field=models.CharField(choices=[('HATCHPACK', 'HATCHPACK'), ('SEDAN', 'SEDAN'), ('SUV', 'SUV')], max_length=250),
        ),
    ]