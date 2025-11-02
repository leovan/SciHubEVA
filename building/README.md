# Building

## macOS

> [!NOTE]
> Require macOS 10.15+, x86_64 and arm64 arch are tested.

1. Create a python environment.
2. Install requirements.

   ```shell
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. Update the translations.

   ```shell
   pyside6-lupdate \
     scihub_eva/api/*.py \
     scihub_eva/ui/*.py \
     ui/*.qml \
     ui/elements/*.qml \
     -ts i18n/SciHubEVA_zh_CN.ts \
     -ts i18n/SciHubEVA_pt_PT.ts

   pyside6-lrelease i18n/SciHubEVA_*.ts
   ```

4. Install [create-dmg](https://github.com/create-dmg/create-dmg).

   ```shell
   brew install create-dmg
   ```

5. Build and package.

   ```shell
   ./building/build_macos.sh ${arch}
   ```

   `SciHubEVA-${arch}-latest.dmg` will be in `dist-macOS-${arch}`.

## Windows

> [!NOTE]
> Require Windows 10+, x86_64 arch is tested.

1. See step 1 in [macOS](#macos).
2. See step 2 in [macOS](#macos).
3. See step 3 in [macOS](#macos).
4. Install [Inno Setup](https://jrsoftware.org/isinfo.php) and make sure `ISCC.exe` is in your `PATH`.
5. Build and package.

   ```powershell
   ./building/build_windows.ps1 ${arch}
   ```

   `SciHubEVA-${arch}-latest.exe` will be in `dist-Windows-${arch}`.

## Linux

> [!NOTE]
> Require Ubuntu 22.04+, x86_64 arch is tested.

1. See step 1 in [macOS](#macos).
2. See step 2 in [macOS](#macos).
3. See step 3 in [macOS](#macos).
4. Install system packages.

   ```shell
   sudo apt install -y binutils librsvg2-bin libfuse2 libgl1-mesa-dev libxcb* libxau-dev liblzma-dev libegl-dev
   ```

5. Install [appimagetool](https://appimage.github.io/appimagetool/) and make sure `appimagetool-x86_64.AppImage` is in your `PATH`.

   ```shell
   curl -O https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage ~/.local/bin/appimagetool-x86_64.AppImage
   ```

6. Build and package.

    ```shell
    ./building/build_linux.sh ${arch}
    ```

   `SciHubEVA-${arch}-latest.AppImage` will be in `dist-Linux-${arch}`.
