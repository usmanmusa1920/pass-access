# Generated by Django 4.1 on 2022-10-01 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("secureapp", "0005_alter_secureiteminfo_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category_platform_list",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="secureapp.categories",
            ),
        ),
    ]
