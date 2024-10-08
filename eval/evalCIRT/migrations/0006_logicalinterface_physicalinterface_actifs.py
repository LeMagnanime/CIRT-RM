# Generated by Django 5.0.4 on 2024-07-21 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyse_risques', '0007_remove_asset_menaces_alter_asset_criticite'),
        ('evalCIRT', '0005_alter_donnee_risque_brute'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogicalInterface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalInterface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('physical_address', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Actifs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('cpe_id', models.IntegerField()),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyse_risques.typeactif')),
                ('interface_logique', models.ManyToManyField(related_name='actifs', to='evalCIRT.logicalinterface')),
                ('interface_physique', models.ManyToManyField(related_name='actifs', to='evalCIRT.physicalinterface')),
            ],
            options={
                'verbose_name': 'Actifs',
            },
        ),
    ]
