from colorama import Fore, Style

from lib.libData.DataManager import *
from lib.libData.DataManager import DataFields
import GlobalAssets as assets

class LocalDataFields (DataFields):
    LAST_LOGGED_IN = 'last_logged_in'
    SETTINGS_CONST = 'settings'
    class Settings (Enum):
        """ Settings fields for the local data database. All formatted. """
        SHOW_HEARTS = 'Show Hearts'

    pass

class LocalDataManager (DataManager):
    _DATABASE_NAME = 'local_data'

    def __init__(self):
        super().__init__(os.path.join(os.path.dirname(__file__)), DataManager.DatabaseType.DICT)

        if not self.datafileExists(self._DATABASE_NAME):
            self.createDatafile(self._DATABASE_NAME)

    def getDefaultValues(self) -> dict:
        return {
            LocalDataFields.LAST_LOGGED_IN: None,
            LocalDataFields.SETTINGS_CONST: {
                LocalDataFields.Settings.SHOW_HEARTS.name: True
            }
        }

    def getDataField(self, field: DataFields) -> any:
        """ Gets a data field from the database. New function to not run into a method resolution order error. """
        return self.getData(self._DATABASE_NAME, field)

    def getData(self, identifier: str, key: DataFields = None):
        """ Check if the DataField is an instance of LocalDataFields.Settings """
        data = super().getData(identifier)  # Get the data from the parent class

        # Only handle LocalDataFields.Settings specifically
        if isinstance(key, LocalDataFields.Settings):
            return data[LocalDataFields.SETTINGS_CONST][key.name]  # Get the settings data

        # If not LocalDataFields.Settings, just return the regular data
        return data[key] if key is not None else data

    def setDataField(self, field: DataFields, newVal) -> None:
        """ Sets a value to a field in a datafile. Assumes the newVal is a valid value for the field. """
        self.setData(self._DATABASE_NAME, field, newVal)

    def setData(self, identifier: str, field: DataFields, newVal) -> None:
        # If the field is an instance of LocalDataFields.Settings, set the data under settings
        if isinstance(field, LocalDataFields.Settings):
            # Get the data from the file
            data = self.getData(identifier)

            # Ensure the "settings" key exists in the data
            if LocalDataFields.SETTINGS_CONST not in data:
                data[LocalDataFields.SETTINGS_CONST] = {}  # Initialize settings if not present

            # Set the new value under "settings" for the specific field
            data[LocalDataFields.SETTINGS_CONST][field.name] = newVal  # Use field.name for clarity

            # Get the formatted file path
            path = self.getFormattedFilename(identifier)

            # Write the updated data back to the file
            try:
                with open(path, 'w') as file:
                    json.dump(data, file, indent=4)
            except Exception as e:  # Handle any errors that occur during the file write
                raise DataManagerErrors.PathNotExists(str(e))
        else:
            # For other types of fields, call the parent class's setData method
            super().setData(identifier, field, newVal)