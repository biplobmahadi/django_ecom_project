# Generated by Django 3.1.5 on 2021-06-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0002_auto_20210619_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myorder',
            name='is_canceled',
        ),
        migrations.RemoveField(
            model_name='myorder',
            name='is_confirmed',
        ),
        migrations.AddField(
            model_name='myorder',
            name='order_status',
            field=models.CharField(blank=True, choices=[('confirmed', 'confirmed'), ('cancelled', 'cancelled')], max_length=10),
        ),
    ]
