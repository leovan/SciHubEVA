Write-Output "Install requirements"
pip install -r requirements.txt
pip install -r requirements-dev.txt

Write-Output "Generate i18n files"
python building/convert_i18n_zh.py
foreach ($file in (Get-ChildItem -Path i18n *.ts | %{$_.FullName}))
{
  pyside6-lrelease $file
}

Write-Output "Build with PyInstaller"
pyside6-rcc SciHubEVA.qrc -o scihub_eva/resources.py

if (Test-Path "build-Windows-x64")
{
  Remove-Item "build-Windows-x64" -Recurse
}
if (Test-Path "dist-Windows-x64")
{
  Remove-Item "dist-Windows-x64" -Recurse
}
if (Test-Path "SciHubEVA.spec")
{
  Remove-Item "SciHubEVA.spec"
}

pyinstaller app.py `
  --workpath "build-Windows-x64" `
  --distpath "dist-Windows-x64" `
  --hidden-import "socks" `
  --hidden-import "PIL" `
  --add-data "LICENSE;." `
  --add-data "preferences/qtquickcontrols2.conf;preferences" `
  --add-data "images/SciHubEVA-icon.png;images" `
  --add-data "i18n/*.qm;i18n" `
  --name "SciHubEVA" `
  --icon "building/Windows/SciHubEVA.ico" `
  --version-file "building/Windows/SciHubEVA.win.version" `
  --windowed `
  --clean `
  --noupx

python building/post_process.py dist-Windows-x64

Write-Output "Package with Inno Setup"

Invoke-WebRequest -Uri "https://github.com/jrsoftware/issrc/raw/main/Files/Languages/Unofficial/ChineseSimplified.isl" -OutFile "building\\Windows\\ChineseSimplified.isl"
Invoke-WebRequest -Uri "https://github.com/jrsoftware/issrc/raw/main/Files/Languages/Unofficial/ChineseTraditional.isl" -OutFile "building\\Windows\\ChineseTraditional.isl"

& "${Env:ProgramFiles(x86)}\\Inno Setup 6\\ISCC.exe" "building\\Windows\\SciHubEVA-x64.iss"
