import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

STATUS_CHOICES = (
    ('Выкл', 'Выкл'),
    ('Вкл', 'Вкл'),
)

MODERATOR_STATUS_CHOICES = (
    ('False', 'False'),
    ('True', 'True'),
)


# Create your models here.
class City(models.Model):
    """Город"""
    name = models.CharField(verbose_name='Город', max_length=100)
    district = models.ForeignKey('api_v1.District', verbose_name='Район', related_name='districts',
                                 on_delete=models.CASCADE, null=True, blank=True)
    street = models.ForeignKey('api_v1.Street', verbose_name='Улица', related_name='city_streets',
                               on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    """Район"""
    name = models.CharField(verbose_name='Район', max_length=150)
    street = models.ForeignKey('api_v1.Street', verbose_name='Улица', related_name='district_streets',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Street(models.Model):
    """Улица"""
    name = models.CharField(verbose_name='Улица', max_length=150)
    house = models.ForeignKey('api_v1.House', verbose_name='Дом', related_name='houses',
                              on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class House(models.Model):
    """Дом"""
    name = models.CharField(verbose_name='Дом', max_length=100)
    apartment = models.ForeignKey('api_v1.Apartment', verbose_name='Квартира', related_name='apartments',
                                  on_delete=models.CASCADE, null=True, blank=True)
    node = models.ForeignKey('api_v1.Node', verbose_name='Узел', related_name='house_nodes',
                             on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    """Квартира"""
    number = models.PositiveIntegerField(verbose_name='Квартира')
    node = models.ForeignKey('api_v1.Node', verbose_name='Узел', related_name='apartment_nodes',
                             on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.number}"


class Device(models.Model):
    """Устройство"""
    uuid = models.CharField(
        max_length=100000,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    dev_eui = models.CharField(max_length=16, unique=True, verbose_name='Идентификатор')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время последнего показания", blank=True)
    activated_at = models.DateTimeField(verbose_name="Время активации", blank=True, null=True)
    on_off = models.CharField(max_length=50, null=False, blank=False,
                              choices=STATUS_CHOICES, verbose_name="Состояние", default='Выкл')
    description = models.CharField(max_length=150, verbose_name='Описание')
    type = models.CharField(max_length=50, verbose_name='Тип устройства')
    owner = models.CharField(max_length=100, verbose_name='Владелец')
    device_permission = models.CharField(max_length=50, null=False, blank=False,
                                         choices=MODERATOR_STATUS_CHOICES, verbose_name="Права устройства",
                                         default='False')
    apartment = models.ForeignKey('api_v1.Apartment', verbose_name='Квартира', related_name='device_apartments',
                                  on_delete=models.CASCADE, null=True, blank=True)
    house = models.ForeignKey('api_v1.House', verbose_name='Дом', related_name='device_houses',
                              on_delete=models.CASCADE, null=True, blank=True)
    meter = models.ManyToManyField('api_v1.Meter', verbose_name='Счетчик', related_name='device_meters',
                                   blank=True)

    def __str__(self):
        return f"{self.dev_eui}"


class Meter(models.Model):
    """Счетчик"""
    uuid = models.CharField(
        max_length=100000,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    serial_number = models.PositiveIntegerField(unique=True)
    on_off = models.CharField(max_length=50, null=False, blank=False,
                              choices=STATUS_CHOICES, verbose_name="Состояние", default='Выкл')
    registration = models.DateTimeField(verbose_name="Время регистрации", blank=True, null=True)
    first_testify_date = models.DateTimeField(verbose_name="Время первого показания", blank=True, null=True)
    start_value = models.PositiveIntegerField()
    measure = models.CharField(max_length=50)
    meter_permission = models.CharField(max_length=50, null=False, blank=False,
                                        choices=MODERATOR_STATUS_CHOICES, verbose_name="Права устройства",
                                        default='False')

    def __str__(self):
        return self.serial_number


class Node(models.Model):
    """Узел"""
    uuid = models.CharField(
        max_length=100000,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    geo = models.CharField(max_length=150, verbose_name='Координаты')
    name = models.CharField(max_length=150, verbose_name='Имя')
    description = models.CharField(max_length=150, verbose_name='Описание', null=True, blank=True)
    owner = models.CharField(max_length=100, verbose_name='Владелец', null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name='Адрес')
    node_permission = models.CharField(max_length=50, null=False, blank=False,
                                       choices=MODERATOR_STATUS_CHOICES, verbose_name="Права узла",
                                       default='False')

    def __str__(self):
        return self.name
