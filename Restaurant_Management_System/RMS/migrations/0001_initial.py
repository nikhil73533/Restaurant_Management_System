# Generated by Django 3.2 on 2021-05-26 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Food_Name', models.CharField(max_length=100)),
                ('Food_Price', models.IntegerField()),
                ('Discount_In_Percentage', models.IntegerField(blank=True, null=True)),
                ('Food_Avg_Rating', models.FloatField(null=True)),
                ('Food_Type', models.CharField(max_length=100)),
                ('Description', models.CharField(max_length=5000)),
                ('food_pic', models.ImageField(blank=True, null=True, upload_to='Food/')),
                ('users', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Foodtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_type', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capicity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('Name', models.CharField(max_length=50, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=60, unique=True, verbose_name='email address')),
                ('Address', models.CharField(max_length=200, verbose_name='Address')),
                ('state', models.CharField(max_length=100, null=True, verbose_name='state')),
                ('city', models.CharField(max_length=100, null=True, verbose_name='city')),
                ('pincode', models.CharField(max_length=50, null=True, verbose_name='Pincode')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/')),
                ('phone', models.CharField(max_length=20, verbose_name='phone number')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('penilty', models.FloatField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=5000)),
                ('rate', models.PositiveIntegerField()),
                ('food', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='RMS.food')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(verbose_name='date published')),
                ('order_address', models.CharField(max_length=5000)),
                ('state', models.CharField(max_length=5000, null=True)),
                ('city', models.CharField(max_length=5000, null=True)),
                ('pincode', models.CharField(max_length=5000, null=True)),
                ('quantity', models.IntegerField()),
                ('deliver_status', models.BooleanField(default=False)),
                ('total_amount', models.FloatField(null=True)),
                ('food', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='RMS.food')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.BooleanField(default=False)),
                ('discount', models.PositiveIntegerField()),
                ('tex', models.PositiveIntegerField()),
                ('penilty', models.PositiveIntegerField(null=True)),
                ('total_amount', models.FloatField(null=True)),
                ('food', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='RMS.food')),
                ('order_no', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='RMS.orders')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
