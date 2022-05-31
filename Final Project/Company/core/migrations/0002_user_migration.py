# Generated by Django 4.0.4 on 2022-05-12 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):


    dependencies = [('core', '0001_role_migration')
    ]

    operations = [

        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50, verbose_name='Full name of the user')),
                ('email', models.EmailField(max_length=254, verbose_name='Email of the user')),
                ('phone_number', models.CharField(default='+123456789', max_length=15, verbose_name='Number')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.role')),
            ],
        ),



    ]
