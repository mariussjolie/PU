# Generated by Django 3.1.6 on 2021-02-23 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0008_auto_20210223_2124'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('user', 'item'), name='unique_useritem'),
        ),
    ]
