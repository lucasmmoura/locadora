from django.contrib import admin
from locadora_app.models.carro import Carro
# Register your models here.

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    readonly_fields = ("valor_diaria", "seguro")

