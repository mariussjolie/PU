# Generated by Django 3.1.6 on 2021-02-22 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0004_auto_20210216_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='picture',
            field=models.ImageField(default='images/default_image.png', upload_to='images/'),
        ),
    ]
