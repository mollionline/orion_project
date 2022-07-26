from django.contrib import admin
from .models import City, District, Street, House, Apartment, Node, Device, Meter


# Register your models here.
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Город"""
    list_display = ('name', 'district', 'street')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    """Район"""
    list_display = ('name', 'street')


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    """Улица"""
    list_display = ('name', 'house')


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    """Дом"""
    list_display = ('name', 'apartment', 'node')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    """Квартира"""
    list_display = ('number', 'node')


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    """Узел"""
    list_display = ('uuid', 'geo', 'name', 'description', 'owner', 'address', 'node_permission')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """Устройство"""
    list_display = (
        'uuid', 'dev_eui', 'updated_at', 'activated_at',
        'on_off', 'description', 'type', 'owner', 'device_permission', 'apartment', 'house')


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    """Счетчик"""
    list_display = (
        'uuid', 'serial_number', 'on_off', 'registration',
        'first_testify_date', 'start_value', 'measure', 'meter_permission'
    )
