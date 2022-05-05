from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [ ('models','0003_service_migration')
    ]

    operations = [

        migrations.CreateModel(
            name='RequestStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pend', 'Pending'), ('Canc', 'Canceled'), ('Comp', 'Completed')], default='Pend', max_length=4)),
            ],
        ),


    ]
