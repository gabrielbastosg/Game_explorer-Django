from unittest.mock import patch

import requests
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import FavoriteGame, GameStatus


def fake_response(payload):
    """Cria um objeto parecido com o retorno do requests.get, com .json()
    e .raise_for_status() que nao fazem nada de errado."""
    class _Resp:
        def json(self):
            return payload

        def raise_for_status(self):
            pass

    return _Resp()


class HomeRobustnessTest(TestCase):
    def setUp(self):
        # O cache vive na memoria e vazaria entre os testes; limpamos antes
        # de cada um para que cada teste comece com o cache vazio.
        cache.clear()

    @patch('games.views.requests.get')
    def test_home_mostra_jogo_quando_api_responde(self, mock_get):
        mock_get.return_value = fake_response({
            'results': [{'id': 1, 'name': 'The Witcher 3'}],
            'count': 1,
            'next': None,
            'previous': None,
        })

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The Witcher 3')

    @patch('games.views.requests.get')
    def test_home_nao_quebra_quando_api_falha(self, mock_get):
        # Simula a RAWG fora do ar / timeout.
        mock_get.side_effect = requests.RequestException('API fora do ar')

        response = self.client.get(reverse('home'))

        # O importante: pagina abre (200), nao da erro 500, e sem jogos.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['games']), [])

    @patch('games.views.requests.get')
    def test_segunda_visita_usa_cache_e_nao_chama_api(self, mock_get):
        mock_get.return_value = fake_response({
            'results': [{'id': 1, 'name': 'The Witcher 3'}],
            'count': 1,
            'next': None,
            'previous': None,
        })

        self.client.get(reverse('home'))   # 1a visita: bate na API e guarda
        self.client.get(reverse('home'))   # 2a visita: deveria vir do cache

        # A API foi consultada uma unica vez; a segunda veio do cache.
        self.assertEqual(mock_get.call_count, 1)


class MyShelfTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='gamer', password='senha123')
        self.client.login(username='gamer', password='senha123')

    def test_progresso_calcula_porcentagem_de_zerados(self):
        GameStatus.objects.create(user=self.user, game_id=1, name='Jogo A', status='zerei')
        GameStatus.objects.create(user=self.user, game_id=2, name='Jogo B', status='quero')

        response = self.client.get(reverse('my_shelf'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total'], 2)
        self.assertEqual(response.context['progresso'], 50)

    def test_progresso_zero_quando_estante_vazia(self):
        response = self.client.get(reverse('my_shelf'))

        self.assertEqual(response.context['total'], 0)
        self.assertEqual(response.context['progresso'], 0)

    def test_delete_review_limpa_nota_e_comentario(self):
        # Arrange: um jogo zerado, ja com nota e review preenchidos
        jogo = GameStatus.objects.create(
            user=self.user, game_id=42, name='Celeste',
            status='zerei', nota=5, review='Obra-prima',
        )

        # Act: simula o clique no botao "Apagar" (um POST para a view)
        self.client.post(reverse('delete_review', args=[42]))

        # Assert: recarrega do banco e confere que ficou tudo vazio
        jogo.refresh_from_db()
        self.assertIsNone(jogo.nota)
        self.assertEqual(jogo.review, '')


class LoginRequiredTest(TestCase):
    def test_favoritos_exige_login(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_estante_exige_login(self):
        response = self.client.get(reverse('my_shelf'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)


class ModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='gamer', password='senha123')

    def test_str_do_favorito(self):
        fav = FavoriteGame.objects.create(user=self.user, game_id=1, name='Hollow Knight')
        self.assertEqual(str(fav), 'Hollow Knight')

    def test_str_do_status(self):
        status = GameStatus.objects.create(
            user=self.user, game_id=1, name='Elden Ring', status='jogando',
        )
        self.assertEqual(str(status), 'Elden Ring - jogando')

class GameDetailTest(TestCase):
    def setUp(self):
        # fetch_rawg guarda no cache; limpamos pra cada teste comecar do zero.
        cache.clear()

    @patch('games.views.requests.get')
    def test_mostra_jogos_relacionados(self, mock_get):
        # A view bate na RAWG 3 vezes, nesta ordem: jogo, screenshots, serie.
        # O side_effect em LISTA devolve um item por chamada, na ordem.
        mock_get.side_effect = [
            fake_response({'id': 3328, 'name': 'The Witcher 3'}),                  # 1) o jogo
            fake_response({'results': []}),                                        # 2) screenshots
            fake_response({'results': [{'id': 1, 'name': 'Thronebreaker'}]}),      # 3) a serie
        ]

        response = self.client.get(reverse('game_detail', args=[3328]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thronebreaker')