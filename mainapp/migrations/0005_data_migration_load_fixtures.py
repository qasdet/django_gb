from django.core.management import call_command
from django.db import migrations


def forwards_func(apps, schema_editor):
    fixtures = [
        "001_news",
        "002_courses",
        "003_lessons",
        "004_teachers",
    ]
    for fixture in fixtures:
        call_command("loaddata", fixture, app_label="mainapp")


def reverse_func(apps, schema_editor):
    models = [
        "News",
        "Courses",
        "Lessons",
        "Teachers",
    ]
    for model in models:
        MyModel = apps.get_model("mainapp", model)
        MyModel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0004_teachers_model"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
