# Generated by Django 3.1.5 on 2021-02-01 10:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0006_remove_client_curr_bal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trancation',
            name='date',
            field=models.TextField(default=datetime.date.today),
        ),
    ]