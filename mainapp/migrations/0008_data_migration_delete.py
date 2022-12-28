from django.db import migrations

from mainapp.models import News


def forwards_func(apps, schema_editor):
    news: News = apps.get_model("mainapp", "News")
    news.objects.all().delete()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0007_data_migration_move"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
