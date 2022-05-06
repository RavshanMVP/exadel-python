from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):


    dependencies = [('models', '0001_role_migration')
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50, verbose_name='Full name of the user')),
                ('email', models.EmailField(max_length=254, verbose_name='Email of the user')),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.role')),
            ],
        ),

    ]
