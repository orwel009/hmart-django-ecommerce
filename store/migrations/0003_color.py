# Generated by Django 4.0.6 on 2022-07-13 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=30)),
            ],
        ),
    ]