from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_category_migration'),
    ]

    operations = [


        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey (null=True,on_delete=models.deletion.CASCADE, to='core.category'),
            preserve_default=False,
        ),

    ]
