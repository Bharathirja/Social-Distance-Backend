# Generated by Django 3.0.8 on 2020-11-02 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20201029_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='latitude_delta',
            field=models.CharField(default=1, max_length=200, verbose_name='latitude_delta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookings',
            name='longitude_delta',
            field=models.CharField(default=1, max_length=200, verbose_name='longitude_delta'),
            preserve_default=False,
        ),
    ]