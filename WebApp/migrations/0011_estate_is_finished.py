# Generated by Django 3.1.6 on 2021-03-16 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0010_auto_20210316_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='estate',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]
