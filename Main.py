from colorama import Fore, Style

from lib.libForms.Form import *
from lib.libData.DataManager import *
import GlobalAssets as assets
from GameManager import runGame, WordManager
from auth import PlayerData, LocalData

def sendHomePage() -> None:
    assets.clear_console() # Clears the console
    settings = FormSettings() # Initialises common form settings
    settings.editSetting(FormSettings.Setting.HEADER, assets.getTitle())
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)

    if (assets.logged_in_player): # Returns true if logged_in_player is not None (therefore, logged in)
        form = OptionForm(f"Hello, {assets.logged_in_player}", settings=settings) # Greats logged in player
        form.addOption(Fore.GREEN + "Play", runGame) # Opens game menu.

        def sendStatsMenu() -> None:
            assets.clear_console()

            print(assets.getTitle())

            playerManager = assets.getPlayerManager() # Get player manager
            getData = lambda field: playerManager.getData(assets.logged_in_player, field) # Get player data

            # print stats menu
            print(f"""
Stats:
  {Fore.LIGHTGREEN_EX}XP: {getData(PlayerData.PlayerDataFields.XP)}{Style.RESET_ALL}
  Games Played: {playerManager.getGamesPlayed(assets.logged_in_player)}
  Wins: {getData(PlayerData.PlayerDataFields.WINS)}
  Losses: {getData(PlayerData.PlayerDataFields.LOSSES)}
  WLR: {playerManager.getWLR(assets.logged_in_player)}
  Points per Win Average: {round(int(getData(PlayerData.PlayerDataFields.XP)) / int(getData(PlayerData.PlayerDataFields.WINS)), 2) if int(getData(PlayerData.PlayerDataFields.WINS)) > 0 else "N/A"}
  Easy PB: {playerManager.getPB(assets.logged_in_player, WordManager.Difficulties.EASY.value) or "N/A"}
  Medium PB: {playerManager.getPB(assets.logged_in_player, WordManager.Difficulties.MEDIUM.value) or "N/A"}
  Hard PB: {playerManager.getPB(assets.logged_in_player, WordManager.Difficulties.HARD.value) or "N/A"}
            """)

            assets.pause(Style.DIM) # Pause console to observe stats.

            sendHomePage()
        form.addOption(Fore.YELLOW + "Stats", sendStatsMenu)

        def sendSettingsMenu() -> None:
            form = OptionForm("Settings", "Enter a setting option to toggle it.", settings)
            form.settings.editSetting(FormSettings.Setting.HEADER, f"{assets.getTitle()}\n\n<--------------⚙️-------------->")

            local = assets.getLocalData() # Get local data

            def toggleSetting(setting: LocalData.LocalDataFields.Settings) -> None:
                local.setDataField(setting, not local.getDataField(setting)) # Toggle the setting
                sendSettingsMenu() # Refresh the settings menu

            for setting in LocalData.LocalDataFields.Settings: # Loop through all settings
                form.addOption(Fore.LIGHTBLUE_EX + setting.value, lambda self=None, setting=setting: toggleSetting(setting), local.getDataField(setting) and Fore.GREEN + "✅" or Fore.RED + "❌") # Add option to toggle the setting

            if (assets.logged_in_player == assets.get_guest_identifier()): # If the player is a guest
                def portStats() -> None:
                    portStatsSettings = settings # Copy instance of settings
                    portStatsSettings.editSetting(FormSettings.Setting.HEADER, f"{assets.getTitle()}\n\n<--------------🔁-------------->")
                    form = InputForm("Port Stats", settings=portStatsSettings) # Create input form

                    form.registerTextInput("Username", validation=lambda input: ("Username already exists" if assets.getPlayerManager().datafileExists(input) else False) or ("Invalid Username: Please only use letters (a-z) in your username. Do not use spaces or other special characters." if not input.isalnum() else False))
                    username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower() # Set username variable
                    
                    form = InputForm("Port Stats", settings=portStatsSettings) # Create input form
                    form.addSeparator(f"Username: {username}") # Display username.
                    form.registerTextInput("Password") # Registers a text input for the password
                    password = form.send()["Password"][InputForm.DataEntryConsts.RESPONSE] # Set password variable

                    form = OptionForm("Confirm New Account", f"Please confirm the below details:\n  - Username: {username}\n  - Password: {password if password else Fore.RED + 'NOT SET' + Style.RESET_ALL}", settings=settings) # Create confirmation form displaying the username and password
                    form.addOption(Fore.GREEN + "✅ CONFIRM" + Style.RESET_ALL, lambda: None) # Adds option to confirm the new account.
                    form.addOption(Fore.RED + "❌ Cancel" + Style.RESET_ALL, sendSettingsMenu) # Adds option to retry sign-up.
                    form.send() # Sends form to player

                    playerManager = assets.getPlayerManager()
                    playerManager.renameDatafile(assets.get_guest_identifier(), username) # Rename the guest datafile to the new username
                    playerManager.setData(username, PlayerData.PlayerDataFields.IDENTIFIER, username) # Set the password for the new account
                    playerManager.setData(username, PlayerData.PlayerDataFields.PASSWORD, password) # Set the password for the new account
                    assets.logged_in_player = username # Set the logged in player to the new username
                    sendHomePage() # Return to the home page

                form.addSeparator() # Add a separator
                form.addOption(Fore.LIGHTCYAN_EX + "Port Guest Stats", lambda: portStats(), "Port guest stats to a new player.") # Add option to port guest stats

            form.addOption(Fore.RED + "🔴 Back", sendHomePage) # Adds option to go back to the home page

            form.send()
        form.addOption(Fore.LIGHTBLUE_EX + "Settings", sendSettingsMenu)

        def logout() -> None:
            form = OptionForm(f"Hey, {assets.logged_in_player}!", Fore.LIGHTRED_EX + "Are you sure you want to log out?", settings=settings) # Create confirmation form for the logout
            def handleLogout() -> None:
                assets.logged_in_player = None  # Properly log out the user
            form.addOption(Fore.GREEN + "✅ CONFIRM" + Style.RESET_ALL, handleLogout) # Adds option to confirm the new account. 
            form.addOption(Fore.RED + "❌ Back" + Style.RESET_ALL, lambda: None) # Adds option to retry sign-up.
            form.send()
            sendHomePage()
        form.addOption(Fore.RED + "Log Out", logout)
        form.send()
    else:
        sendLoginFrom()

