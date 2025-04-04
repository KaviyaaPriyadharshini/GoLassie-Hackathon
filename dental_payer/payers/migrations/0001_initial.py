# Generated by Django 5.1.7 on 2025-03-15 05:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pretty_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayerGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payer_number', models.CharField(blank=True, max_length=50, null=True)),
                ('tax_id', models.CharField(blank=True, max_length=50, null=True)),
                ('source', models.CharField(max_length=255)),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='payers.payer')),
            ],
        ),
        migrations.AddField(
            model_name='payer',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payers', to='payers.payergroup'),
        ),
    ]
