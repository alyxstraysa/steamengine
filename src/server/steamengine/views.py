from __future__ import unicode_literals
import os
import numpy as np
import pickle
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
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
    elif query_type == 'get-recommendations':
        return get_recommendations(request)
    elif query_type == 'get-reviews':
        return get_reviews(request)
    elif query_type == 'get-tags':
        return get_tags(request)
    return JsonResponse({})

def get_game_by_id(request: HttpRequest) -> HttpResponse:
    """
    Look up game by steam id

    steam_id: Steam id of game
    """
    steam_id = request.GET.get('steam-id', None)
    if steam_id is None:
        return JsonResponse({'game': None})
    game = Game.objects.filter(steam_id=steam_id).first()
    if game is None:
        return JsonResponse({'game': None})
    return JsonResponse({'game': model_to_dict(game)})

def get_game_by_name(request: HttpRequest) -> HttpResponse:
    """
    Look up game by steam name

    name: Name of game
    """
    name = request.GET.get('name', None)
    if name is None:
        return JsonResponse({'game': None})
    game = Game.objects.filter(name=name).first()
    if game is None:
        return JsonResponse({'game': None})
    return JsonResponse({'game': model_to_dict(game)})

def from_game_ids(x):
    file = os.path.join(settings.BASE_DIR, 'server', 'steamengine', 'recommender', 'game_id_dict.dill')
    with open(file, 'rb') as f:
        game_id_dict = pickle.load(f)
    return [try_dict(game_id_dict, i) for i in x]

def to_game_ids(x):
    file = os.path.join(settings.BASE_DIR, 'server', 'steamengine', 'recommender', 'game_id_list.npy')
    game_id_list = np.load(file)
    return [game_id_list[i] for i in x]

def recommend(X, selected, n):
    sampled_vectors = X[:,selected]
    average_vector = np.sum(sampled_vectors, axis=1)
    distances = np.linalg.norm(X.T - average_vector, axis=1)
    ordered = np.argsort(distances)
    recommended = np.zeros(n, dtype=np.int)
    i = 0
    j = 0
    while i < n:
        if ordered[j] not in selected:
            recommended[i] = ordered[j]
            i += 1
        j += 1
    return recommended

def get_recommendations(request: HttpRequest) -> HttpResponse:
    """
    Returns a list of game recommendations

    game_list: List of steam ids of games
    rec:       Recommender to use
    max:       Maximum number of recommendations to return
    """
    if 'game-id' in request.GET:
        game_list = from_game_ids(request.GET.getlist('game-id'))
        game_list = [x for x in game_list if x is not None]
    else:
        games = []
    if len(game_list) == 0:
        return JsonResponse({'games': []})
    max_games = request.GET.get('max', 10)
    try:
        max_games = int(max_games)
    except:
        max_games = 10
    rec = request.GET.get('rec', 1)
    try:
        rec = int(rec)
    except:
        rec = 1
    if rec <= 0 or rec > 6:
        rec = (rec % 6) + 1
    file = os.path.join(settings.BASE_DIR, 'server', 'steamengine', 'recommender', 'X_%s.npy' % rec)
    X = np.load(file)
    recommended = recommend(X, game_list, max_games)
    recommended_ids = to_game_ids(recommended)
    return JsonResponse({'games': recommended_ids})

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

def try_call(f, x):
    try:
        return f(x)
    except:
        return None

def try_dict(d, x):
    if x in d:
        return d[x]
    else:
        return None
