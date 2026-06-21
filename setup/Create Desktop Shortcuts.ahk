#Requires AutoHotkey v2.0
#SingleInstance Force

APP_NAME := "eMachination CAD Patent Prompt-Rig"
appRoot := A_ScriptDir
if RegExMatch(appRoot, "i)\\setup$")
    appRoot := RegExReplace(appRoot, "i)\\setup$", "")

startLauncher := appRoot "\\launchers\\Start eMachination CAD Patent Prompt-Rig.ahk"
stopLauncher := appRoot "\\launchers\\Stop eMachination CAD Patent Prompt-Rig.ahk"

if !FileExist(startLauncher) {
    MsgBox("Start launcher not found:`r`n`r`n" startLauncher, APP_NAME, "Iconx")
    ExitApp(1)
}
if !FileExist(stopLauncher) {
    MsgBox("Stop launcher not found:`r`n`r`n" stopLauncher, APP_NAME, "Iconx")
    ExitApp(1)
}
if (A_AhkPath = "" || !FileExist(A_AhkPath)) {
    MsgBox("AutoHotkey v2 executable path could not be resolved. Open this helper with AutoHotkey v2.", APP_NAME, "Iconx")
    ExitApp(1)
}

desktopDir := PickDesktopDir()
if !DirExist(desktopDir) {
    MsgBox("Desktop folder not found:`r`n`r`n" desktopDir, APP_NAME, "Iconx")
    ExitApp(1)
}

startLnk := desktopDir "\\Start eMachination CAD Patent Prompt-Rig.lnk"
stopLnk := desktopDir "\\Stop eMachination CAD Patent Prompt-Rig.lnk"

try {
    if FileExist(startLnk)
        FileDelete(startLnk)
    if FileExist(stopLnk)
        FileDelete(stopLnk)
    FileCreateShortcut(A_AhkPath, startLnk, appRoot, '"' startLauncher '"', "Start " APP_NAME)
    FileCreateShortcut(A_AhkPath, stopLnk, appRoot, '"' stopLauncher '"', "Stop " APP_NAME)
    MsgBox("Desktop shortcuts created:`r`n`r`n" startLnk "`r`n" stopLnk, APP_NAME, "Iconi")
} catch as err {
    MsgBox("Could not create Desktop shortcuts:`r`n`r`n" err.Message, APP_NAME, "Iconx")
    ExitApp(1)
}
ExitApp(0)

PickDesktopDir() {
    candidates := []
    candidates.Push(A_Desktop)
    userProfile := EnvGet("USERPROFILE")
    if (userProfile != "")
        candidates.Push(userProfile "\\Desktop")
    for _, envName in ["OneDrive", "OneDriveConsumer", "OneDriveCommercial"] {
        oneDriveRoot := EnvGet(envName)
        if (oneDriveRoot != "")
            candidates.Push(oneDriveRoot "\\Desktop")
    }
    for _, candidate in candidates {
        if DirExist(candidate)
            return candidate
    }
    return A_Desktop
}
