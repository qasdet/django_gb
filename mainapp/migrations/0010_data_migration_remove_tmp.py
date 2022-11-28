from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0009_data_migration_restore"),
    ]

    operations = [
        migrations.DeleteModel(
            name="NewsTemp",
        ),
    ]
