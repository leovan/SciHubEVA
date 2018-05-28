# macOS

1. Create a python environment

   ```{bash}
   conda create -n python35 python=3.5
   source activate python35
   ```

2. Install requirements

   ```{bash}
   pip install -r requirements.txt
   ```

   **Note:** `pdfminer.six` will automatically install `pycryptodome` which may cause error when building, you should replace it with `pycryptodomex`.

   ```{bash}
   pip uninstall pycryptodome
   pip install pycryptodomex
   ```

3. Update the translations

   Install Qt first and make sure you can run `lupdate` and `lrelease` commands.

   ```{bash}
   lupdate SciHubEVA.pro
   pylupdate5 SciHubEVA.pro
   lrelease SciHubEVA.pro
   ```

   Complied translations will be in `translations` ends with `.qm`.

4. Building with `pyinstaller`

   ```{bash}
   pip install PyInstaller

   rm -rf build
   rm -rf dist
   rm -f SciHubEVA.spec
   
   rm -f scihub_resources.py
   pyrcc5 SciHubEVA.qrc -o scihub_resources.py
   
   pyinstaller -w scihub_eva.py \
     --hidden-import "PyQt5.Qt" \
     --hidden-import "PyQt5.QtQuick" \
     --add-data "LICENSE:." \
     --add-data "SciHubEVA.conf:." \
     --add-data "images/SciHubEVA.png:images" \
     --add-data "translations/SciHubEVA_zh_CN.qm:translations" \
     --name "SciHubEVA" \
     --icon "images/SciHubEVA.icns"
   
   cp Info.plist dist/SciHubEVA.app/Contents
   ```

   `SciHubEVA.app` will be in `dist`.

5. Packaing with `appdmg`

   Install [Node.js](https://nodejs.org) first.

   ```{bash}
   npm install -g appdmg

   appdmg SciHubEVA.dmg.json dist/SciHubEVA.dmg
   ```

   `SciHubEVA.dmg` will be in `dist`.

# WINDOWS

1. Create a python environment

   ```{bat}
   conda create -n python35 python=3.5
   activate python35
   ```

2. Install requirements

   ```{bat}
   pip install -r requirements.txt
   ```

   **Note:** `pdfminer.six` will automatically install `pycryptodome` which may cause error when building, you should replace it with `pycryptodomex`.

   ```{bat}
   pip uninstall pycryptodome
   pip install pycryptodomex
   ```

3. Update the translations

   Install Qt first and make sure you can run `lupdate` and `lrelease` commands.

   ```{bash}
   lupdate SciHubEVA.pro
   pylupdate5 SciHubEVA.pro
   lrelease SciHubEVA.pro
   ```

   Complied translations will be in `translations` ends with `.qm`.

4. Building with `pyinstaller`

   ```{dos}
   pip install PyInstaller
   
   rd /s /Q build
   rd /s /Q dist
   del /Q SciHubEVA.spec
   
   del /Q scihub_resources.py
   pyrcc5 SciHubEVA.qrc -o scihub_resources.py
   
   pyinstaller -w scihub_eva.py ^
     --hidden-import "PyQt5.Qt" ^
     --hidden-import "PyQt5.QtQuick" ^
     --add-data "LICENSE;." ^
     --add-data "SciHubEVA.conf;." ^
     --add-data "images/SciHubEVA.png;images" ^
     --add-data "translations/SciHubEVA_zh_CN.qm;translations" ^
     --name "SciHubEVA" ^
     --icon "images/SciHubEVA.ico" ^
     --version-file "SciHubEVA.win.version"
   ```

   All compiled files will be in `dist\SciHubEVA`.

5. Packaing with NSIS

   Install [NSIS](http://nsis.sourceforge.net) first and add installation directory to PATH.

   ```{bash}
   makensis SciHubEVA.nsi
   ```

   `SciHubEVA.exe` installer will be in the `dist`.

6. x86 version

   If you need a x86 version, please make sure you have a x86 version python environment, and modify the `SciHubEVA.nsi` accordingly.

   ```{text}
   OutFile "dist\SciHubEVA-x64.exe" -> OutFile "dist\SciHubEVA-x86.exe"
   InstallDir "$PROGRAMFILES64\${PRODUCT_NAME}" -> InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"
   ```
