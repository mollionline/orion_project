from django.db import models


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

    def __str__(self):
        return self.name


class Apartment(models.Model):
    """Квартира"""
    number = models.PositiveIntegerField(verbose_name='Квартира')

    def __str__(self):
        return f"{self.number}"
