from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):


    dependencies = [('models','0004_request_status_migration')
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(default='', verbose_name='Full address')),
                ('created_at', models.DateTimeField(null=True, verbose_name='Time of the service')),
                ('area', models.FloatField(default=0.0, verbose_name='Area of cleaning')),
                ('cost_total', models.FloatField(default=0.0, verbose_name='Total cost of the service')),
            ],
        ),
    ]
