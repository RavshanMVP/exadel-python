from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):


    dependencies = [('models', '0005_request_migration')
    ]

    operations = [

        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, verbose_name='Star rating of the service')),
                ('feedback', models.TextField(default='', verbose_name='Comment of the service')),
                ('created_at', models.DateTimeField(null=True, verbose_name='Time of the comment')),
                ('request_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.request')),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.service')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.user')),
            ],
        ),

    ]
