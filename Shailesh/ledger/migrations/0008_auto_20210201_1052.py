# Generated by Django 3.1.5 on 2021-02-01 10:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0007_auto_20210201_1035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trancation',
            options={},
        ),
        migrations.AddField(
            model_name='trancation',
            name='booking_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='trancation',
            name='passenger_list',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='trancation',
            name='date',
            field=models.TextField(),
        ),
    ]