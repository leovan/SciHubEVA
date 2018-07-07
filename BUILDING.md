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
   
   # Update translations
   
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
     --hidden-import "PyQt5.sip" \
     --hidden-import "PyQt5.Qt" \
     --hidden-import "PyQt5.QtQuick" \
     --add-data "LICENSE:." \
     --add-data "SciHubEVA.conf:." \
     --add-data "images/SciHubEVA.png:images" \
     --add-data "translations/SciHubEVA_zh_CN.qm:translations" \
     --name "SciHubEVA" \
     --icon "images/SciHubEVA.icns" \
     --noupx
   
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

# Windows

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
   
   # Update translations
   
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
     --hidden-import "PyQt5.sip" ^
     --hidden-import "PyQt5.Qt" ^
     --hidden-import "PyQt5.QtQuick" ^
     --add-data "LICENSE;." ^
     --add-data "SciHubEVA.conf;." ^
     --add-data "images/SciHubEVA.png;images" ^
     --add-data "translations/SciHubEVA_zh_CN.qm;translations" ^
     --name "SciHubEVA" ^
     --icon "images/SciHubEVA.ico" ^
     --version-file "SciHubEVA.win.version" ^
     --noupx
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

# Linux

1. Create a python environment

   ```{bash}
   conda create -n python35 python=3.5
   activate python35
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
   
   # Update translations
   
   lrelease SciHubEVA.pro
   ```

   Complied translations will be in `translations` ends with `.qm`.

4. Building with `pyinstaller`

   **Note:** When building you may get errors of `Python library not found`, then you need put the python library to you `$LD_LIBRARY_PATH` by:

   ```{bash}
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/python/root/lib
   ```

   ```{bash}
   pip install PyInstaller
   
   rm -rf build
   rm -rf dist
   rm -f SciHubEVA.spec
   
   rm -f scihub_resources.py
   pyrcc5 SciHubEVA.qrc -o scihub_resources.py
   
   pyinstaller -w scihub_eva.py \
     --hidden-import "PyQt5.sip" \
     --hidden-import "PyQt5.Qt" \
     --hidden-import "PyQt5.QtQuick" \
     --add-data "LICENSE:." \
     --add-data "SciHubEVA.conf:." \
     --add-data "images/SciHubEVA.png:images" \
     --add-data "translations/SciHubEVA_zh_CN.qm:translations" \
     --name "SciHubEVA" \
     --noupx
   ```

   All compiled files will be in `dist\SciHubEVA`.

5. Packaing with AppImage

   Install the `appimagetool` from [**AppImageKit**](https://github.com/AppImage/AppImageKit) and prepare the `SciHubEVA.AppDir` for AppImage.

   ```{bash}
   cd dist
   
   # Download appimagetool and make it executable
   chmod u+x appimagetool-*.AppImage
   
   # Make AppDir
   mkdir SciHubEVA.AppDir
   mkdir SciHubEVA.AppDir/usr
   mkdir SciHubEVA.AppDir/usr/bin
   mkdir SciHubEVA.AppDir/usr/lib
   mkdir SciHubEVA.AppDir/usr/share
   mkdir SciHubEVA.AppDir/usr/share/applications
   mkdir SciHubEVA.AppDir/usr/share/icons
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/512x512
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/512x512/apps
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/256x256
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/256x256/apps
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/128x128
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/128x128/apps
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/64x64
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/64x64/apps
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/48x48
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/48x48/apps
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/24x24
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/24x24/apps
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/22x22
   mkdir SciHubEVA.AppDir/usr/share/icons/hicolor/22x22/apps
   mkdir SciHubEVA.AppDir/usr/share/metainfo
   
   cp -r SciHubEVA/* SciHubEVA.AppDir/usr/bin
   cp ../SciHubEVA.desktop SciHubEVA.AppDir
   cp ../SciHubEVA.desktop SciHubEVA.AppDir/usr/share/applications
   cp ../images/SciHubEVA.png SciHubEVA.AppDir
   cp ../SciHubEVA.appdata.xml SciHubEVA.AppDir/usr/share/metainfo
   
   convert -resize 512 SciHubEVA.AppDir/SciHubEVA.png SciHubEVA.AppDir/usr/share/icons/hicolor/512x512/apps/SciHubEVA.png
   convert -resize 256 SciHubEVA.AppDir/SciHubEVA.png SciHubEVA.AppDir/usr/share/icons/hicolor/256x256/apps/SciHubEVA.png
   convert -resize 128 SciHubEVA.AppDir/SciHubEVA.png SciHubEVA.AppDir/usr/share/icons/hicolor/128x128/apps/SciHubEVA.png
   convert -resize 64 SciHubEVA.AppDir/SciHubEVA.png SciHubEVA.AppDir/usr/share/icons/hicolor/64x64/apps/SciHubEVA.png
   convert -resize 48 SciHubEVA.AppDir/SciHubEVA.png SciHubEVA.AppDir/usr/share/icons/hicolor/48x48/apps/SciHubEVA.png
   convert -resize 24 SciHubEVA.AppDir/SciHubEVA.png SciHubEVA.AppDir/usr/share/icons/hicolor/24x24/apps/SciHubEVA.png
   convert -resize 22 SciHubEVA.AppDir/SciHubEVA.png SciHubEVA.AppDir/usr/share/icons/hicolor/22x22/apps/SciHubEVA.png
   
   cd SciHubEVA.AppDir
   ln -s usr/bin/SciHubEVA AppRun
   cd ..
   
   ./appimagetool-*.AppImage SciHubEVA.AppDir --no-appstream
   ```
