# Generated by Django 3.2.14 on 2022-07-21 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0013_auto_20220606_0031"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="courses",
            options={"verbose_name": "Course", "verbose_name_plural": "Courses"},
        ),
    ]
