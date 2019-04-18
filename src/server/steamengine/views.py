from __future__ import unicode_literals
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import *

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {})

def query(request: HttpRequest) -> HttpResponse:
    query_type = request.GET.get('query-type', None)
    if query_type is None:
        return JsonResponse({})
    elif query_type == 'get-game-by-steam-id':
        return get_game_by_id(request)
    elif query_type == 'get-game-by-name':
        return get_game_by_name(request)

def get_game_by_id(request: HttpRequest) -> HttpResponse:
    """
    Look up game by steam id

    steam_id: Steam id of game
    """
    steam_id = request.GET.get('steam-id', None)
    if steam_id is None:
        return JsonResponse({'game': None})
    print(steam_id)
    if steam_id == '0':
        game = Game(id=0, name="Test Game", steam_id=0, price=0.00)
    else:
        game = Game.objects.filter(steam_id=steam_id).first()
    if game is None:
        return JsonResponse({'game': None})
    return JsonResponse({'game': model_to_dict(game)})

def get_game_by_name(request: HttpRequest) -> HttpResponse:
    """
    Look up game by steam name
    """
    game_name = request.GET.get('game-name', None)
    if game_name is None:
        return JsonResponse({'game': None})
    print(game_name)
    if game_name == 'Test Game':
        game = Game(id=0, name="Test Game", steam_id=0, price=0.00)
    else:
        game = Game.objects.filter(name=game_name).first()
    if game is None:
        return JsonResponse({'game': None})
    return JsonResponse({'game': model_to_dict(game)})

def get_recommendations(request: HttpRequest) -> HttpResponse:
    """
    Returns a list of game recommendations

    game_list: List of steam ids of games
    filter_ids: List of Steam ids to filter
    genres:    List of genres to filter
    num:       Maximum number of recommendations to return
    """
    pass

def get_reviews(request: HttpRequest) -> HttpResponse:
    """
    Returns a list of game reviews

    game_ids:   List of Steam ids to use for recommendation
    filter_ids: List of Steam ids to filter
    num:        Maximum number of reviews to return
    """
    pass

def get_tags(request: HttpRequest) -> HttpResponse:
    """
    Returns a list of game tags

    game_id: Game Steam id
    num: Number of tags to return
    """
    pass



def safe_cast(val, typ, default):
    try:
        return typ(val)
    except ValueError:
        return default
