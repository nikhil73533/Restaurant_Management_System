# Generated by Django 3.2 on 2021-05-27 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0007_auto_20210527_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='Conform',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
