# Generated by Django 4.2.5 on 2023-09-30 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RUempty', '0008_rename_name_room_number_alter_room_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='section',
            name='start_time',
        ),
        migrations.AddField(
            model_name='section',
            name='time_block',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='RUempty.timeblock'),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
