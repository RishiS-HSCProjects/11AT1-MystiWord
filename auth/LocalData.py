from colorama import Fore, Style

from lib.libData.DataManager import *
from lib.libData.DataManager import DataFields

class LocalDataFields (DataFields):
    """ Enum class with datafields storing local data """
    LAST_LOGGED_IN = 'last_logged_in'
    SETTINGS_CONST = 'settings'
    class Settings (Enum):
        """ Settings fields for the local data database. All formatted for display. """
        SHOW_HEARTS = 'Show Hearts'
        AFTER_GAME_STATS = 'Display Stats after Game'

    pass

class LocalDataManager (DataManager):
    _DATABASE_NAME = 'local_data'

    def __init__(self):
        """ Initalise database manager. """
        super().__init__(os.path.join(os.path.dirname(__file__)), DataManager.DatabaseType.DICT) # Set directory path and database type.

        if not self.datafileExists(self._DATABASE_NAME): # Create datafile if not already exists.
            self.createDatafile(self._DATABASE_NAME) # Create datafile. Will replace empty file with default values.

    def getDefaultValues(self) -> dict:
        """ Get the default values for local data (to replace if field does not exist.) """
        return {
            LocalDataFields.LAST_LOGGED_IN: None,
            LocalDataFields.SETTINGS_CONST: {
                LocalDataFields.Settings.SHOW_HEARTS.name: True,
                LocalDataFields.Settings.AFTER_GAME_STATS.name: False,
            }
        }

    def getDataField(self, field: DataFields) -> any:
        """ Gets a data field from the database. New function to not run into a method resolution order error. """
        return self.getData(self._DATABASE_NAME, field)

    def getData(self, identifier: str, key: DataFields = None):
        """ Check if the DataField is an instance of LocalDataFields.Settings
            Strictly private function. Use `LocalDataManager.getDataField()`.
        """
        data = super().getData(identifier) # Get the data from the parent class

        # Only handle LocalDataFields.Settings specifically
        if isinstance(key, LocalDataFields.Settings):
            return data[LocalDataFields.SETTINGS_CONST][key.name] # Get the settings data

        # If not LocalDataFields.Settings, just return the regular data
        return data[key] if key is not None else data

    def setDataField(self, field: DataFields, newVal) -> None:
        """ Sets a value to a field in a datafile. Assumes the newVal is a valid value for the field. """
        self.setData(self._DATABASE_NAME, field, newVal) # Call set data with the database name as the identifier.

    def setData(self, identifier: str, field: DataFields, newVal) -> None:
        """ Set a data field within local_data.
            Strictly private function. Use `LocalDataManager.setDataField()`.
        """
        # If the field is an instance of LocalDataFields.Settings, set the data under settings
        if isinstance(field, LocalDataFields.Settings):
            data = self.getData(identifier) # Get the data from the file

            if LocalDataFields.SETTINGS_CONST not in data: # Ensure the "settings" key exists in the data
                data[LocalDataFields.SETTINGS_CONST] = {} # Initialize settings if not present

            # Set the new value under "settings" for the specific field
            data[LocalDataFields.SETTINGS_CONST][field.name] = newVal # Use field.name for clarity

            path = self.getFormattedFilename(identifier) # Get the formatted file path

            # Write the updated data back to the file
            try:
                with open(path, 'w') as file:
                    json.dump(data, file, indent=4)
            except Exception as e: # Handle any errors that occur during the file write
                raise DataManagerErrors.PathNotExists(str(e))
        else:
            # For other types of fields, call the parent class's setData method
            super().setData(identifier, field, newVal)