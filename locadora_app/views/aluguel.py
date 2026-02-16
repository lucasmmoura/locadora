from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from locadora_app.models.aluguel import Aluguel
from locadora_app.serializers.aluguel import AluguelSerializer

from django_filters.rest_framework import DjangoFilterBackend




class AluguelListCreateView(ListCreateAPIView):
    queryset = Aluguel.objects.all()
    serializer_class = AluguelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ativo"]

    def perform_create(self, serializer):
        carro = serializer.validated_data['carro']

        if carro.alugado:
            raise ValidationError(
                "Esse carro já está alugado"
            )


        serializer.save(usuario=self.request.user)

    from rest_framework.filters import OrderingFilter, SearchFilter

    filter_backends= [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = "__all__"
    search_fields = ["carro__modelo", "carro__marca"]
    ordering = ["-id"]


    def get_queryset(self):
        #Cada usuário vê apenas seu próprio aluguel
        return Aluguel.objects.filter(usuario=self.request.user)


class AluguelDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AluguelSerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        return Aluguel.objects.filter(usuario=self.request.user)

    def patch(self, request, *args, **kwargs):
        aluguel = self.get_object()

        if not aluguel.ativo:
            return Response(
                {"detail":"Aluguel já finalizado"},
                status = status.HTTP_400_BAD_REQUEST
            )

        aluguel.finalizar()

        return Response(
            {"detail":"Aluguel finalizado com sucesso."},
            status = status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        aluguel = self.get_object()

        if not aluguel.ativo:
            return Response(
                {"detail":"Aluguel já finalizado não pode ser alterado"},
                status = status.HTTP_400_BAD_REQUEST
            )

        return save().update(request, *args, **kwargs)