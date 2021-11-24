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


with open(f'{addonPath}/config.json') as f:
  configData = json.load(f)

themeData = configData[configData['currentTheme']]

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
def options() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)

# create a new menu item, "test"
action = QAction("Colour Options", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, options)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

