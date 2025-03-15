from colorama import Fore, Style

from lib.libForms.Form import *
from lib.libData.DataManager import *
import GlobalAssets as assets

def sendLoginFrom() -> None:
    
    from auth import Auth
    from auth.PlayerData import PlayerDataFields as fields

    def sendSignIn() -> None:
        form = InputForm("Sign In", settings=settings)
        form.registerTextInput("Username", tooltip="Leave empty to go back", validation=lambda input: "Invalid Username" if not Auth.doesUserExist(input.lower()) else False)
        username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower()
        if username == "":
            sendLoginFrom()

        form = InputForm("Sign In", settings=settings)
        form.addSeparator(f"Username: {username}")
        form.registerTextInput("Password", tooltip="Leave empty to go back", validation=lambda input: "Password Incorrect" if not input == assets.getPlayerManager().getData(username, fields.PASSWORD) else False)
        if form.send()["Password"][InputForm.DataEntryConsts.RESPONSE] == "":
            sendLoginFrom()

        assets.logged_in_player = username

    def sendSignUp() -> None:
        form = InputForm("Sign Up", settings=settings)
        form.registerTextInput("Username", tooltip="Leave empty to go back", validation=lambda input: "Username already exists" if Auth.doesUserExist(input.lower()) else False)
        username = form.send()["Username"][InputForm.DataEntryConsts.RESPONSE].lower()
        if username == "":
            sendLoginFrom()

        form = InputForm("Sign Up", settings=settings)
        form.addSeparator(f"Username: {username}")
        form.registerTextInput("Password", tooltip="Leave empty to go back")
        password = form.send()["Password"][InputForm.DataEntryConsts.RESPONSE]
        if password == "":
            sendLoginFrom()

        form = OptionForm("Confirm New User", f"Please confirm the below details:\n  - Username: {username}\n  - Password: {password}", settings=settings)

        def createPlayer():
            playerManager = assets.getPlayerManager()
            playerManager.createDatafile(username)
            playerManager.setData(username, fields.PASSWORD, password)
        form.addOption(Fore.GREEN + "✅ CONFIRM" + Style.RESET_ALL, createPlayer)

        form.addOption(Fore.RED + "❌ RETRY" + Style.RESET_ALL, sendSignUp)

        form.send()

        pass

    def registerGuest() -> None:
        pass

    assets.clear_console()
    settings = FormSettings()
    settings.editSetting(FormSettings.Setting.HEADER, f"{assets.getTitle()}\n\n<--------------🔒-------------->")
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)
    settings.editSetting(FormSettings.Setting.CLEAR_FORM_AFTER_FORM, True)

    form = OptionForm("Get Started", "Please log in to get started! You can also play as a temporary guest.", settings)
    form.addOption("🔐  Sign In", lambda: sendSignIn(), "Login to an existing account.")
    form.addOption("➕  Sign Up", lambda: sendSignUp(), "Create a new account.")
    form.addOption("👤  Play as Guest", lambda: registerGuest(), "You will be able to port your stats later on.")

    form.send()

    from GameManager import runGame
    runGame()

if __name__ == "__main__":
    sendLoginFrom()