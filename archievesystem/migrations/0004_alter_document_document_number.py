# Generated by Django 5.1.4 on 2025-01-13 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archievesystem', '0003_document_document_number_document_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_number',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
