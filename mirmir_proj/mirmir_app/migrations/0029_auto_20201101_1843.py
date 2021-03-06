# Generated by Django 3.1.1 on 2020-11-02 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mirmir_app', '0028_auto_20201101_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailconfirmation',
            name='user',
        ),
        migrations.AddField(
            model_name='emailconfirmation',
            name='contact',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='email_confirmations', to='mirmir_app.contact'),
            preserve_default=False,
        ),
    ]
