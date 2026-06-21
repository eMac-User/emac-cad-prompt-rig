#Requires AutoHotkey v2.0
#SingleInstance Force

DetectHiddenWindows true
SetTitleMatchMode 2
quiet := false
for arg in A_Args {
    if (StrLower(arg) = "/quiet")
        quiet := true
}

closed := 0
CloseMatchingScripts("eMachination_Coding_Prompt_Rig.ahk", &closed)
; Defensive compatibility for early development packages.
CloseMatchingScripts("VeydraNet_Hotkey_Board.ahk", &closed)

if (!quiet) {
    if (closed > 0)
        MsgBox("Close request sent to " closed " AutoHotkey window(s).", "eMachination CAD Patent Prompt-Rig")
    else
        MsgBox("No eMachination CAD Patent Prompt-Rig AutoHotkey window was found. It may already be stopped.", "eMachination CAD Patent Prompt-Rig")
}
ExitApp()

CloseMatchingScripts(scriptName, &closed) {
    try {
        ids := WinGetList(scriptName " ahk_class AutoHotkey")
        for hwnd in ids {
            try {
                WinClose("ahk_id " hwnd)
                closed += 1
            }
        }
    }
}
