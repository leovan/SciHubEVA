!include "LogicLib.nsh"
!include "WinVer.nsh"
!include "nsDialogs.nsh"
!include "MUI2.nsh"

!define PRODUCT_NAME "Sci-Hub EVA"
!define PRODUCT_VERSION "1.0.0.0"
!define PRODUCT_SHORT_VERSION "1.0"
!define PRODUCT_DISPLAY_NAME "$(LNG_ProductName) v${PRODUCT_SHORT_VERSION}"
!define PRODUCT_PUBLISHER "Leo Van"
!define PRODUCT_WEB_SITE ""
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PRODUCT_STARTMENU_REGVAL "NSIS:StartMenuDir"

SetCompress auto
SetCompressor lzma

!define MULTIUSER_EXECUTIONLEVEL Admin
!define MULTIUSER_INSTALLMODE_COMMANDLINE
!include "MultiUser.nsh"

!define MUI_ABORTWARNING
!define MUI_ICON "images\SciHubEVA.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "images\SciHubEVA-nsis-header.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "images\SciHubEVA-nsis-header.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "images\SciHubEVA-nsis-wizard-install.bmp"
!define MUI_COMPONENTSPAGE_CHECKBITMAP "${NSISDIR}\Contrib\Graphics\Checks\modern.bmp"
!define MUI_UNICON "images\SciHubEVA.ico"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "images\SciHubEVA-nsis-wizard-uninstall.bmp"
!define MUI_LICENSEPAGE_CHECKBOX

!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome Page
!insertmacro MUI_PAGE_WELCOME

; License Page
!insertmacro MUI_PAGE_LICENSE "$(LNG_License)"

; Directory Page
!insertmacro MUI_PAGE_DIRECTORY

; Start menu Page
var ICONS_GROUP
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "${PRODUCT_NAME}"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${PRODUCT_STARTMENU_REGVAL}"
!insertmacro MUI_PAGE_STARTMENU Application $ICONS_GROUP

; Desktop Short Page
Page custom DesktopShortcutPageInitFunc DesktopShortcutPageLeaveFunc ""

; Instfiles Page
!insertmacro MUI_PAGE_INSTFILES

; Finish Page
!define MUI_FINISHPAGE_RUN "$INSTDIR\SciHubEVA.exe"
!define MUI_FINISHPAGE_RUN_TEXT "$(LNG_Run)  $(LNG_ProductName) v${PRODUCT_SHORT_VERSION}"
!insertmacro MUI_PAGE_FINISH

; Uninstaller Page
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "SimpChinese"

; Pages
Var CreateDesktopShortcutDialog
Var CreateDesktopShortcutTitle
Var CreateDesktopShortcutCheckbox
Var CreateDesktopShortcutCheckboxState

LangString LNG_CreateDesktopShortcutTitle ${LANG_ENGLISH} "Select Additional Tasks"
LangString LNG_CreateDesktopShortcutTitle ${LANG_SIMPCHINESE} "选择附加任务"

LangString LNG_CreateDesktopShortcutSubTitle ${LANG_ENGLISH} "Select additional tasks to be performed."
LangString LNG_CreateDesktopShortcutSubTitle ${LANG_SIMPCHINESE} "选择要执行的附加任务。"

LangString LNG_CreateDesktopShortcutLabel ${LANG_ENGLISH} "Select the additional tasks you would like Setup to perform while installing Sci-Hub EVA, then click Install to continue."
LangString LNG_CreateDesktopShortcutLabel ${LANG_SIMPCHINESE} "请选择安装 Sci-Hub EVA 时需要执行的附加任务，然后点击[安装(I)]。"

LangString LNG_CreateDesktopShortcutChechbox ${LANG_ENGLISH} "Create a desktop icon"
LangString LNG_CreateDesktopShortcutChechbox ${LANG_SIMPCHINESE} "创建桌面快捷方式(&D)"

Function DesktopShortcutPageInitFunc
  !insertmacro MUI_HEADER_TEXT "$(LNG_CreateDesktopShortcutTitle)" "$(LNG_CreateDesktopShortcutSubTitle)"
  nsDialogs::Create 1018
	Pop $CreateDesktopShortcutDialog
	${If} $CreateDesktopShortcutDialog == error
		Abort
	${EndIf}
  ${NSD_CreateLabel} 0 0 100% 25u "$(LNG_CreateDesktopShortcutLabel)"
	Pop $CreateDesktopShortcutTitle
	${NSD_CreateCheckbox} 0 30u 100% 30u "$(LNG_CreateDesktopShortcutChechbox)"
	Pop $CreateDesktopShortcutCheckbox
  ${NSD_Check} $CreateDesktopShortcutCheckbox
  nsDialogs::Show
FunctionEnd

