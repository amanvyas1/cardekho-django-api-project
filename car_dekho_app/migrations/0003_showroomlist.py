# Generated by Django 5.0.1 on 2024-01-23 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dekho_app', '0002_carlist_chassisnumber_carlist_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowroomList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('website', models.URLField(max_length=100)),
            ],
        ),
    ]
