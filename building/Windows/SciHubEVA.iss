#define MyAppName "Sci-Hub EVA"
#define MyAppVersion "2.1.0"
#define MyAppPublisher "Leo Van"
#define MyAppURL "https://leovan.me"
#define MyAppExeName "SciHubEVA.exe"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright=Copyright (c) 2018-2019 Leo Van.
AppReadmeFile=https://github.com/leovan/SciHubEVA
DefaultDirName={pf64}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\..\LICENSE
OutputDir=..\..\dist
OutputBaseFilename=SciHubEVA-x64
SetupIconFile=..\..\images\SciHubEVA-win-installer.ico
Compression=lzma2/ultra64
SolidCompression=yes
DisableWelcomePage=no
WizardImageFile=..\..\images\SciHubEVA-inno-installer-wizard.bmp
WizardSmallImageFile=..\..\images\SciHubEVA-inno-installer-wizard-small.bmp
ArchitecturesAllowed=x64
UninstallDisplayIcon={app}\{#MyAppExeName}
PrivilegesRequired=admin

[Languages]
Name: "en"; MessagesFile: "compiler:\Default.isl"
Name: "zh_Hans"; MessagesFile: "compiler:\Languages\ChineseSimplified.isl"
Name: "zh_Hant"; MessagesFile: "compiler:\Languages\ChineseTraditional.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\..\dist\SciHubEVA\SciHubEVA.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\dist\SciHubEVA\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram, {#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser
