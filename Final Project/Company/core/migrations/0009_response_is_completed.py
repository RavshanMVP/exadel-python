# Generated by Django 3.2.13 on 2022-06-08 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20220608_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Completed or in process'),
        ),
    ]
