# Generated by Django 3.1.1 on 2020-10-16 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mirmir_app', '0008_auto_20201016_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='carouselslide',
            name='caption_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
