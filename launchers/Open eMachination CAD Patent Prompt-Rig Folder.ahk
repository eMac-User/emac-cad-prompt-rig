#Requires AutoHotkey v2.0
#SingleInstance Force

appRoot := A_ScriptDir
if RegExMatch(appRoot, "i)\\launchers$")
    appRoot := RegExReplace(appRoot, "i)\\launchers$", "")
Run(appRoot)
ExitApp(0)
