# Generated by Django 5.0.3 on 2024-03-19 13:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='last_issue_date',
            field=models.DateField(default=datetime.date(2024, 3, 19)),
        ),
        migrations.AlterField(
            model_name='book',
            name='max_reserve_date',
            field=models.DateField(default=datetime.date(2024, 3, 19)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='due_date',
            field=models.DateField(default=datetime.date(2024, 3, 19)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='issue_date',
            field=models.DateField(default=datetime.date(2024, 3, 19)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='max_date_of_reserve',
            field=models.DateField(default=datetime.date(2024, 3, 19)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='return_date',
            field=models.DateField(default=datetime.date(2024, 3, 19)),
        ),
        migrations.AlterField(
            model_name='user',
            name='valid_till',
            field=models.DateField(default=datetime.date(2024, 3, 19)),
        ),
    ]
