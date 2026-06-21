#Requires AutoHotkey v2.0
#SingleInstance Force

APP_NAME := "eMachination CAD Patent Prompt-Rig"
appRoot := A_ScriptDir
if RegExMatch(appRoot, "i)\\setup$")
    appRoot := RegExReplace(appRoot, "i)\\setup$", "")

startLauncher := appRoot "\\launchers\\Start eMachination CAD Patent Prompt-Rig.ahk"
if !FileExist(startLauncher) {
    MsgBox("Start launcher not found:`r`n`r`n" startLauncher, APP_NAME, "Iconx")
    ExitApp(1)
}
if (A_AhkPath = "" || !FileExist(A_AhkPath)) {
    MsgBox("AutoHotkey v2 executable path could not be resolved. Open this helper with AutoHotkey v2.", APP_NAME, "Iconx")
    ExitApp(1)
}

startupLnk := A_Startup "\\Start eMachination CAD Patent Prompt-Rig.lnk"
answer := MsgBox("Create optional Windows Startup shortcut?`r`n`r`nThis will start eMachination CAD Patent Prompt-Rig when your Windows user account signs in.", APP_NAME, "YesNo Icon?")
if (answer != "Yes")
    ExitApp(0)

try {
    if FileExist(startupLnk)
        FileDelete(startupLnk)
    FileCreateShortcut(A_AhkPath, startupLnk, appRoot, '"' startLauncher '"', "Start " APP_NAME)
    MsgBox("Startup shortcut created:`r`n`r`n" startupLnk, APP_NAME, "Iconi")
} catch as err {
    MsgBox("Could not create Startup shortcut:`r`n`r`n" err.Message, APP_NAME, "Iconx")
    ExitApp(1)
}
ExitApp(0)
