# Generated by Django 3.2.7 on 2021-09-29 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0015_auto_20210222_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateSelector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
    ]
