from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import OrderingFilter, SearchFilter
from locadora_app.models.carro import Carro
from locadora_app.serializers.carro import CarroSerializer



class CarroListCreateView(ListCreateAPIView): #Cria uma view de api e já vem pronta pra get e post
    # Diz qual dado a api usa, no caso são todos de Carro
    queryset = Carro.objects.all()

    # Diz como os dados entram e saem da api
    serializer_class = CarroSerializer

    # Apenas leitura para quem está deslogado e leitura e post para quem está logado
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Cria um filtro
    filter_backends = [OrderingFilter, SearchFilter]

    #Ordenar todos os campos
    ordering_fields = '__all__'

    #
    search_fields = ['marca', 'modelo']



class CarroDetailView(RetrieveUpdateDestroyAPIView): #Get, PUT/PATCH, Delete
    queryset = Carro.objects.all()
    serializer_class = CarroSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    ordering = ['id'] #Mostra a lista sempre ordenada
    