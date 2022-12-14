# Generated by Django 3.2.14 on 2022-07-21 19:01

from django.db import migrations, models

import authapp.models


class Migration(migrations.Migration):

    dependencies = [
        ("authapp", "0004_alter_customuser_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="age",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="age"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to=authapp.models.users_avatars_path, verbose_name="avatar"
            ),
        ),
    ]
