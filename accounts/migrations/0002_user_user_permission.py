# Generated by Django 4.0.6 on 2022-07-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_permission',
            field=models.CharField(choices=[(False, False), (True, True)], default=False, max_length=50, verbose_name='Права устройства'),
        ),
    ]
