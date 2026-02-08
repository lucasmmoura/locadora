from django.contrib import admin
from locadora_app.models.carro import Carro
from locadora_app.models.aluguel import Aluguel
# Register your models here.

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    readonly_fields = ("valor_diaria", "seguro")

@admin.register(Aluguel)
class AluguelAdmin(admin.ModelAdmin):

    readonly_fields = (
        "valor_total",
    )

    list_filter = (
        "ativo",
    )

    actions = ["finalizar_aluguel"]

    #Filtra os carros disponíveis para aluguel. Vai aparecer somente os carros com alugado = False
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "carro":
            kwargs["queryset"] = Carro.objects.filter(
                alugado = False
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




    def finalizar_aluguel(self, request, queryset):
        ativos = queryset.filter(
            ativo = True
        )

        if not ativos.exists():
            self.message_user(
                request,
                "Nenhum aluguel ativo selecionado",
                level= "warning"
            )
            return

        for aluguel in ativos:
            aluguel.finalizar()

        self.message_user(
            request,
            "Aluguel(is) ativo(s) finalizado(s) com sucesso."
        )

    finalizar_aluguel.short_description = "FINALIZAR ALUGUEL"



