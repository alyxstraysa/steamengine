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
import os
import pickle
from django.conf import settings



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
    elif query_type == 'get-distances':
        return get_distances(request)
    elif query_type == 'get-reviews':
        return get_reviews(request)
    elif query_type == 'get-tags':
        return get_tags(request)
    elif query_type == 'get-all-games':
        return get_all_games()
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

def get_all_games() -> HttpResponse:
    """
    Returns all games in the database
    """
    return JsonResponse({'games': [model_to_dict(game) for game in Game.objects.all()]})

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

def distances(X, base_ids, ids):
    sampled_vectors = X[:,base_ids]
    average_vector = np.sum(base_ids, axis=1)
    distances = np.linalg.norm(X.T - average_vector, axis=1)
    return distances[ids]

def get_recommendations(request: HttpRequest) -> HttpResponse:
    """
    Returns a list of game recommendations

    game-id: List of steam ids of games
    rec: Recommender to use
    max: Maximum number of recommendations to return
    """
    if 'game-id' in request.GET:
        game_list = from_game_ids(request.GET.getlist('game-id'))
        game_list = [x for x in game_list if x is not None]
    else:
        game_list = []
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

def get_distances(request: HttpRequest) -> HttpResponse:
    """
    Returns a list of game feature space distances

    base-id : Base steam id
    game-id: List of steam ids of games
    rec: Recommender to use
    """
    if 'base-id' not in request.GET:
        return JsonResponse({})
    base_id = from_game_ids([request.GET.get('base-id', 0)])
    if base_id is None:
        return JsonResponse({})
    if 'game-id' in request.GET:
        game_list = from_game_ids(request.GET.getlist('game-id'))
        game_list_ids = [(x, y) for x, y in zip(game_list,request.GET.getlist('game-id')) if x is not None]
        game_list = [p[0] for p in game_list_ids]
        game_ids = [p[1] for p in game_list_ids]
    else:
        game_list = []
    if len(game_list) == 0:
        return JsonResponse({})
    rec = request.GET.get('rec', 1)
    try:
        rec = int(rec)
    except:
        rec = 1
    if rec <= 0 or rec > 6:
        rec = (rec % 6) + 1
    file = os.path.join(settings.BASE_DIR, 'server', 'steamengine', 'recommender', 'X_%s.npy' % rec)
    X = np.load(file)
    d = distances(X, [base_id], game_list)
    print(game_ids)
    print(d)
    print({'distances': {x:d for d, x in zip(d, game_ids)}})
    return JsonResponse({'distances': {x:d for d, x in zip(d, game_ids)}})

def get_reviews(request: HttpRequest) -> HttpResponse:
    """
    Returns a list of game reviews

    game_ids:   List of Steam ids to use for recommendation
    """
    file = os.path.join(settings.BASE_DIR, 'server', 'steamengine', 'tags', 'reviews.pickle')

    steam_id = request.GET.get('steam-id', None)

    if steam_id is None:
        return JsonResponse({'tags': []})

    with open(file, 'rb') as pickled:
        review_dict = pickle.load(pickled)

        if steam_id not in review_dict:
            return JsonResponse({'tags': []})
        else:
            review = review_dict[steam_id]

            return JsonResponse({'review': review_dict[steam_id]})


def get_tags(request: HttpRequest) -> HttpResponse:
    """
    Returns a list of game tags

    game_id: Game Steam id
    num: Number of tags to return
    """
    file = os.path.join(settings.BASE_DIR, 'server', 'steamengine', 'tags', 'dill.pickle')

    steam_id = request.GET.get('steam-id', None)

    num = request.GET.get('max', 5)
    try:
        num = int(num)
    except:
        num = 5

    if steam_id is None:
        return JsonResponse({'tags': []})

    with open(file, 'rb') as pickled:
        steam_tag_dict = pickle.load(pickled)

        if steam_id not in steam_tag_dict:
            return JsonResponse({'tags': []})
        else:
            steam_tag_extracted = steam_tag_dict[steam_id]

            num = min(num, len(steam_tag_extracted))

            return JsonResponse({'tags': steam_tag_dict[steam_id][:num]})

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
