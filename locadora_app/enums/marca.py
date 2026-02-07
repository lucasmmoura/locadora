from django.db import models

class Marca(models.TextChoices):
    PORSCHE = 'PORSCHE', 'Porsche'
    FERRARI = 'FERRARI', 'Ferrari'
    FORD = 'FORD', 'Ford'
    LAMBORGHINI = 'LAMBORGHINI', 'Lamborghini'
    TESLA = 'TESLA', 'Tesla'
    BUGATTI = 'BUGATTI', ' Bugatti'