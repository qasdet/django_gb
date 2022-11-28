from django.db import migrations

from mainapp.models import News


def forwards_func(apps, schema_editor):
    news: News = apps.get_model("mainapp", "News")
    news_temp: News = apps.get_model("mainapp", "NewsTemp")
    for row in news_temp.objects.all():
        news.objects.create(
            title=row.title,
            preambule=row.preambule,
            body=row.body,
        )


def reverse_func(apps, schema_editor):
    news: News = apps.get_model("mainapp", "NewsTemp")
    news.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0008_data_migration_delete"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
