# Generated by Django 3.2 on 2021-05-31 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0012_rename_contact_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='Name',
            field=models.CharField(max_length=5000, null=True),
        ),
    ]
