# Ballot-Manifest-2.0

## Installation
1. Install python 3.6 or newer
2. Run "pip install -r requirements.txt" in the source directory

## Export to .exe
1. Use PyInstaller
1a. https://github.com/brentvollebregt/auto-py-to-exe
2. In the python installation navigate to: /Lib/site-packages/PyInstaller/hooks
2a. Add hook.pandas.py
2b. include code: hiddenimports = ['pandas._libs.tslibs.timedeltas']
3. PyInstall settings:
3a. One File
3b. Window Based
3c. Select Icon and Logo Images as additional files
4 Run PyInstaller
5. Manually copy settings.json into directory with .exe