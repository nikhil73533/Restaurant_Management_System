# Generated by Django 3.2 on 2021-06-02 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0016_review_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='check_sum',
        ),
    ]