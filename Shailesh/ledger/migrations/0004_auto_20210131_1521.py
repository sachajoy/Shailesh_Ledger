# Generated by Django 3.1.5 on 2021-01-31 15:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0003_auto_20210131_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trancation',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
