import GlobalAssets

player_manager = GlobalAssets.getPlayerManager()

def doesUserExist(username: str) -> bool:
    """ Returns if a user exists. """
    return player_manager.datafileExists(username)