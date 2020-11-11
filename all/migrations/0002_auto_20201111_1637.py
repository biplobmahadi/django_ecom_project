# Generated by Django 3.1.2 on 2020-11-11 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(editable=False, help_text='set a slug for url', max_length=150, unique=True),
        ),
    ]
