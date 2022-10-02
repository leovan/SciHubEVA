# Building

## macOS

1. Create a python environment.
2. Install requirements.

   ```shell
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. Update the translations.

   ```shell
   # Generate translations source of QML files
   lupdate SciHubEVA.pro

   # Generate translations source of Python files
   pyside6-lupdate \
     scihub_eva/api/*.py \
     scihub_eva/ui/*.py \
     -ts i18n/SciHubEVA_zh_CN.ts
   ```

4. Install [create-dmg](https://github.com/create-dmg/create-dmg).

   ```shell
   brew install create-dmg
   ```

5. Build and package.

   ```shell
   ./building/build_macos_x64.sh
   ```

   `SciHubEVA-x64-latest.dmg` will be in `dist-macOS-x64`.

## Windows

1. See step 1 in [macOS](#macOS).
2. See step 2 in [macOS](#macOS).
3. See step 3 in [macOS](#macOS).
4. Install [Inno Setup](https://jrsoftware.org/isinfo.php) and make sure `ISCC.exe` is in your `PATH`.
5. Build and package.

   ```powershell
   ./building/build_windows_x64.ps1
   ```

   `SciHubEVA-x64-latest.exe` will be in `dist-Windows-x64`.
