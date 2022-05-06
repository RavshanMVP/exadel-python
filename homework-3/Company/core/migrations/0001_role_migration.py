from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=7, verbose_name='User or Company')),
                ('status', models.CharField(choices=[('user', 'User'), ('Comp', 'Company')], default='user', max_length=4)),
            ],
        ),
    ]
