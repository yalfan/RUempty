# Generated by Django 4.2.5 on 2023-09-30 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RUempty', '0015_alter_meetingtime_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='name',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterUniqueTogether(
            name='building',
            unique_together={('campus', 'name')},
        ),
    ]