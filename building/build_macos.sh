#!/usr/bin/env bash
set -e

arch=$1
echo "Building macOS ${arch} target ..."

echo "Installing requirements ..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

echo "Generating i18n files ..."
python building/convert_i18n_zh.py
pyside6-lrelease i18n/SciHubEVA_*.ts

echo "Building with PyInstaller ..."
pyside6-rcc SciHubEVA.qrc -o scihub_eva/resources.py

rm -rf build-macOS-${arch}
rm -rf dist-macOS-${arch}
rm -rf "Sci-Hub EVA.spec"

pyinstaller app.py \
  --workpath "build-macOS-${arch}" \
  --distpath "dist-macOS-${arch}" \
  --hidden-import "socks" \
  --add-data "LICENSE:." \
  --add-data "building/macOS/qtquickcontrols2.conf:confs" \
  --add-data "building/macOS/SciHubEVA-icon.png:images" \
  --add-data "i18n/*.qm:i18n" \
  --name "Sci-Hub EVA" \
  --icon "building/macOS/SciHubEVA.icns" \
  --onedir \
  --windowed \
  --noupx \
  --target-arch ${arch}

cp building/macOS/Info.plist "dist-macOS-${arch}/Sci-Hub EVA.app/Contents"

echo "Post processing ..."
python building/post_process.py dist-macOS-${arch}

echo "Packaging with create-dmg ..."
create-dmg \
  --volname "Sci-Hub EVA" \
  --volicon "building/macOS/SciHubEVA-dmg.icns" \
  --background "building/macOS/SciHubEVA-dmg-background.png" \
  --window-pos 200 120 \
  --window-size 600 430 \
  --text-size 14 \
  --icon-size 100 \
  --icon "Sci-Hub EVA.app" 100 150 \
  --hide-extension "Sci-Hub EVA.app" \
  --app-drop-link 300 150 \
  --eula "LICENSE" \
  --format "ULFO" \
  "dist-macOS-${arch}/SciHubEVA-${arch}-latest.dmg" \
  "dist-macOS-${arch}/Sci-Hub EVA.app"

echo "Building macOS ${arch} target finished."
