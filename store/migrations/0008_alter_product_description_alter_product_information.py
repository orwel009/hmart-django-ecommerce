# Generated by Django 4.0.6 on 2022-07-13 12:15

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='information',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
