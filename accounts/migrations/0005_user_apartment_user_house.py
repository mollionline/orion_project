# Generated by Django 4.0.6 on 2022-07-26 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0013_remove_apartment_customer_remove_house_customer'),
        ('accounts', '0004_alter_user_user_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='apartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_apartments', to='api_v1.apartment', verbose_name='Квартира'),
        ),
        migrations.AddField(
            model_name='user',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_houses', to='api_v1.house', verbose_name='Дом'),
        ),
    ]
