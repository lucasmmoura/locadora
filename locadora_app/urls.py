from django.urls import path
from locadora_app.views.carro import CarroListCreateView, CarroDetailView
from locadora_app.views.aluguel import AluguelListCreateView, AluguelDetailView

urlpatterns = [
    path("carros/", CarroListCreateView.as_view()),
    path("carros/<int:pk>/", CarroDetailView.as_view()), #Captura o ID

    path("aluguels/", AluguelListCreateView.as_view()), #GET E POST
    path("aluguels/<int:pk>/", AluguelDetailView.as_view()), #Pega o ID e mostra os detalhes

]