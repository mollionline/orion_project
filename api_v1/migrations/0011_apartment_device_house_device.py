# Generated by Django 4.0.6 on 2022-07-26 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0010_node_node_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apartment_devices', to='api_v1.device', verbose_name='Устройство'),
        ),
        migrations.AddField(
            model_name='house',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='house_devices', to='api_v1.device', verbose_name='Устройство'),
        ),
    ]
