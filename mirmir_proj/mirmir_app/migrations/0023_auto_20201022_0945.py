# Generated by Django 3.1.1 on 2020-10-22 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mirmir_app', '0022_auto_20201021_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description_teaser',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
    ]
