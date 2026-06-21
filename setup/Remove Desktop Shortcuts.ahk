#Requires AutoHotkey v2.0
#SingleInstance Force

APP_NAME := "eMachination CAD Patent Prompt-Rig"
removed := 0
for _, desktopDir in DesktopCandidates() {
    if !DirExist(desktopDir)
        continue
    removed += RemoveIfPresent(desktopDir "\\Start eMachination CAD Patent Prompt-Rig.lnk")
    removed += RemoveIfPresent(desktopDir "\\Stop eMachination CAD Patent Prompt-Rig.lnk")
}
MsgBox("Removed " removed " Desktop shortcut(s).", APP_NAME, "Iconi")
ExitApp(0)

RemoveIfPresent(path) {
    if FileExist(path) {
        try {
            FileDelete(path)
            return 1
        }
    }
    return 0
}

DesktopCandidates() {
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
    return candidates
}
