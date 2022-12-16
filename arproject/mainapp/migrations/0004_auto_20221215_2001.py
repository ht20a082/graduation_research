# Generated by Django 3.2 on 2022-12-15 11:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_image_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='height',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='width',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
