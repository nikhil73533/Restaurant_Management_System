# Generated by Django 3.2 on 2021-04-23 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0002_alter_myuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic/'),
        ),
    ]