# Generated by Django 3.1.5 on 2021-06-15 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_img',
        ),
    ]
