#!/usr/bin/env bash
set -e

arch=$1
echo "Building Linux ${arch} target ..."

echo "Installing requirements ..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

echo "Generating i18n files ..."
python building/convert_i18n_zh.py
pyside6-lrelease i18n/SciHubEVA_*.ts

echo "Building with PyInstaller ..."
pyside6-rcc SciHubEVA.qrc -o scihub_eva/resources.py

rm -rf build-Linux-${arch}
rm -rf dist-Linux-${arch}
rm -rf SciHubEVA.spec

pyinstaller app.py \
  --workpath "build-Linux-${arch}" \
  --distpath "dist-Linux-${arch}" \
  --hidden-import "socks" \
  --add-data "LICENSE:." \
  --add-data "building/Linux/qtquickcontrols2.conf:confs" \
  --add-data "building/Linux/SciHubEVA-icon.png:images" \
  --add-data "confs/ddos-guard-fake-mark.json:confs" \
  --add-data "i18n/*.qm:i18n" \
  --name "SciHubEVA" \
  --onedir \
  --windowed \
  --noupx \
  --target-arch ${arch}

echo "Post processing ..."
python building/post_process.py dist-Linux-${arch}

echo "Packaging with appimagetool ..."

export ARCH=${arch}

cp -r building/Linux/usr dist-Linux-${arch}/SciHubEVA/

icon_sizes=("8" "16" "22" "24" "32" "36" "42" "48" "64" "72" "96" "128" "256" "512")

for icon_size in "${icon_sizes[@]}"; do
  mkdir -p dist-Linux-${arch}/SciHubEVA/usr/share/icons/hicolor/${icon_size}x${icon_size}/apps
  rsvg-convert -h ${icon_size} -w ${icon_size} building/Linux/tech.leovan.SciHubEVA.svg > dist-Linux-${arch}/SciHubEVA/usr/share/icons/hicolor/${icon_size}x${icon_size}/apps/tech.leovan.SciHubEVA.png
done

mkdir -p dist-Linux-${arch}/SciHubEVA/usr/share/icons/hicolor/scalable/apps
cp building/Linux/tech.leovan.SciHubEVA.svg dist-Linux-${arch}/SciHubEVA/usr/share/icons/hicolor/scalable/apps/

cp -r building/Linux/AppRun-${arch} dist-Linux-${arch}/SciHubEVA/AppRun
cp -r building/Linux/usr/share/applications/tech.leovan.SciHubEVA.desktop dist-Linux-${arch}/SciHubEVA/
cp -r building/Linux/tech.leovan.SciHubEVA.svg dist-Linux-${arch}/SciHubEVA/
chmod 755 dist-Linux-${arch}/SciHubEVA/AppRun
appimagetool-${arch}.AppImage dist-Linux-${arch}/SciHubEVA dist-Linux-${arch}/SciHubEVA-${arch}-latest.AppImage

echo "Building Linux ${arch} target finished."
