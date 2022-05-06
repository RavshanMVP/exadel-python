from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):



    dependencies = [ ('models','0006_review_migration')
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='service_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.service'),
        ),
        migrations.AddField(
            model_name='request',
            name='status_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.requeststatus'),
        ),
        migrations.AddField(
            model_name='request',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.user'),
        ),
    ]
