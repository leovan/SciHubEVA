#define MyAppName "Sci-Hub EVA"
#define MyAppVersion "6.3.1"
#define MyAppPublisher "Leo Van"
#define MyAppURL "https://github.com/leovan/SciHubEVA"
#define MyAppExeName "SciHubEVA.exe"
#define MyAppArch "x86_64"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright=Copyright (c) 2018-2025 Leo Van.
VersionInfoVersion={#MyAppVersion}
DefaultDirName={autopf64}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\..\LICENSE
OutputDir=..\..\dist-Windows-{#MyAppArch}
OutputBaseFilename=SciHubEVA-{#MyAppArch}-latest
SetupIconFile=SciHubEVA-inno-installer.ico
Compression=lzma2/ultra64
SolidCompression=yes
DisableWelcomePage=no
WizardImageFile=SciHubEVA-inno-installer-wizard.bmp
WizardSmallImageFile=SciHubEVA-inno-installer-wizard-small.bmp
ArchitecturesAllowed=x64
UninstallDisplayIcon={app}\{#MyAppExeName}
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "en"; MessagesFile: "compiler:\Default.isl"
Name: "pt"; MessagesFile: "compiler:\Languages\Portuguese.isl"
Name: "zh_Hans"; MessagesFile: "ChineseSimplified.isl"
Name: "zh_Hant"; MessagesFile: "ChineseTraditional.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\..\dist-Windows-{#MyAppArch}\SciHubEVA\SciHubEVA.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\dist-Windows-{#MyAppArch}\SciHubEVA\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram, {#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser
