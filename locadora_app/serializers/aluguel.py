from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from locadora_app.models import Aluguel
from locadora_app.serializers.carro import CarroSerializer
from locadora_app.models.carro import Carro

class AluguelSerializer(ModelSerializer):

    carro = CarroSerializer(read_only = True)
    carro_id = PrimaryKeyRelatedField(
        queryset = Carro.objects.all(),
        source = 'carro',
        write_only = True,
    )





    class Meta:
        model = Aluguel
        exclude = ['usuario']