; CI-friendly Inno Setup Script for PDReader
; Uses relative paths and works in GitHub Actions

#define MyAppName "PDReader"
#define MyAppVersion "0.1"
#define MyAppPublisher "Sanjid Sharaf"
#define MyAppExeName "PDReaderApp.exe"

#ifdef GITHUB_ACTIONS
  #define EXE_PATH "..\\dist\\" + MyAppExeName
  #define OUT_DIR "..\\dist"
#else
  #define EXE_PATH "dist\\" + MyAppExeName
  #define OUT_DIR "dist"
#endif

[Setup]
AppId={{974A3A4B-6B6A-4E09-87B8-079839951E2A}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\PD Reader
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes
OutputDir={#OUT_DIR}
OutputBaseFilename=pdreadersetup
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "{#EXE_PATH}"; DestDir: "{app}"; Flags: ignoreversion

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
