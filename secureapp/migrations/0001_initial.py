# Generated by Django 4.2.4 on 2023-09-25 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('category_key', models.CharField(max_length=255)),
                ('category_value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SecureItemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('platform', models.CharField(max_length=100)),
                ('custom_platform', models.CharField(blank=True, max_length=100, null=True)),
                ('visibility', models.CharField(default='private', max_length=100)),
                ('i_label', models.CharField(max_length=255, unique=True)),
                ('the_key', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('last_review', models.DateTimeField(auto_now=True)),
                ('i_username', models.TextField(blank=True, null=True)),
                ('i_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('i_email', models.EmailField(blank=True, max_length=300, null=True)),
                ('i_password', models.CharField(blank=True, max_length=300, null=True)),
                ('i_passphrase', models.CharField(blank=True, max_length=300, null=True)),
                ('i_api', models.CharField(blank=True, max_length=300, null=True)),
                ('i_ssh_key_pub', models.CharField(blank=True, max_length=300, null=True)),
                ('i_ssh_key_prt', models.CharField(blank=True, max_length=300, null=True)),
                ('i_card_no', models.CharField(blank=True, max_length=300, null=True)),
                ('i_card_valid_range', models.CharField(blank=True, max_length=300, null=True)),
                ('i_card_ccv', models.CharField(blank=True, max_length=300, null=True)),
                ('i_card_pin', models.CharField(blank=True, max_length=300, null=True)),
                ('i_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.passcode')),
                ('trusted_user', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('platform_key', models.CharField(max_length=255)),
                ('platform_value', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secureapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='ItemSecretIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.TextField(blank=True, null=True)),
                ('rely_on', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='secureapp.secureiteminfo')),
                ('trusted_people', models.ManyToManyField(blank=True, related_name='trusted_people', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemSecret',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_hash', models.TextField(blank=True, null=True)),
                ('the_private', models.TextField(blank=True, null=True)),
                ('rely_on', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='secureapp.secureiteminfo')),
            ],
        ),
    ]
