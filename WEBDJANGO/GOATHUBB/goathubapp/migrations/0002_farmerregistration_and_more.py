# Generated by Django 5.1.3 on 2024-12-04 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goathubapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerRegistration',
            fields=[
                ('registration_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=50, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('district', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='veterinaryconsultation',
            name='farmer_id',
        ),
        migrations.AddField(
            model_name='veterinaryconsultation',
            name='farmer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='goathubapp.farmer'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='disease',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='goathubapp.disease'),
        ),
        migrations.AlterField(
            model_name='veterinaryconsultation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('in_progress', 'In Progress')], default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='veterinaryconsultation',
            name='veterinary_response',
            field=models.TextField(blank=True, null=True),
        ),
    ]
