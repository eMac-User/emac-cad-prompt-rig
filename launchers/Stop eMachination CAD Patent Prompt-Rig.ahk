#Requires AutoHotkey v2.0
#SingleInstance Force

appRoot := A_ScriptDir
if RegExMatch(appRoot, "i)\\launchers$")
    appRoot := RegExReplace(appRoot, "i)\\launchers$", "")
stopHelper := appRoot "\\tools\\stop_emachination_cad_patent_prompt_rig.ahk"
if !FileExist(stopHelper) {
    MsgBox("Stop helper not found:`r`n`r`n" stopHelper, "eMachination CAD Patent Prompt-Rig", "Iconx")
    ExitApp(1)
}
Run('"' A_AhkPath '" "' stopHelper '"', appRoot)
ExitApp(0)
