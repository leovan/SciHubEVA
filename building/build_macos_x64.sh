#!/usr/bin/env bash

echo "Install requirements"
pip install -r requirements.txt
pip install -r requirements-dev.txt

echo "Generate i18n files"
python building/convert_i18n_zh.py
pyside6-lrelease i18n/SciHubEVA_*.ts

echo "Build with PyInstaller"
pyside6-rcc SciHubEVA.qrc -o scihub_eva/resources.py

rm -rf build-macOS-x64
rm -rf dist-macOS-x64
rm -rf SciHubEVA.spec

pyinstaller app.py \
  --workpath "build-macOS-x64" \
  --distpath "dist-macOS-x64" \
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
  --noupx \
  --target-arch x86_64

cp building/macOS/Info.plist dist-macOS-x64/SciHubEVA.app/Contents

echo "Post process"
python building/post_process.py dist-macOS-x64

echo "Package with create-dmg"
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
  --format "ULFO" \
  "dist-macOS-x64/SciHubEVA-x64-latest.dmg" \
  "dist-macOS-x64/SciHubEVA.app"
