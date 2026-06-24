from django.shortcuts import render, redirect
from decouple import config
import requests
from django.contrib.auth import login
from .models import FavoriteGame, GameStatus
from .forms import CadastroForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from datetime import date
# Create your views here.

API_KEY = config('RAWG_API_KEY')

def home(request):
    search = request.GET.get('search', '')
    platform = request.GET.get('platform', '')
    ordering = request.GET.get('ordering', '')
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1  

    if page < 1:
        page = 1  

    url = f'https://api.rawg.io/api/games?key={API_KEY}&page={page}'
    if search:
        url += f'&search={search}&search_precise=true'
    if platform:
        url += f'&parent_platforms={platform}'
    if ordering:
        url += f'&ordering={ordering}'
        if ordering == '-released':
            hoje = date.today().isoformat()
            url += f'&dates=1970-01-01,{hoje}'

    response = requests.get(url)
    data = response.json()

    return render(request, 'games/home.html', {
        'games': data['results'],
        'search': search,
        'platform': platform,
        'ordering': ordering,
        'page':page,
        'has_next': data['next'] is not None,
        'has_previous': data['previous'] is not None,
    })


def game_detail(request, game_id):
    url = f'https://api.rawg.io/api/games/{game_id}?key={API_KEY}'
    try:
        game = requests.get(url).json()
    except (requests.RequestException, ValueError):
        raise Http404("Não foi possível carregar este jogo.")

    # screenshots são um extra: se falharem, seguimos sem a galeria
    shots_url = f'https://api.rawg.io/api/games/{game_id}/screenshots?key={API_KEY}'
    try:
        screenshots = requests.get(shots_url).json().get('results', [])
    except (requests.RequestException, ValueError):
        screenshots = []

    current_status = None
    if request.user.is_authenticated:
        game_status = GameStatus.objects.filter(user=request.user, game_id=game_id).first()
        if game_status:
            current_status = game_status.status

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteGame.objects.filter(user=request.user, game_id=game_id).exists()

    return render(request, 'games/game_detail.html', {
        'game': game,
        'current_status': current_status,
        'screenshots': screenshots,
        'is_favorite': is_favorite,
        })


def register(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CadastroForm()
        
    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_favorite(request,game_id):
    url = f'https://api.rawg.io/api/games/{game_id}?key={API_KEY}'
    response = requests.get(url)
    game = response.json()

    FavoriteGame.objects.get_or_create(
        user=request.user,
        game_id=game['id'],
        defaults = {
            'name': game['name'],
            'background_image': game['background_image'],
            'released': game['released']
        }
    )
    return redirect('game_detail', game_id=game_id)


@login_required
def favorites(request):
    favorites= FavoriteGame.objects.filter(user=request.user)
    return render(request, 'games/favorites.html', {'favorites': favorites})


@login_required
def remove_favorite(request, game_id):
    FavoriteGame.objects.filter(user=request.user, game_id=game_id).delete()
    next_url = request.META.get('HTTP_REFERER')
    return redirect(next_url or 'favorites')


@login_required
def set_status(request, game_id):
    if request.method == "POST":
        status = request.POST.get("status")

        url = f'https://api.rawg.io/api/games/{game_id}?key={API_KEY}'
        response = requests.get(url)
        game = response.json()


        GameStatus.objects.update_or_create(
            user=request.user,
            game_id=game['id'],
            defaults={
                'name': game['name'],
                'background_image': game['background_image'],
                'status': status,
            }

        )
    return redirect('game_detail', game_id=game_id)

@login_required
def set_review(request, game_id):
    if request.method == "POST":
        game_status = GameStatus.objects.filter(user=request.user, game_id=game_id).first()
        if game_status:
            game_status.nota = request.POST.get("nota") or None
            game_status.review = request.POST.get("review", "")
            game_status.save()
    return redirect('my_shelf')   

@login_required
def my_shelf(request):
    quero = GameStatus.objects.filter(user=request.user, status='quero')
    jogando = GameStatus.objects.filter(user=request.user, status='jogando')
    zerei = GameStatus.objects.filter(user=request.user, status='zerei')

    total = quero.count() + jogando.count() + zerei.count()
    progresso = round(zerei.count() / total * 100) if total else 0

    return render(request, 'games/my_shelf.html', {
        'quero': quero,
        'jogando': jogando,
        'zerei': zerei,
        'total': total,
        'progresso': progresso,
    })