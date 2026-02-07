from datetime import date
from django.core.validators import *


def validar_ano(valor):
    ano_atual = date.today().year
    ano_minimo = ano_atual - 5
    ano_maximo = ano_atual + 5

    if valor < ano_minimo or valor > ano_maximo:
        raise ValidationError(
            f"O ano máximo permitido é {ano_maximo} e o ano mínimo é {ano_minimo}",
            params = { 'value': valor}
        )