def sendLoginFrom() -> None:
    
    from auth import Auth
    from auth.PlayerData import PlayerDataFields as fields

    def sendSignIn() -> None:
        """ Sends a sign in form to the user. """

        last_logged_in = assets.getLocalData().getDataField(LocalData.LocalDataFields.LAST_LOGGED_IN) # Get the last logged in player

        form = InputForm("Sign In", settings=settings) # Creates a sign-in form
        form.registerTextInput( # Registers a text input with validation ensuring the user exists.
            "Username", # Input name
            tooltip=f"Leave empty to autofil to '{Fore.CYAN + last_logged_in + Fore.RESET}'" if last_logged_in else "Leave empty to go back", # Tooltip for exit/autofill
            validation=lambda input: ( # Validation code
                "Username does not exist" if not Auth.doesUserExist(input.lower()) and input != "" else # Check that username does not exist (or is empty)
                ("Invalid Username: Please only use letters (a-z) in your username. Do not use spaces or other special characters."  if not input.isalnum() and input != "" else # Invalid if username is not alphanumeric 
                False # False means username is valid
                )

            )
        )
        username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower().replace(" ", "_") # Set username variable t0 full lowercase and remove spaces
        if username == "":
            if last_logged_in:
                username = last_logged_in
            else:
                sendLoginFrom() # If operation is aborted, go back to the Login Form.

        form = InputForm("Sign In", settings=settings) # Re-create sign-in form if username passed validation
        form.addSeparator(f"Username: {username}") # Display username.
        try:
            form.registerTextInput("Password", tooltip="Leave empty to go back", validation=lambda input: "Password Incorrect" if not input == assets.getPlayerManager().getData(username, fields.PASSWORD) and input != "" else False) # Registers a text input with validation ensuring the password is correct.
            if form.send()["Password"][InputForm.DataEntryConsts.RESPONSE] == "":
                sendLoginFrom() # If operation is aborted, go back to the Login Form.
        except json.decoder.JSONDecodeError:
            print(Fore.RED + "File corrupted. Please sign up for a new account.\n" + Style.RESET_ALL) # Sends warning
            os.system('pause')

            assets.getPlayerManager().deleteDatafile(username)

            sendSignUp()
            return

        assets.logged_in_player = username # Set the logged in player to this player. Username acts as the player identifier.
        assets.getLocalData().setDataField(LocalData.LocalDataFields.LAST_LOGGED_IN, username) # Set the last logged in player to this player.

    def sendSignUp() -> None:
        """ Sends a sign in form to the user. """
        form = InputForm("Sign Up", settings=settings) # Creates a sign-up forms
        form.registerTextInput("Username", tooltip="Leave empty to go back", validation=lambda input: "Username already exists" if Auth.doesUserExist(input.lower()) else False) # Registers a text input with validation ensuring the user does not already exist.
        username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower() # Set username variable
        if username == "":
            sendLoginFrom() # If operation is aborted, go back to the Login Form.

        form = InputForm("Sign Up", settings=settings) # Re-creates the sign-up form
        form.addSeparator(f"Username: {username}") # Display username.
        form.registerTextInput("Password") # Registers a text input for the password
        password = form.send()["Password"][InputForm.DataEntryConsts.RESPONSE] # Set password variable

        form = OptionForm("Confirm New User", f"Please confirm the below details:\n  - Username: {username}\n  - Password: {password if password else Fore.RED + 'NOT SET' + Style.RESET_ALL}", settings=settings) # Create confirmation form displaying the username and password

        def createPlayer():
            """ Creates a player datafile """
            playerManager = assets.getPlayerManager() # Get player manager 
            playerManager.createDatafile(username) # Create the datafile. This will automatically add the default values.
            playerManager.setData(username, fields.PASSWORD, password) # Set the password to the datafile.
        form.addOption(Fore.GREEN + "✅ CONFIRM" + Style.RESET_ALL, createPlayer) # Adds option to confirm the new account. 

        form.addOption(Fore.RED + "❌ RETRY" + Style.RESET_ALL, sendSignUp) # Adds option to retry sign-up.

        form.send() # Sends form to player

        pass

    def registerGuest() -> None:
        """ Opens terminal for a guest """

        playerManager = assets.getPlayerManager() # Assigns player manager

        guest_exists = playerManager.datafileExists(assets.get_guest_identifier()) # Checks if guest datafile already exists

        def createGuestProfile() -> None:
            if guest_exists: 
                playerManager.deleteDatafile(assets.get_guest_identifier()) # Deletes existing datafile
            
            playerManager.createDatafile(assets.get_guest_identifier()) # Creates a new stock datafile
            
        if guest_exists: 
            form = OptionForm("Create Guest Profile", "A guest profile already exists. Would you like to continue using that?", settings) # Option form to override guest profile
            form.setBody(f"""Stats:
  XP: {playerManager.getData(assets.get_guest_identifier(), PlayerData.PlayerDataFields.XP)}
  Games Played: {playerManager.getGamesPlayed(assets.get_guest_identifier())}""") # Display guest stats
            form.addOption(Fore.GREEN + "✅  Yes, continue guest account!" + Style.RESET_ALL, lambda: None) # Continues with existing profile
            form.addOption(Fore.RED + "❌  No, reset stats and create a new guest account!" + Style.RESET_ALL, createGuestProfile) # Overrides profile
            form.addOption(Fore.LIGHTBLACK_EX + "Back to Login Page", lambda: sendHomePage())

            form.send() # Sends form
        else:
            createGuestProfile() # Creates guest profile
    
        assets.logged_in_player = assets.get_guest_identifier()
        sendHomePage()

        pass

    assets.clear_console() # Clears the console
    settings = FormSettings() # Initialises common form settings
    settings.editSetting(FormSettings.Setting.HEADER, f"{assets.getTitle()}\n\n<--------------🔒-------------->")
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)

    form = OptionForm("Get Started", "Please log in to get started! You can also play as a temporary guest.", settings) # Create Login Options Form
    form.addOption("🔐  Sign In", lambda: sendSignIn(), "Login to an existing account.") # Sign in option
    form.addOption("➕  Sign Up", lambda: sendSignUp(), "Create a new account.") # Sign up option
    form.addOption("👤  Play as Guest", lambda: registerGuest(), "You will be able to port your stats later on.") # Play as guest option
    form.addOption("🔴  Exit", lambda: exit()) # Quit app if this option is selected

    form.send() # Sends the form

    sendHomePage() # Open home page unless any process is aborted.

if __name__ == "__main__":
    assets.logged_in_player = None # Logs out player
    sendHomePage() # If file is opened from the CMD, it will open the login form first (as no player is signed in).