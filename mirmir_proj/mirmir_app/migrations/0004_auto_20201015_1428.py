# Generated by Django 3.1.1 on 2020-10-15 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mirmir_app', '0003_auto_20201015_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='main_phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='state_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='zip_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
