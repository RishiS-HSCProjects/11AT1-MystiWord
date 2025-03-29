import GlobalAssets

player_manager = GlobalAssets.getPlayerManager() # Gets the player manager once.

def doesUserExist(username: str) -> bool:
    """ Returns if a user exists. """
    return player_manager.datafileExists(username)