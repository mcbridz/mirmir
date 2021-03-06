# Generated by Django 3.1.1 on 2020-10-19 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mirmir_app', '0011_mainpagehighlight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselslide',
            name='display_order',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='carouselslide',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='carousel_images'),
        ),
        migrations.AlterField(
            model_name='mainpagehighlight',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='highlight_images'),
        ),
        migrations.AlterField(
            model_name='mainpagehighlight',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
