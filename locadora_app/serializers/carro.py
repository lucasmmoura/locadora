from rest_framework.serializers import ModelSerializer
from locadora_app.models.carro import Carro


class CarroSerializer(ModelSerializer):
    class Meta:
        model = Carro
        fields = "__all__"