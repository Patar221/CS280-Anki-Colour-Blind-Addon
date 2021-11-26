#aqt.utils.showInfo() -> For Debugging

#Imports
from aqt import mw
from aqt.addons import *
import json


######################################################################################################################################################
# The below code was taken and modifed from the Custom Background Image and Gear Icon Addon (https://ankiweb.net/shared/info/1210908941)
# I took the relevent portions that applied to what I needed and modified variable names to match my naming convention to make it easier to read
# Full credit to ijgnd and AnKingMed

addonPath = os.path.dirname(__file__)
addonFolderName = os.path.basename(addonPath)

webPath = os.path.join(addonPath, "web", "css")
userTemplatePath = os.path.join(addonPath, "user_files", "css_template") #Added by me to be referenced later
userPath = os.path.join(addonPath, "user_files", "css") #Added by me to be referenced later

regex = r"(user_files.*|web.*)"
mw.addonManager.setWebExports(__name__, regex)

cssFilesToReplace = [os.path.basename(f) for f in os.listdir(webPath) if f.endswith(".css")]

from anki.utils import pointVersion
def maybe_adjust_filename_for_2136(filename):
    if pointVersion() >= 36:
        filename = filename.lstrip("css/")
    return filename

def replace_css(webContent, context):
    edit_css_files() #Call function added by myself to modify css files

    for index, fileName in enumerate(webContent.css):
        fileName = maybe_adjust_filename_for_2136(fileName)
        if fileName in cssFilesToReplace:
            webContent.css[index] = f"/_addons/{addonFolderName}/web/css/{fileName}"
            webContent.css.append(f"/_addons/{addonFolderName}/user_files/css/custom_{fileName}")
gui_hooks.webview_will_set_content.append(replace_css)

######################################################################################################################################################

# Loops through config file to get current theme data
def get_current_theme(config):
    for theme in config['themes']:
        if currentTheme == theme['name']:
            return theme

with open(f'{addonPath}/config.json') as f:
  configData = json.load(f)

currentTheme = configData['currentTheme']
themes = configData['themes']
themeData = get_current_theme(configData)



def edit_css_files():
    #aqt.utils.showInfo(themeData['learnColour'])
    for fileName in os.listdir(userTemplatePath):
        if fileName.endswith(".css"):

            # Read in the file
            with open(f"{userTemplatePath}/{fileName}", 'r') as file:
                fileData = file.read()

            # Replace the target string
            fileData = fileData.replace('[newCountColour]', themeData['newColour'])
            fileData = fileData.replace('[learnCountColour]', themeData['learnColour'])
            fileData = fileData.replace('[reviewCountColour]', themeData['reviewColour'])

            # Write the file out again
            with open(f"{userPath}/{fileName}", 'w') as file:
                file.write(fileData)

#Menu Options
def changeTheme(theme) -> None:
    # Read in the file
    with open(f"{addonPath}/config.json", 'r') as file:
        fileData = file.read()

    # Replace the target string
    fileData = re.sub('(?<="currentTheme": ")(.*)(?=")', theme, fileData)

    # Write the file out again
    with open(f"{addonPath}/config.json", 'w') as file:
        file.write(fileData)

    aqt.utils.showInfo("Restart Anki to apply changes to the theme")

# Create CBM menu
menu = QMenu(('CBM'), mw)
mw.form.menubar.addMenu(menu)

# Add Theme Selector menu
themeSelect = QMenu("Select Theme", mw)
menu.addMenu(themeSelect)

general = QAction('General', mw)
general.triggered.connect(lambda: changeTheme('General'))
themeSelect.addAction(general)

deuteranopia = QAction('Deuteranopia', mw)
deuteranopia.triggered.connect(lambda: changeTheme('Deuteranopia'))
themeSelect.addAction(deuteranopia)

protanopia = QAction('Protanopia', mw)
protanopia.triggered.connect(lambda: changeTheme('Protanopia'))
themeSelect.addAction(protanopia)

tritanopia = QAction('Tritanopia', mw)
tritanopia.triggered.connect(lambda: changeTheme('Tritanopia'))
themeSelect.addAction(tritanopia)

monochromacy = QAction('Monochromacy', mw)
monochromacy.triggered.connect(lambda: changeTheme('Monochromacy'))
themeSelect.addAction(monochromacy)

# Currently does not work
# Used to dynamically create list of themes
'''
# Create list of themes
for theme in themes:
    themeName = theme['name']
    action = QAction(themeName, mw)
    action.triggered.connect(lambda: changeTheme(themeName))
    themeSelect.addAction(action)
'''

