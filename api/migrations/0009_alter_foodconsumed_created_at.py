# Generated by Django 4.1 on 2022-08-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_timespend_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodconsumed',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
