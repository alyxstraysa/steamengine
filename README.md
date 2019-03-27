# steamengine

## closest_5_games.json
Graph with games as nodes
Each game has an edge to the 5 other games whose playtimes are most highly covariant
Dictionary with keys 'nodes' and 'links' which contain the nodes and edges of the graph
Each node is a dictionary with an 'id' key
Each edge is a dictionary with a 'source' and 'target' key

## game_ids.json
List of Steam game ids in the order corresponding to the above graph
For example, index 0 of the array is '10', meaning that node 0 of the above graph corresponds to the game with Steam id 10 (Counter-Strike)
Use https://steamdb.info/app/<game_id>/graphs/, or the Item metadata file from https://cseweb.ucsd.edu/~jmcauley/datasets.html#steam_data to search for which game an id represents
