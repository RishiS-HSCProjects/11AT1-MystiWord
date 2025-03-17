from colorama import Fore, Style

from lib.libForms.Form import *
from lib.libData.DataManager import *
import GlobalAssets as assets
from GameManager import runGame
from auth import PlayerData

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

            # print stats menu
            print(f"""
Stats:
  {Fore.LIGHTGREEN_EX}XP: {assets.getPlayerManager().getData(assets.logged_in_player, PlayerData.PlayerDataFields.XP)}{Style.RESET_ALL}
  Games Played: {assets.getPlayerManager().getGamesPlayed(assets.logged_in_player)}
  Wins: {assets.getPlayerManager().getData(assets.logged_in_player, PlayerData.PlayerDataFields.WINS)}
  Losses: {assets.getPlayerManager().getData(assets.logged_in_player, PlayerData.PlayerDataFields.LOSSES)}
  WLR: {assets.getPlayerManager().getWLR(assets.logged_in_player)}
            """)

            assets.pause(Style.DIM) # Pause console to observe stats.

            sendHomePage()
        form.addOption(Fore.YELLOW + "Stats", sendStatsMenu)

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
        form = InputForm("Sign In", settings=settings) # Creates a sign-in form
        form.registerTextInput( # Registers a text input with validation ensuring the user exists.
            "Username", # Input name
            tooltip="Leave empty to go back", # Tooltip for exit
            validation=lambda input: ( # Validation code
                "Username does not exist" if not Auth.doesUserExist(input.lower()) and input != "" else # Check that username does not exist (or is empty)
                ("Invalid Username: Please only use letters (a-z) in your username. Do not use spaces or other special characters."  if not input.isalnum() and input != "" else # Invalid if username is not alphanumeric 
                False # False means username is valid
                )

            )
        )
        username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower().replace(" ", "_") # Set username variable t0 full lowercase and remove spaces
        if username == "":
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

    def sendSignUp() -> None:
        """ Sends a sign in form to the user. """
        form = InputForm("Sign Up", settings=settings) # Creates a sign-up forms
        form.registerTextInput("Username", tooltip="Leave empty to go back", validation=lambda input: "Username already exists" if Auth.doesUserExist(input.lower()) else False) # Registers a text input with validation ensuring the user does not already exist.
        username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower() # Set username variable
        if username == "":
            sendLoginFrom() # If operation is aborted, go back to the Login Form.

        form = InputForm("Sign Up", settings=settings) # Re-creates the sign-up form
        form.addSeparator(f"Username: {username}") # Display username.
        form.registerTextInput("Password", tooltip="Leave empty to go back") # Registers a text input for the password
        password = form.send()["Password"][InputForm.DataEntryConsts.RESPONSE] # Set password variable
        if password == "":
            sendLoginFrom() # If operation is aborted, go back to the Login Form.

        form = OptionForm("Confirm New User", f"Please confirm the below details:\n  - Username: {username}\n  - Password: {password}", settings=settings) # Create confirmation form displaying the username and password

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
            form.setBody(f"Stats:\nXP: {playerManager.getData(assets.get_guest_identifier(), PlayerData.PlayerDataFields.XP)}")
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