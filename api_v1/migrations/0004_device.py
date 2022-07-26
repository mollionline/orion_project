# Generated by Django 4.0.6 on 2022-07-25 06:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0003_alter_house_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=100000, primary_key=True, serialize=False)),
                ('dev_eui', models.CharField(max_length=16, unique=True, verbose_name='Идентификатор')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время последнего показания')),
                ('activated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время активации')),
                ('on_off', models.CharField(choices=[('Выкл', 'Выкл'), ('Вкл', 'Вкл')], default='Выкл', max_length=50, verbose_name='Состояние')),
                ('description', models.CharField(max_length=150, verbose_name='Описание')),
                ('type', models.CharField(max_length=50, verbose_name='Тип устройства')),
                ('owner', models.CharField(max_length=100, verbose_name='Владелец')),
                ('device_permission', models.CharField(choices=[(False, False), (True, True)], default=False, max_length=50, verbose_name='Права устройства')),
            ],
        ),
    ]
