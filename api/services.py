def get_developed_games(api_token_obj):
    developed_games = api_token_obj.first().developer.get_developed_games()
    serialized_games = []
    for game in developed_games:
        serialized_games.append({
            'name': game.name,
            'slug': game.slug,
            'price': game.price,
            'downloads': game.downloads,
            'plays': game.plays
        })
    return serialized_games
