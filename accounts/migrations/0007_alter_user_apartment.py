# Generated by Django 4.0.6 on 2022-07-26 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0013_remove_apartment_customer_remove_house_customer'),
        ('accounts', '0006_remove_user_apartment_user_apartment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='apartment',
            field=models.ManyToManyField(blank=True, related_name='customer_apartments', to='api_v1.apartment', verbose_name='Квартира'),
        ),
    ]
