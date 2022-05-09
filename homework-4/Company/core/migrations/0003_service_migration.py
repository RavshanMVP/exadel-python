from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('models', '0002_user_migration')
                    ]

    operations = [

        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name of the service')),
                ('cost', models.FloatField(default=0.0, verbose_name='price of one service')),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.user')),
            ],
        ),

    ]
