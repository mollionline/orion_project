# Generated by Django 4.0.6 on 2022-07-25 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_user_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_permission',
            field=models.CharField(choices=[('has_not_permission', 'has_not_permission'), ('has_permission', 'has_permission')], default='has_not_permission', max_length=50, verbose_name='Права устройства'),
        ),
    ]