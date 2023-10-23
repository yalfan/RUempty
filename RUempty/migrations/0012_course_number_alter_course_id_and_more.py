# Generated by Django 4.2.5 on 2023-09-30 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RUempty', '0011_subject_course_subject_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='number',
            field=models.CharField(default=None, max_length=3),
        ),
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('subject_id', 'id')},
        ),
    ]
