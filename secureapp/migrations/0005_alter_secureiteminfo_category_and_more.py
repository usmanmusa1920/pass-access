# Generated by Django 4.0.2 on 2022-10-01 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secureapp', '0004_categories_category_platform_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secureiteminfo',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='secureiteminfo',
            name='platform',
            field=models.CharField(max_length=100),
        ),
    ]
