from django.contrib import admin
from .models import City, District, Street, House, Apartment


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
    list_display = ('name', 'apartment')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    """Квартира"""
    list_display = ('number',)
