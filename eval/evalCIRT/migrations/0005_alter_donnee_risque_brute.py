# Generated by Django 5.0.3 on 2024-04-14 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evalCIRT', '0004_donnee_alter_company_number_alter_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donnee',
            name='risque_brute',
            field=models.FloatField(default=0),
        ),
    ]
