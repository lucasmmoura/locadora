from django.db import models
from django.db.models import DateField
from django.core.validators import MinLengthValidator, MinValueValidator
from .base import BaseModel
from locadora_app.enums import Marca
from datetime import date
from locadora_app.validators.validators import *




class Carro(BaseModel):

    marca = models.CharField(
        verbose_name='Marca',
        help_text = 'Marca do carro',
        choices = Marca,
        max_length = 20,
        validators = [MinLengthValidator(4, "Mínimo de 4 caracteres")]
    )

    modelo = models.CharField(
        verbose_name = 'Modelo',
        help_text= 'Modelo do carro',
        max_length= 20,
        validators= [MinLengthValidator(2, 'Mínimo de 2 caracteres')],
        default= 0
    )

    ano = models.IntegerField(
        verbose_name= 'Ano',
        help_text= 'Digite o ano do carro',
        default= date.today().year,
        validators = [validar_ano]

    )

    alugado = models.BooleanField(
        verbose_name= 'Alugado?',
        help_text='Marque se o carro estiver alugado',
        default= False
    )

    placa = models.CharField(
        verbose_name= 'Placa',
        help_text= 'Digite a placa do carro',
        max_length= 7,
        validators= [MinLengthValidator(7, 'Mínimo 7 caracteres')],
        default= 0
    )

    valor_diaria = models.DecimalField(
        verbose_name= 'Valor da diária',
        help_text= 'Calculado automáticamente',
        validators= [MinValueValidator(200)],
        decimal_places= 2,
        max_digits= 8,
        default= None,
        editable = False
    )

    seguro = models.DecimalField(
        verbose_name = 'Seguro',
        help_text = 'Valor do seguro do carro selecionado',
        validators = [MinValueValidator(50, 'Valor mínimo é 50')],
        max_digits = 8,
        decimal_places = 2,
        default = None,
        editable = False
    )

    ultima_revisao = models.DateField(
        verbose_name = 'Data da última revisão',
        help_text = 'Data da última revisão',
    )

    ipva = models.BooleanField(
        verbose_name = 'IPVA',
        help_text = 'O IPVA está pago?',
        default = True
    )






    class Meta:
        abstract = False
        verbose_name = 'CARRO'
        verbose_name_plural = 'CARROS'




    def __str__(self):
        return f"{self.id} - {self.marca}"


    def clean(self):
        if not self.ipva and self.alugado:
            raise ValidationError(
                f"Carros com IPVA atrasados não podem ser alugados"
            )

        ano_hoje = date.today().year
        ano_minimo = date.today().year - 1
        if self.ultima_revisao.year < ano_minimo:
            raise ValidationError(
                f"Carros com vistoria há mais de um ano não podem ser alugados"
            )




    def save(self, *args, **kwargs):
        if self.marca == Marca.PORSCHE:
            self.valor_diaria = 2000
        if self.marca == Marca.FERRARI:
            self.valor_diaria = 1500
        if self.marca == Marca.FORD:
            self.valor_diaria = 200
        if self.marca == Marca.LAMBORGHINI:
            self.valor_diaria = 2000
        if self.marca == Marca.TESLA:
            self.valor_diaria = 500
        if self.marca == Marca.BUGATTI:
            self.valor_diaria = 5000


        self.seguro = max(self.valor_diaria * 0.05, 50)

        super().save(*args, **kwargs)

