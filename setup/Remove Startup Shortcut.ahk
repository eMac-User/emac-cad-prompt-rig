#Requires AutoHotkey v2.0
#SingleInstance Force

APP_NAME := "eMachination CAD Patent Prompt-Rig"
startupLnk := A_Startup "\\Start eMachination CAD Patent Prompt-Rig.lnk"
if FileExist(startupLnk) {
    try {
        FileDelete(startupLnk)
        MsgBox("Removed Startup shortcut:`r`n`r`n" startupLnk, APP_NAME, "Iconi")
    } catch as err {
        MsgBox("Could not remove Startup shortcut:`r`n`r`n" err.Message, APP_NAME, "Iconx")
        ExitApp(1)
    }
} else {
    MsgBox("No eMachination CAD Patent Prompt-Rig Startup shortcut was found.", APP_NAME, "Iconi")
}
ExitApp(0)
