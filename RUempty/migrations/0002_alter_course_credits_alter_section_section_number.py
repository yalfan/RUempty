# Generated by Django 4.1.1 on 2023-09-27 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RUempty', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='credits',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='section',
            name='section_number',
            field=models.IntegerField(),
        ),
    ]
