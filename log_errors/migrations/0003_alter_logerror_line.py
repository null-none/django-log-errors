# Generated by Django 3.2.14 on 2022-08-13 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("log_errors", "0002_alter_logerror_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logerror",
            name="line",
            field=models.PositiveIntegerField(default=1),
        ),
    ]