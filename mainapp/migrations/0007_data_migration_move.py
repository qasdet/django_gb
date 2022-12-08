from django.db import migrations, models

from mainapp.models import News


def forwards_func(apps, schema_editor):
    news: News = apps.get_model("mainapp", "News")
    news_temp: News = apps.get_model("mainapp", "NewsTemp")
    for row in news.objects.all():
        news_temp.objects.create(
            title=row.title,
            preambule=row.preambule,
            body=row.body,
        )


def reverse_func(apps, schema_editor):
    news_temp = apps.get_model("mainapp", "NewsTemp")
    news_temp.objects.all().delete()
    schema_editor.delete_model(news_temp)


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0006_data_migration_news"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsTemp",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=256, verbose_name="Title")),
                ("preambule", models.CharField(max_length=1024, verbose_name="Preambule")),
                ("body", models.TextField(blank=True, null=True, verbose_name="Body")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
