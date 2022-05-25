from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_custom_python_migration'),
    ]

    operations = [


migrations.RunSQL(
    'ALTER TABLE "core_category"'
    'RENAME COLUMN category TO name'
    ';'
),


migrations.RunSQL(
    'INSERT INTO "core_category" VALUES (1,"Dusting");'
    'INSERT INTO "core_category" VALUES (2,"Dishwashing");'
    'INSERT INTO "core_category" VALUES (3, "Washing floors");'
),

    ]
