# Generated by Django 3.2.16 on 2023-11-04 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20231104_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='blog_images', verbose_name='Изображение'),
        ),
    ]
