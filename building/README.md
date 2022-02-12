# Building

## macOS

1. Create a python environment.

   ```bash
   conda create -n python39 python=3.9
   conda activate python39
   ```

2. Install requirements.

   ```bash
   pip install -r requirements.txt
   ```

3. Update the translations. Install Qt first and make sure you can run `lupdate` and `lrelease` commands.

   ```bash
   # Generate translations source of QML files
   lupdate SciHubEVA.pro

   # Generate translations source of Python files
   pyside6-lupdate \
     scihub_eva/api/*.py \
     scihub_eva/ui/*.py \
     -ts i18n/SciHubEVA_zh_CN.ts

   # Do translations with Qt Linguist
   # ......

   # Traditional Chinese translation was done by opencc
   opencc -c s2twp -i i18n/SciHubEVA_zh_CN.ts -o i18n/SciHubEVA_zh_TW.ts
   opencc -c s2hk -i i18n/SciHubEVA_zh_CN.ts -o i18n/SciHubEVA_zh_HK.ts

   # Generate translations target
   lrelease i18n/SciHubEVA_*.ts
   ```

   Complied translations will be in `i18n` end with `.qm`.

4. Build with `PyInstaller`.

   ```bash
   rm -rf build-macOS
   rm -rf dist-macOS
   rm -f SciHubEVA.spec

   pyside6-rcc SciHubEVA.qrc -o scihub_eva/resources.py

   pyinstaller app.py \
     --workpath "build-macOS" \
     --distpath "dist-macOS" \
     --hidden-import "socks" \
     --hidden-import "PIL" \
     --add-data "LICENSE:." \
     --add-data "preferences/qtquickcontrols2.conf:preferences" \
     --add-data "images/SciHubEVA-icon.png:images" \
     --add-data "i18n/*.qm:i18n" \
     --name "SciHubEVA" \
     --icon "building/macOS/SciHubEVA.icns" \
     --onedir \
     --windowed \
     --noupx

   cp building/macOS/Info.plist dist-macOS/SciHubEVA.app/Contents

   # Post process
   python building/post_process.py
   ```

   `SciHubEVA.app` will be in `dist-macOS`.

5. Package with `appdmg`. Install [Node.js](https://nodejs.org) first, then run the following commands:

   ```bash
   brew install create-dmg

   create-dmg \
     --volname "Sci-Hub EVA" \
     --volicon "building/macOS/SciHubEVA-dmg.icns" \
     --background "building/macOS/SciHubEVA-dmg-background.png" \
     --window-pos 200 120 \
     --window-size 600 430 \
     --text-size 14 \
     --icon-size 100 \
     --icon "SciHubEVA.app" 100 150 \
     --hide-extension "SciHubEVA.app" \
     --app-drop-link 300 150 \
     --eula "LICENSE" \
     --format "UDBZ" \
     "dist-macOS/SciHubEVA.dmg" \
     "dist-macOS/SciHubEVA.app"
   ```

   `SciHubEVA.dmg` will be in `dist-macOS`.

## Windows

1. See setcion 1 in [macOS](#macOS).
2. See setcion 2 in [macOS](#macOS).
3. See setcion 3 in [macOS](#macOS).
4. Build with `PyInstaller`.

   ```powershell
   :: Install the latest develop version of PyInstaller

   rd /s /Q build-Windows
   rd /s /Q dist-Windows
   del /F /S /Q SciHubEVA.spec

   pyside6-rcc SciHubEVA.qrc -o scihub_eva/resources.py

   pyinstaller app.py ^
     --workpath "build-Windows" ^
     --distpath "dist-Windows" ^
     --hidden-import "socks" ^
     --hidden-import "PIL" ^
     --add-data "LICENSE;." ^
     --add-data "preferences/qtquickcontrols2.conf;preferences" ^
     --add-data "images/SciHubEVA-icon.png;images" ^
     --add-data "i18n/*.qm;i18n" ^
     --name "SciHubEVA" ^
     --icon "building/Windows/SciHubEVA.ico" ^
     --version-file "building/Windows/SciHubEVA.win.version" ^
     --windowed ^
     --clean ^
     --noupx

   :: Post process
   python building/post_process.py
   ```

   All compiled files will be in `dist-Windows\SciHubEVA`.

5. Package with Inno Setup. Install [Inno Setup 6](http://www.jrsoftware.org/isinfo.php) first and add installation directory to PATH. Download Chinese (Simplified) and Chinese (Traditional) translations from [here](http://www.jrsoftware.org/files/istrans/), and copy them to `INNO_SETUP_ROOT\Languages`.

   ```powershell
   ISCC.exe building/Windows/SciHubEVA.iss
   ```

   `SciHubEVA.exe` installer will be in the `dist-Windows`.

6. If you need a x86 version, please make sure you have a x86 version python environment, and modify the `SciHubEVA.iss` accordingly.

   ```text
   DefaultDirName={autopf64}\{#MyAppName} -> DefaultDirName={autopf32}\{#MyAppName}
   OutputBaseFilename=SciHubEVA-x64 -> OutputBaseFilename=SciHubEVA-x86
   ```
