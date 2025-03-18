from colorama import Fore, Style

from lib.libData.DataManager import *
from lib.libData.DataManager import DataFields
import GlobalAssets as assets

class LocalDataFields (DataFields):
    LAST_LOGGED_IN = 'last_logged_in'
    pass

class LocalDataManager (DataManager):

    _DATABASE_NAME = 'local_data'

    def __init__(self):
        super().__init__(os.path.dirname(__file__), DataManager.DatabaseType.DICT)

        if not self.datafileExists(self._DATABASE_NAME):
            self.createDatafile(self._DATABASE_NAME)
    
    def getDefaultValues(self) -> dict:
        return {
            LocalDataFields.LAST_LOGGED_IN: None
        }

    def getDataField(self, field: DataFields) -> any:
        """ Gets a data field from the database. New function to not run into a method resolution order error. """
        return super().getData(self._DATABASE_NAME, field)

    def setData(self, field: DataFields, newVal) -> None:
        return super().setData(self._DATABASE_NAME, field, newVal) # Default the database name to the local data database (as this manager is only managing one file)
