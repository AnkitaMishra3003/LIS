# Generated by Django 5.0.3 on 2024-03-23 15:05

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('issued_code', models.CharField(default='0', max_length=9)),
                ('reserved_code', models.CharField(default='0', max_length=9)),
                ('edition', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)])),
                ('year', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2101)])),
                ('category', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Adventure'), (2, 'Fantasy'), (3, 'Crime'), (4, 'Classics'), (5, 'History'), (6, 'Romance'), (7, 'Biography'), (8, 'Mathematics'), (9, 'Computer Science'), (10, 'Science'), (11, 'Mechanics')], default=0, null=True)),
                ('last_issue_date', models.DateField(default=datetime.date(2024, 3, 23))),
                ('available', models.BooleanField(default=1)),
                ('reserved', models.BooleanField(default=0)),
                ('max_reserve_date', models.DateField(default=datetime.date(2024, 3, 23))),
                ('cupboard', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('rack', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)])),
                ('position', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)])),
                ('ISBN', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Issue Book'), (2, 'Return Book'), (3, 'Reserve Book')], default=0, null=True)),
                ('max_date_of_reserve', models.DateField(default=datetime.date(2024, 3, 23))),
                ('issue_date', models.DateField(default=datetime.date(2024, 3, 23))),
                ('due_date', models.DateField(default=datetime.date(2024, 3, 23))),
                ('return_date', models.DateField(default=datetime.date(2024, 3, 23))),
                ('dues', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('user_code', models.CharField(default='0', max_length=9)),
                ('book_id', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=9)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=12)),
                ('notification', models.CharField(max_length=1000)),
                ('type', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Undergraduate Student'), (2, 'Postgraduate Student'), (3, 'Research Scholar'), (4, 'Faculty Member'), (5, 'Administrator')], default=0, null=True)),
                ('max_books', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(10)])),
                ('active_no', models.IntegerField(default=0)),
                ('reserve_no', models.IntegerField(default=0)),
                ('fine', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('valid_till', models.DateField(default=datetime.date(2024, 3, 23))),
                ('active_books', models.ManyToManyField(blank=True, null=True, related_name='active_books', to='api.book')),
                ('reserved_books', models.ManyToManyField(blank=True, null=True, related_name='reserved_books', to='api.book')),
                ('transactions', models.ManyToManyField(blank=True, null=True, related_name='transactions', to='api.transaction')),
                ('users', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
