# Generated by Django 5.1.3 on 2024-12-06 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goathubapp', '0004_consultationreply_specialcase_vetconsultation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationreply',
            name='farmer_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
