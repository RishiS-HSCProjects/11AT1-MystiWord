from lib.libData.DataManager import *

class PlayerDataFields (DataFields):
    USERNAME = 'username'
    PASSWORD = 'password'
    XP = 'xp'
    pass

class PlayerDataErrors (DataManagerErrors):
    class UnknownPlayer(Exception):
        """
            This exception is raised when the game tries accessing an unknown player.
        """
        
        def __init__(self, identifier: str = None):
            super().__init__("Tried manipulating an unknown player" + (f": {str(identifier)}" if identifier else ""))

class PlayerDataManager (DataManager):
    def __init__(self):
        super().__init__(os.path.join(os.path.dirname(__file__), "players"), self.DatabaseType.DICT) # Define database properties

    def getDefaultValues(self) -> dict:
        return {
            PlayerDataFields.XP: 0 # Sets XP to 0 on new account creation
        }