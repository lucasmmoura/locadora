from django.db import models
from .base import BaseModel
from locadora_app.models.carro import Carro
from datetime import date
from django.core.validators import *

class Aluguel(BaseModel):
    carro = models.ForeignKey(
        Carro,
        on_delete = models.CASCADE
    )

    data_inicio = models.DateField(
        verbose_name= 'Data de início',
        help_text='Qual foi a data de aluguel?',
    )

    data_prevista_devolucao = models.DateField(
        verbose_name = 'Qual a data prevista para a devolução?',
        help_text = 'Data prevista para devolução',
    )

    data_devolucao = models.DateField(
        verbose_name = 'Data de devolução',
        help_text = 'Data que o carro foi devolvido',
        blank = True,
        null = True
        #Data não pode ser antes da data atual
    )

    valor_total = models.DecimalField(
        verbose_name = 'Valor total',
        help_text = 'Valores finais',
        max_digits = 8,
        decimal_places = 2,
        null=True,
        blank = True,
        editable = False
    )

    ativo = models.BooleanField(
        verbose_name = 'Alugar carro?',
        help_text = 'Alugar carro?',
        default = True
    )





    def finalizar(self):
        self.data_devolucao = date.today()

        dias = (self.data_devolucao - self.data_inicio).days
        #Validação caso o aluguel termine no mesmo dia
        if dias <= 0:
            dias = 1

        self.valor_total = dias * (self.carro.valor_diaria + self.carro.seguro)

        #Quando clicar em finalizar ele vai atualizar os checkbox
        self.ativo = False
        self.carro.alugado = False

        #Salvar
        self.carro.save()
        self.save()

        if not self.ativo:
            return



    def clean(self):
        if self.carro.alugado == True:
            raise ValidationError ('Carro já está alugado')

        if self.carro.ipva == False:
            raise ValidationError("Carro com IPVA atrasado não pode ser alugado")


        ano_atual = date.today().year
        ano_minimo = date.today().year - 1
        if self.carro.ultima_revisao.year < ano_minimo:
            raise ValidationError('A última revisão não pode ter sido feita a mais de um ano')


        data_comeco = date.today()
        if self.data_inicio < data_comeco:
            raise ValidationError("Data de aluguel não pode ser menor que hoje")
        if self.data_inicio > data_comeco:
            raise ValidationError("Data de alugel não pode ser no futuro")


        if self.data_prevista_devolucao < data_comeco:
            raise ValidationError("Data prevista para devolução não pode ser menor que hoje")

        if self.data_devolucao and self.data_devolucao < data_comeco:  #Se a data de devolução for true e data de devolução for menor que data comeco
            raise ValidationError("Data de devolução não pode ser menor do que a data de inicio do aluguel")



    def save(self, *args, **kwargs):
        if self.pk is None: #pk = primary key. quando é none significa que o objeto não foi salvo nenhuma vez
            self.carro.alugado = True
            self.carro.save()
        super().save(*args, **kwargs)





    class Meta:
        verbose_name = 'ALUGUEL',
        verbose_name_plural = 'ALUGUEL'

    def __str__(self):
        return(
            f"Aluguel - A{self.id} - {self.carro} - ({self.data_inicio} até {self.data_prevista_devolucao})"
        )

