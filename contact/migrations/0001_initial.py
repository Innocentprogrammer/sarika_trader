# Generated by Django 5.0.4 on 2025-05-25 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=60)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=400)),
                ('country', models.CharField(max_length=15)),
                ('state', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=15)),
                ('pincode', models.CharField(max_length=10)),
                ('message', models.TextField()),
            ],
        ),
    ]
