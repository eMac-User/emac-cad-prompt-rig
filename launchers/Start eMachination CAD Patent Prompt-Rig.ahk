#Requires AutoHotkey v2.0
#SingleInstance Off

appRoot := A_ScriptDir
if RegExMatch(appRoot, "i)\\launchers$")
    appRoot := RegExReplace(appRoot, "i)\\launchers$", "")
runtime := appRoot "\\src\\eMachination_Coding_Prompt_Rig.ahk"
if !FileExist(runtime) {
    MsgBox("Runtime script not found:`r`n`r`n" runtime, "eMachination CAD Patent Prompt-Rig", "Iconx")
    ExitApp(1)
}
Run('"' A_AhkPath '" "' runtime '"', appRoot)
ExitApp(0)
