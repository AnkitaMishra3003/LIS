# Generated by Django 5.0.3 on 2024-03-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_transaction_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='notification',
            field=models.CharField(default='0', max_length=1000),
        ),
    ]
