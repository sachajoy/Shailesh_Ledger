# Generated by Django 3.1.6 on 2021-02-22 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0014_remove_client_mobno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
