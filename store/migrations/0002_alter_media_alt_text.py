# Generated by Django 4.1.1 on 2022-10-04 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="media",
            name="alt_text",
            field=models.CharField(
                blank=True,
                help_text="format: required, max_length-255",
                max_length=255,
                null=True,
                verbose_name="alternate text",
            ),
        ),
    ]
