# Generated by Django 3.2.8 on 2021-12-27 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0017_firm'),
    ]

    operations = [
        migrations.AddField(
            model_name='trancation',
            name='firm',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ledger.firm'),
        ),
    ]
