# Generated by Django 4.2.5 on 2023-09-30 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RUempty', '0014_rename_building_code_room_building_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingtime',
            name='day',
            field=models.CharField(max_length=4),
        ),
    ]