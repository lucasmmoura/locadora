from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from locadora_app.models.carro import Carro
from datetime import date
from datetime import timedelta


class AluguelTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="teste",
            password="123"
        )

        self.client.login(username="teste", password="123")

        self.carro = Carro.objects.create(
            marca="Porsche",
            modelo="911",
            ano=2026,
            placa="ABC1234",
            valor_diaria=1000,
            seguro=100,
            ultima_revisao=date.today(),
            ipva=True,
            alugado=False
        )

    def test_nao_pode_alugar_carro_ja_alugado(self):
        hoje = date.today()

        response1 = self.client.post(
            "/api/aluguels/",
            {
                "carro_id": self.carro.id,
                "data_inicio": hoje,
                "data_prevista_devolucao": hoje
            },
            format="json"
        )

        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post(
            "/api/aluguels/",
            {
                "carro_id": self.carro.id,
                "data_inicio": hoje,
                "data_prevista_devolucao": hoje
            },
            format="json"
        )

        self.assertEqual(response2.status_code, 400)

    def test_nao_pode_editar_aluguel_finalizado(self):
        hoje = date.today()

        response = self.client.post(
            "/api/aluguels/",
            {
                "carro_id": self.carro.id,
                "data_inicio": hoje,
                "data_prevista_devolucao": hoje
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        aluguel_id = response.data["id"]

        # Finalizar
        self.client.patch(f"/api/aluguels/{aluguel_id}/")

        # Tentar editar
        response_update = self.client.put(
            f"/api/aluguels/{aluguel_id}/",
            {
                "carro_id": self.carro.id,
                "data_inicio": hoje,
                "data_prevista_devolucao": hoje
            },
            format="json"
        )

        self.assertEqual(response_update.status_code, 400)

    def test_finalizacao_altera_status_corretamente(self):
        hoje = date.today()

        response = self.client.post(
            "/api/aluguels/",
            {
                "carro_id": self.carro.id,
                "data_inicio": hoje,
                "data_prevista_devolucao": hoje
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        aluguel_id = response.data["id"]

        # Finalizar
        self.client.patch(f"/api/aluguels/{aluguel_id}/")

        # Buscar novamente
        response_detail = self.client.get(f"/api/aluguels/{aluguel_id}/")

        self.assertEqual(response_detail.status_code, 200)
        self.assertEqual(response_detail.data["ativo"], False)
        self.assertIsNotNone(response_detail.data["valor_total"])