Function DesktopShortcutPageLeaveFunc
  ${NSD_GetState} $CreateDesktopShortcutCheckbox $CreateDesktopShortcutCheckboxState
  ${If} $CreateDesktopShortcutCheckboxState == ${BST_CHECKED}
    CreateShortCut "$DESKTOP\$(LNG_ProductName).lnk" "$INSTDIR\SciHubEVA.exe"
	${EndIf}
FunctionEnd

LicenseLangString LNG_License ${LANG_ENGLISH} "LICENSE"
LicenseLangString LNG_License ${LANG_SIMPCHINESE} "LICENSE"
LangString LNG_ProductName ${LANG_ENGLISH} "Sci-Hub EVA"
LangString LNG_ProductName ${LANG_SIMPCHINESE} "Sci-Hub EVA"
LangString LNG_Setup ${LANG_ENGLISH} "Setup"
LangString LNG_Setup ${LANG_SIMPCHINESE} "安装"
LangString LNG_Uninstall ${LANG_ENGLISH} "Uninstall"
LangString LNG_Uninstall ${LANG_SIMPCHINESE} "卸载"
LangString LNG_Run ${LANG_ENGLISH} "Run"
LangString LNG_Run ${LANG_SIMPCHINESE} "运行"

Name "$(LNG_ProductName) v${PRODUCT_SHORT_VERSION}"
OutFile "dist\SciHubEVA-x64.exe"
InstallDir "$PROGRAMFILES64\${PRODUCT_NAME}"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show
BrandingText "$(LNG_ProductName) v${PRODUCT_SHORT_VERSION}"
SetOverwrite on
Caption "$(LNG_ProductName) v${PRODUCT_SHORT_VERSION} $(LNG_Setup)"
UninstallCaption "$(LNG_ProductName) v${PRODUCT_SHORT_VERSION} $(LNG_Uninstall)"

VIProductVersion "1.0.0.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "Sci-Hub EVA"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "ProductName" "Sci-Hub EVA"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductVersion" "1.0.0.0"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "ProductVersion" "1.0.0.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "Leo Van"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "CompanyName" "Leo Van"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "Copyright (C) 2018 ${PRODUCT_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "LegalCopyright" "版权所有 (C) 2018 ${PRODUCT_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalTrademarks" ""
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "LegalTrademarks" ""
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "Sci-Hub EVA Installer"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileDescription" "Sci-Hub EVA 安装程序"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "1.0.0.0"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileVersion" "1.0.0.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "Comments" ""
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "Comments" ""

Section "MainSection" SEC001
  SetOutPath "$INSTDIR"
  SetOverwrite on
  File /nonfatal /r "dist\SciHubEVA\*"
SectionEnd

Function .onInit
  !insertmacro MULTIUSER_INIT
  !define MUI_LANGDLL_ALWAYSSHOW
  !insertmacro MUI_LANGDLL_DISPLAY
  StrCpy $0 0
  IntOp $0 $0 | ${SF_SELECTED}
  SectionSetFlags ${SEC001} $0
FunctionEnd

Section -AdditionalIcons
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  CreateDirectory "$SMPROGRAMS\$(LNG_ProductName)"
  CreateShortCut "$SMPROGRAMS\$(LNG_ProductName)\$(LNG_Uninstall).lnk" "$INSTDIR\uninst.exe"
  CreateShortCut "$SMPROGRAMS\$(LNG_ProductName)\$(LNG_ProductName).lnk" "$INSTDIR\SciHubEVA.exe"
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\SciHubEVA.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "InstallPath" "$INSTDIR"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "InstallMode" "$MultiUser.InstallMode"
SectionEnd

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC001} ""
!insertmacro MUI_FUNCTION_DESCRIPTION_END

LangString LNG_UninstSuccess ${LANG_ENGLISH} "Sci-Hub EVA was successfully removed from your computer."
LangString LNG_UninstSuccess ${LANG_SIMPCHINESE} "Sci-Hub EVA 成功卸载。"

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(LNG_UninstSuccess)"
FunctionEnd

LangString LNG_UninstWarning ${LANG_ENGLISH} "Are you sure you want to completely remove Sci-Hub EVA and all of its components?"
LangString LNG_UninstWarning ${LANG_SIMPCHINESE} "你确定要删除 Sci-Hub EVA 及其所有组件吗？"

Function un.onInit
  !insertmacro MULTIUSER_UNINIT
  !insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "$(LNG_UninstWarning)" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  !insertmacro MUI_STARTMENU_GETFOLDER Application $ICONS_GROUP
  
  RMDir /r "$INSTDIR"

  Delete "$SMPROGRAMS\$(LNG_ProductName)\$(LNG_Uninstall).lnk"
  Delete "$SMPROGRAMS\$(LNG_ProductName)\$(LNG_ProductName).lnk"
  RMDir "$SMPROGRAMS\$(LNG_ProductName)"

  Delete "$DESKTOP\$(LNG_ProductName).lnk"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd

