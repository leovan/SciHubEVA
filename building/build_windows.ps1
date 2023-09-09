$arch=$args[0]
Write-Output "Building Windows $($arch) target ..."

Write-Output "Installing requirements ..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

Write-Output "Generating i18n files ..."
python building/convert_i18n_zh.py
foreach ($file in (Get-ChildItem -Path i18n *.ts | ForEach-Object{$_.FullName}))
{
  pyside6-lrelease $file
}

Write-Output "Building with PyInstaller ..."
pyside6-rcc SciHubEVA.qrc -o scihub_eva/resources.py

if (Test-Path "build-Windows-$($arch)")
{
  Remove-Item "build-Windows-$($arch)" -Recurse
}
if (Test-Path "dist-Windows-$($arch)")
{
  Remove-Item "dist-Windows-$($arch)" -Recurse
}
if (Test-Path "SciHubEVA.spec")
{
  Remove-Item "SciHubEVA.spec"
}

pyinstaller app.py `
  --workpath "build-Windows-$($arch)" `
  --distpath "dist-Windows-$($arch)" `
  --hidden-import "socks" `
  --add-data "LICENSE;." `
  --add-data "building/Windows/qtquickcontrols2.conf;confs" `
  --add-data "building/Windows/SciHubEVA-icon.png;images" `
  --add-data "confs/ddos-guard-fake-mark.json;confs" `
  --add-data "i18n/*.qm;i18n" `
  --name "SciHubEVA" `
  --icon "building/Windows/SciHubEVA.ico" `
  --version-file "building/Windows/SciHubEVA.win.version" `
  --windowed `
  --clean `
  --noupx `
  --target-arch $($arch)

Write-Output "Post processing ..."
python building/post_process.py dist-Windows-$($arch)

Write-Output "Packaging with Inno Setup ..."
Invoke-WebRequest -Uri "https://github.com/jrsoftware/issrc/raw/main/Files/Languages/Unofficial/ChineseSimplified.isl" -OutFile "building\\Windows\\ChineseSimplified.isl"
Invoke-WebRequest -Uri "https://github.com/jrsoftware/issrc/raw/main/Files/Languages/Unofficial/ChineseTraditional.isl" -OutFile "building\\Windows\\ChineseTraditional.isl"
& "${Env:ProgramFiles(x86)}\\Inno Setup 6\\ISCC.exe" "building\\Windows\\SciHubEVA-$($arch).iss"

Write-Output "Building Windows $($arch) target finished."
