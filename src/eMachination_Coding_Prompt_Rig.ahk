#Requires AutoHotkey v2.0
#SingleInstance Force
#UseHook

; eMachination CAD Patent Prompt-Rig - AutoHotkey v2 runtime
; Focused Windows runtime with Linux source/runtime support included.
; Runtime model: prompts/index.ini maps labels/paths; Markdown files contain prompt bodies.

APP_NAME := "eMachination CAD Patent Prompt-Rig"
APP_TITLE_LINE_1 := "eMachination CAD Patent"
APP_TITLE_LINE_2 := "Prompt-Rig"
APP_ROOT := A_ScriptDir
if RegExMatch(APP_ROOT, "i)\\src$")
    APP_ROOT := RegExReplace(APP_ROOT, "i)\\src$", "")

INDEX_PATH := APP_ROOT "\prompts\index.ini"
CONFIG_DIR := APP_ROOT "\config"
SETTINGS_PATH := CONFIG_DIR "\settings.ini"
BRAND_RUNTIME_DIR := APP_ROOT "\src\brand"
BRAND_BOARD_IMAGE_PATH := BRAND_RUNTIME_DIR "\emachination-cad-prompt-rig-banner-app.png"
BRAND_ICON_PATH := BRAND_RUNTIME_DIR "\emachination-cad-prompt-rig-icon-256.png"
BRAND_FORGE_ICON_PATH := BRAND_RUNTIME_DIR "\emachination-cad-prompt-rig-icon-128.png"
BRAND_FORGE_BANNER_IMAGE_PATH := BRAND_RUNTIME_DIR "\emachination-prompt-forge-banner-app.png"
BRAND_WINDOW_ICON_PATH := BRAND_RUNTIME_DIR "\emachination-window-icon.ico"

profiles := [
    Map("id", "rough_in_part_development", "name", "Rough-In Parts"),
    Map("id", "mechanical_drawing_cleanup", "name", "Mechanical Drawing Cleanup"),
    Map("id", "cad_application_assist", "name", "CAD Application Assist")
]

boards := [
    Map("id", "primary", "name", "Primary"),
    Map("id", "secondary", "name", "Secondary"),
    Map("id", "tertiary", "name", "Tertiary")
]

promptIndex := Map()
activeProfileIndex := 1
activeBoardIndex := 1
boardGui := 0
boardHwnd := 0
statusCtrl := 0
numpadModeCtrl := 0
rememberNumpadCtrl := 0
profileGui := 0
profileHwnd := 0
forgeGui := 0
forgeHwnd := 0
forgeStatusCtrl := 0
forgeTransformCtrl := 0
forgeExtraCtrl := 0
forgePromptACtrl := 0
forgePromptBLabel := 0
forgePromptBCtrl := 0
forgeAddBCtrl := 0
forgeKeepOpenCtrl := 0
forgePromptBVisible := false
pasteTargetHwnd := 0
originalNumLockState := GetKeyState("NumLock", "T")
boardOpenNumLockState := originalNumLockState
globalChatHotkeysEnabled := true
numpadModeEnabled := false
rememberNumpadMode := false

TryApplyTrayIcon()
InitRuntime()
OnExit(RestoreNumLockOnExit)
if HasLaunchArg("--open-board")
    SetTimer(() => OpenBoard(1), -200)
return

; -----------------------------
; Global board hotkeys
; -----------------------------

; Use ScrollLock scan code for better reliability on keyboards that report
; Ctrl+ScrollLock/Pause combinations strangely. User-facing docs still say ScrollLock.
SC046::
{
    OpenBoard(1)
}


+SC046::
{
    OpenBoard(3)
}

Pause::
{
    CycleBoard()
}

^Pause::
{
    CycleBoard()
}

CtrlBreak::
{
    CycleBoard()
}

^CtrlBreak::
{
    CycleBoard()
}

; ^SC046 / Ctrl+ScrollLock is owned by eMachination_Prompt_Rig_Router.ahk.
; Router default action: switch/open CAD Prompt-Rig.

^!SC046::
{
    ExitPromptRig()
}

; -----------------------------
; Critical global chat-control hotkeys
; Configurable via config/settings.ini: enable_global_chat_hotkeys=1 or 0
; -----------------------------

#HotIf globalChatHotkeysEnabled
Insert::SendChatUtility("clear")
PgUp::SendChatUtility("Ok, continue")
Home::SendChatUtility("Checkpoint this. What is locked, what is open, and what is the next best step?")
End::SendChatUtility("Finalize this. Produce the clean final version now.")
PgDn::SendChatUtility("Next step only. Give me the next concrete action and stop.")
#HotIf

; -----------------------------
; Board-local NumLock profile cycling
; -----------------------------

#HotIf IsBoardFocused()
NumLock::CycleProfile()
Esc::CloseBoard()
F5::ReloadPromptLibrary()
#HotIf

; -----------------------------
; Optional board-focused numpad mode
; -----------------------------

#HotIf IsBoardNumpadActive()
Numpad1::PastePromptSlot(1)
NumpadEnd::PastePromptSlot(1)
Numpad2::PastePromptSlot(2)
NumpadDown::PastePromptSlot(2)
Numpad3::PastePromptSlot(3)
NumpadPgDn::PastePromptSlot(3)
Numpad4::PastePromptSlot(4)
NumpadLeft::PastePromptSlot(4)
Numpad5::PastePromptSlot(5)
NumpadClear::PastePromptSlot(5)
Numpad6::PastePromptSlot(6)
NumpadRight::PastePromptSlot(6)
Numpad7::PastePromptSlot(7)
NumpadHome::PastePromptSlot(7)
Numpad8::PastePromptSlot(8)
NumpadUp::PastePromptSlot(8)
Numpad9::OpenPromptForge()
NumpadPgUp::OpenPromptForge()
Numpad0::CloseBoard()
NumpadIns::CloseBoard()
^!Numpad0::ExitPromptRig()
^!NumpadIns::ExitPromptRig()
#HotIf

; -----------------------------
; Startup and settings
; -----------------------------

HasLaunchArg(target) {
    for arg in A_Args {
        if (arg = target)
            return true
    }
    return false
}
TryApplyTrayIcon() {
    global BRAND_ICON_PATH
    try {
        if FileExist(BRAND_ICON_PATH)
            TraySetIcon(BRAND_ICON_PATH)
    } catch {
    }
}
InitRuntime() {
    global APP_NAME, CONFIG_DIR, SETTINGS_PATH, promptIndex, globalChatHotkeysEnabled, rememberNumpadMode, numpadModeEnabled

    if !DirExist(CONFIG_DIR)
        DirCreate(CONFIG_DIR)

    LoadSettings()

    errors := PreflightPromptLibrary()
    if (errors.Length > 0) {
        msg := "Startup preflight failed. Normal board operation is blocked." "`r`n`r`n"
        maxToShow := Min(errors.Length, 24)
        Loop maxToShow
            msg .= "- " errors[A_Index] "`r`n"
        if (errors.Length > maxToShow)
            msg .= "- ...and " (errors.Length - maxToShow) " more issue(s)." "`r`n"
        msg .= "`r`nFix prompts/index.ini and the prompt Markdown files, then start eMachination CAD Patent Prompt-Rig again."
        MsgBox(msg, APP_NAME " - Preflight Failed", "Iconx")
        ExitApp()
    }
}

LoadSettings() {
    global SETTINGS_PATH, globalChatHotkeysEnabled, rememberNumpadMode, numpadModeEnabled

    if !FileExist(SETTINGS_PATH) {
        WriteDefaultSettings()
        return
    }

    try {
        globalChatHotkeysEnabled := IniRead(SETTINGS_PATH, "settings", "enable_global_chat_hotkeys", "1") = "1"
        rememberNumpadMode := IniRead(SETTINGS_PATH, "settings", "remember_numpad_mode", "0") = "1"
        if rememberNumpadMode
            numpadModeEnabled := IniRead(SETTINGS_PATH, "settings", "enable_numpad_mode", "0") = "1"
        else
            numpadModeEnabled := false
    } catch as err {
        globalChatHotkeysEnabled := true
        rememberNumpadMode := false
        numpadModeEnabled := false
    }
}

WriteDefaultSettings() {
    global SETTINGS_PATH
    try {
        IniWrite("1", SETTINGS_PATH, "settings", "enable_global_chat_hotkeys")
        IniWrite("0", SETTINGS_PATH, "settings", "enable_numpad_mode")
        IniWrite("0", SETTINGS_PATH, "settings", "remember_numpad_mode")
    }
}

SaveSetting(key, value) {
    global SETTINGS_PATH
    try IniWrite(value, SETTINGS_PATH, "settings", key)
}

PreflightPromptLibrary() {
    global INDEX_PATH, APP_ROOT, profiles, boards, promptIndex
    errors := []
    promptIndex := Map()

    if !FileExist(INDEX_PATH) {
        errors.Push("Missing required prompt index: " INDEX_PATH)
        return errors
    }

    sectionCounts := Map()
    try {
        indexText := FileRead(INDEX_PATH, "UTF-8")
    } catch as err {
        errors.Push("Unreadable prompt index: " INDEX_PATH)
        return errors
    }

    Loop Parse indexText, "`n", "`r" {
        line := Trim(A_LoopField)
        if RegExMatch(line, "^\[([^\]]+)\]$", &m) {
            sectionName := m[1]
            if sectionCounts.Has(sectionName)
                sectionCounts[sectionName] += 1
            else
                sectionCounts[sectionName] := 1
        }
    }

    for sectionName, count in sectionCounts {
        if (count > 1)
            errors.Push("Duplicate index section: [" sectionName "] appears " count " times")
    }

    seenPaths := Map()
    expectedCount := 0
    for _, profile in profiles {
        profileId := profile["id"]
        for _, board in boards {
            boardId := board["id"]
            Loop 8 {
                slot := A_Index
                section := profileId "." boardId "." Format("{:02}", slot)
                expectedCount += 1

                sentinel := "__VEYDRANET_MISSING__"
                label := ""
                relPath := ""
                try label := IniRead(INDEX_PATH, section, "label", sentinel)
                catch as err
                    label := sentinel
                try relPath := IniRead(INDEX_PATH, section, "path", sentinel)
                catch as err
                    relPath := sentinel

                if (label = sentinel) {
                    errors.Push("Missing index label for [" section "]")
                    continue
                }
                if (relPath = sentinel) {
                    errors.Push("Missing index path for [" section "]")
                    continue
                }

                label := Trim(label)
                relPath := Trim(relPath)
                if (label = "")
                    errors.Push("Empty label for [" section "]")
                if (relPath = "") {
                    errors.Push("Empty path for [" section "]")
                    continue
                }

                pathError := ValidateSafeRelativePromptPath(relPath)
                if (pathError != "") {
                    errors.Push("Unsafe path for [" section "]: " relPath " (" pathError ")")
                    continue
                }

                if seenPaths.Has(relPath)
                    errors.Push("Duplicate prompt path: " relPath " used by [" seenPaths[relPath] "] and [" section "]")
                else
                    seenPaths[relPath] := section

                fullPath := APP_ROOT "\" StrReplace(relPath, "/", "\")
                if !FileExist(fullPath) {
                    errors.Push("Missing prompt file for [" section "]: " relPath)
                    continue
                }

                try {
                    body := FileRead(fullPath, "UTF-8")
                } catch as err {
                    errors.Push("Unreadable prompt file for [" section "]: " relPath)
                    continue
                }

                if (Trim(body) = "") {
                    errors.Push("Empty prompt file for [" section "]: " relPath)
                    continue
                }

                promptIndex[section] := Map("label", label, "relPath", relPath, "fullPath", fullPath)
            }
        }
    }

    if (promptIndex.Count != expectedCount)
        errors.Push("Prompt index loaded " promptIndex.Count " valid entries, expected " expectedCount)

    return errors
}

ValidateSafeRelativePromptPath(relPath) {
    if (relPath = "")
        return "blank path"
    if InStr(relPath, "\")
        return "backslashes are not allowed in index paths"
    if InStr(relPath, ":")
        return "drive or protocol separator is not allowed"
    if (SubStr(relPath, 1, 1) = "/")
        return "absolute paths are not allowed"
    if InStr(relPath, "..")
        return "parent traversal is not allowed"
    if InStr(relPath, "//")
        return "double slash is not allowed"
    if (SubStr(relPath, 1, 8) != "prompts/")
        return "path must start with prompts/"
    if !RegExMatch(relPath, "i)\.md$")
        return "path must end with .md"
    if !RegExMatch(relPath, "^[A-Za-z0-9_/\.\-]+$")
        return "only letters, numbers, underscore, dash, slash, and dot are allowed"
    return ""
}

; -----------------------------
; Board GUI
; -----------------------------

OpenBoard(boardIndex) {
    global activeBoardIndex, boardOpenNumLockState
    RememberPasteTarget()
    activeBoardIndex := boardIndex
    boardOpenNumLockState := GetKeyState("NumLock", "T")
    BuildBoardGui()
}

CycleBoard(*) {
    global activeBoardIndex, boardOpenNumLockState, boards
    RememberPasteTarget()
    activeBoardIndex := (activeBoardIndex >= boards.Length) ? 1 : activeBoardIndex + 1
    boardOpenNumLockState := GetKeyState("NumLock", "T")
    BuildBoardGui()
}

ReloadPromptLibrary(*) {
    errors := PreflightPromptLibrary()
    if (errors.Length > 0) {
        msg := "Prompt reload failed." "`r`n`r`n"
        maxToShow := Min(errors.Length, 12)
        Loop maxToShow
            msg .= "- " errors[A_Index] "`r`n"
        MsgBox(msg, "eMachination CAD Patent Prompt-Rig - Reload Failed", "Iconx")
        SetBoardStatus("Reload failed")
        return
    }
    BuildBoardGui()
    SetBoardStatus("Prompts reloaded")
}

TryApplyWindowIcon(guiObj) {
    global BRAND_WINDOW_ICON_PATH, BRAND_ICON_PATH
    iconPath := FileExist(BRAND_WINDOW_ICON_PATH) ? BRAND_WINDOW_ICON_PATH : BRAND_ICON_PATH
    try {
        if !FileExist(iconPath)
            return
        hIconSmall := LoadPicture(iconPath, "Icon1 w16 h16", &imageTypeSmall)
        hIconBig := LoadPicture(iconPath, "Icon1 w32 h32", &imageTypeBig)
        if hIconSmall
            SendMessage(0x80, 0, hIconSmall,, "ahk_id " guiObj.Hwnd)
        if hIconBig
            SendMessage(0x80, 1, hIconBig,, "ahk_id " guiObj.Hwnd)
    } catch {
    }
}

BuildBoardGui() {
    global boardGui, boardHwnd, statusCtrl, numpadModeCtrl, rememberNumpadCtrl, BRAND_BOARD_IMAGE_PATH, BRAND_ICON_PATH
    global APP_NAME, APP_TITLE_LINE_1, APP_TITLE_LINE_2, activeProfileIndex, activeBoardIndex, profiles, boards, numpadModeEnabled, rememberNumpadMode, BRAND_BOARD_IMAGE_PATH, BRAND_ICON_PATH
    DestroyBoardGuiOnly()

    profileName := profiles[activeProfileIndex]["name"]
    boardName := boards[activeBoardIndex]["name"]

    boardGui := Gui("+AlwaysOnTop", APP_NAME)
    boardGui.SetFont("s9", "Segoe UI")
    boardGui.MarginX := 12
    boardGui.MarginY := 10
    boardGui.OnEvent("Close", BoardCloseEvent)
    TryApplyWindowIcon(boardGui)

        if FileExist(BRAND_BOARD_IMAGE_PATH) {
        boardGui.Add("Picture", "xm w360 h86", BRAND_BOARD_IMAGE_PATH)
    } else if FileExist(BRAND_ICON_PATH) {
        boardGui.Add("Picture", "x144 w72 h72", BRAND_ICON_PATH)
    }

    boardGui.SetFont("s9 Bold", "Segoe UI")
boardGui.SetFont("s8 Bold", "Segoe UI")
    boardGui.Add("Text", "xm w360 Center", profileName " - " boardName)
    boardGui.SetFont("s8", "Segoe UI")
    boardGui.Add("Text", "xm w360 Center", "Pause/Break cycles boards")

    boardGui.Add("Text", "xm w360 Center", "Num-Lock cycles profiles")
    statusCtrl := boardGui.Add("Text", "xm w360 Center", "Numpad: " (numpadModeEnabled ? "On" : "Off"))

    switchBtn := boardGui.Add("Button", "xm y+8 w170 h30", "Switch Profile")
    switchBtn.OnEvent("Click", OpenProfileChooser)
    openPromptsBtn := boardGui.Add("Button", "x+8 yp w170 h30", "Open Prompts")
    openPromptsBtn.OnEvent("Click", OpenActivePromptFolder)

    numpadModeCtrl := boardGui.Add("Checkbox", "xm y+7 w170", "Enable Numpad Mode")
    numpadModeCtrl.Value := numpadModeEnabled ? 1 : 0
    numpadModeCtrl.OnEvent("Click", NumpadModeChanged)
    rememberNumpadCtrl := boardGui.Add("Checkbox", "x+8 yp w170", "Remember Numpad Mode")
    rememberNumpadCtrl.Value := rememberNumpadMode ? 1 : 0
    rememberNumpadCtrl.OnEvent("Click", RememberNumpadChanged)

    boardGui.Add("Text", "xm y+8 w348 0x10")

    Loop 8 {
        slot := A_Index
        label := GetPromptLabel(slot)
        rowStart := Mod(slot - 1, 2) = 0
        opts := rowStart ? "xm y+8 w170 h32" : "x+8 yp w170 h32"
        btn := boardGui.Add("Button", opts, slot " " label)
        btn.OnEvent("Click", CopyPromptSlot.Bind(slot))
    }

    terminalBtn := boardGui.Add("Button", "xm y+10 w348 h30", "Copy Terminal Buffer")
    terminalBtn.OnEvent("Click", CopyTerminalBuffer)

    closeBtn := boardGui.Add("Button", "xm y+10 w170 h30", "Close")
    closeBtn.OnEvent("Click", BoardCloseButtonEvent)
    forgeBtn := boardGui.Add("Button", "x+8 yp w170 h30", "Prompt Forge")
    forgeBtn.OnEvent("Click", PromptForgeButtonEvent)

    boardGui.Show("AutoSize")
    boardHwnd := boardGui.Hwnd
}

DestroyBoardGuiOnly() {
    global boardGui, boardHwnd, statusCtrl, numpadModeCtrl, rememberNumpadCtrl
    if IsObject(boardGui) {
        try boardGui.Destroy()
    }
    boardGui := 0
    boardHwnd := 0
    statusCtrl := 0
    numpadModeCtrl := 0
    rememberNumpadCtrl := 0
}

BoardCloseEvent(*) {
    CloseBoard()
}

BoardCloseButtonEvent(*) {
    CloseBoard()
}

PromptForgeButtonEvent(*) {
    OpenPromptForge()
}

CloseBoard(*) {
    global activeProfileIndex, activeBoardIndex, numpadModeEnabled, rememberNumpadMode
    DestroyBoardGuiOnly()
    CloseProfileChooserOnly()
    activeProfileIndex := 1
    activeBoardIndex := 1
    if !rememberNumpadMode
        numpadModeEnabled := false
}

SetBoardStatus(text) {
    global statusCtrl
    if IsObject(statusCtrl)
        statusCtrl.Text := text
}

GetPromptSection(slot) {
    global activeProfileIndex, activeBoardIndex, profiles, boards
    return profiles[activeProfileIndex]["id"] "." boards[activeBoardIndex]["id"] "." Format("{:02}", slot)
}

GetPromptEntry(slot) {
    global promptIndex
    section := GetPromptSection(slot)
    if !promptIndex.Has(section)
        throw Error("Missing prompt index entry: [" section "]")
    return promptIndex[section]
}

GetPromptLabel(slot) {
    try {
        entry := GetPromptEntry(slot)
        return entry["label"]
    } catch as err {
        return "ERROR"
    }
}

ReadPromptForSlot(slot, &label, &body) {
    entry := GetPromptEntry(slot)
    label := entry["label"]
    try body := FileRead(entry["fullPath"], "UTF-8")
    catch as err
        throw Error("Unable to read prompt file: " entry["relPath"])
    if (Trim(body) = "")
        throw Error("Prompt file is empty: " entry["relPath"])
}

CopyPromptSlot(slot, *) {
    global APP_NAME
    try {
        ReadPromptForSlot(slot, &label, &body)
        A_Clipboard := body
        SetBoardStatus("Copied: " slot " " label)
    } catch as err {
        SetBoardStatus("ERROR: " err.Message)
        MsgBox(err.Message, APP_NAME " - Prompt Error", "Iconx")
    }
}

PastePromptSlot(slot, *) {
    global APP_NAME, pasteTargetHwnd

    try {
        activeHwnd := WinGetID("A")
        if (activeHwnd && !IsPromptRigWindow(activeHwnd))
            pasteTargetHwnd := activeHwnd
    }

    try {
        ReadPromptForSlot(slot, &label, &body)
        A_Clipboard := body
    } catch as err {
        SetBoardStatus("ERROR: " err.Message)
        MsgBox(err.Message, APP_NAME " - Prompt Error", "Iconx")
        return
    }

    if (!pasteTargetHwnd || !WinExist("ahk_id " pasteTargetHwnd) || IsPromptRigWindow(pasteTargetHwnd)) {
        SetBoardStatus("Paste target unavailable; copied: " slot " " label)
        return
    }

    try {
        WinActivate("ahk_id " pasteTargetHwnd)
        if !WinWaitActive("ahk_id " pasteTargetHwnd, "", 0.7) {
            SetBoardStatus("Could not activate paste target; copied: " slot " " label)
            return
        }
        Sleep(80)
        Send("^v")
        SetBoardStatus("Pasted: " slot " " label)
    } catch as err {
        SetBoardStatus("Paste failed; copied: " slot " " label)
    }
}

OpenActivePromptFolder(*) {
    global APP_NAME
    try {
        entry := GetPromptEntry(1)
        dirPath := RegExReplace(entry["fullPath"], "\\[^\\]+$", "")
        Run(dirPath)
        SetBoardStatus("Opened prompt folder")
    } catch as err {
        SetBoardStatus("ERROR: could not open prompt folder")
        MsgBox(err.Message, APP_NAME " - Open Prompts Error", "Iconx")
    }
}

NumpadModeChanged(ctrl, *) {
    global numpadModeEnabled, rememberNumpadMode
    numpadModeEnabled := ctrl.Value = 1
    SetBoardStatus("Numpad: " (numpadModeEnabled ? "On" : "Off"))
    if rememberNumpadMode
        SaveSetting("enable_numpad_mode", numpadModeEnabled ? "1" : "0")
}

RememberNumpadChanged(ctrl, *) {
    global rememberNumpadMode, numpadModeEnabled
    rememberNumpadMode := ctrl.Value = 1
    SaveSetting("remember_numpad_mode", rememberNumpadMode ? "1" : "0")
    if rememberNumpadMode
        SaveSetting("enable_numpad_mode", numpadModeEnabled ? "1" : "0")
    else
        SaveSetting("enable_numpad_mode", "0")
}


; -----------------------------
; Terminal buffer utility
; -----------------------------

CopyTerminalBuffer(*) {
    terminalHwnd := FindTerminalWindow()

    if !terminalHwnd {
        SetBoardStatus("ERROR: no Windows Terminal / console window found")
        MsgBox("No Windows Terminal / console window found. Open your WSL, PowerShell, or Windows Terminal session first, then try again.", "eMachination CAD Patent Prompt-Rig - Terminal Buffer", "Iconx")
        return
    }

    try {
        WinActivate("ahk_id " terminalHwnd)
        WinWaitActive("ahk_id " terminalHwnd, "", 2)

        ; Windows Terminal default actions:
        ; Ctrl+Shift+A = select all terminal buffer
        ; Ctrl+Shift+C = copy selected text
        Sleep(150)
        Send("^+a")
        Sleep(200)
        Send("^+c")
        Sleep(200)
        SetBoardStatus("Copied terminal buffer to clipboard")
    } catch as err {
        SetBoardStatus("ERROR: terminal buffer copy failed")
        MsgBox("Unable to copy terminal buffer: " err.Message, "eMachination CAD Patent Prompt-Rig - Terminal Buffer", "Iconx")
    }
}

FindTerminalWindow() {
    ; Windows Terminal, including WSL and PowerShell tabs.
    hwnd := WinExist("ahk_exe WindowsTerminal.exe")
    if hwnd
        return hwnd

    ; Classic console fallback.
    hwnd := WinExist("ahk_class ConsoleWindowClass")
    if hwnd
        return hwnd

    ; Older PowerShell host fallback.
    hwnd := WinExist("ahk_exe powershell.exe")
    if hwnd
        return hwnd

    ; PowerShell 7 host fallback.
    hwnd := WinExist("ahk_exe pwsh.exe")
    if hwnd
        return hwnd

    return 0
}

; -----------------------------
; Profile switching
; -----------------------------

OpenProfileChooser(*) {
    global APP_NAME, profileGui, profileHwnd, profiles
    CloseProfileChooserOnly()
    profileGui := Gui("+AlwaysOnTop", APP_NAME " - Switch Profile")
    profileGui.SetFont("s9", "Segoe UI")
    profileGui.MarginX := 12
    profileGui.MarginY := 10
    profileGui.OnEvent("Close", ProfileChooserCloseEvent)
    profileGui.Add("Text", "xm w280 Center", "Switch Profile")
    for index, profile in profiles {
        btn := profileGui.Add("Button", "xm y+6 w280 h30", profile["name"])
        btn.OnEvent("Click", ChooseProfile.Bind(index))
    }
    closeBtn := profileGui.Add("Button", "xm y+10 w280 h28", "Close")
    closeBtn.OnEvent("Click", ProfileChooserCloseEvent)
    profileGui.Show("AutoSize")
    profileHwnd := profileGui.Hwnd
}

ChooseProfile(profileIndex, *) {
    global activeProfileIndex
    activeProfileIndex := profileIndex
    CloseProfileChooserOnly()
    BuildBoardGui()
}

CycleProfile(*) {
    global activeProfileIndex, profiles, boardOpenNumLockState
    activeProfileIndex := (activeProfileIndex >= profiles.Length) ? 1 : activeProfileIndex + 1
    try SetNumLockState(boardOpenNumLockState ? "On" : "Off")
    BuildBoardGui()
}

CloseProfileChooserOnly(*) {
    global profileGui, profileHwnd
    if IsObject(profileGui) {
        try profileGui.Destroy()
    }
    profileGui := 0
    profileHwnd := 0
}

ProfileChooserCloseEvent(*) {
    CloseProfileChooserOnly()
}

; -----------------------------
; Prompt Forge
; -----------------------------

OpenPromptForge(*) {
    RememberPasteTarget()
    BuildPromptForgeGui(false)
}

BuildPromptForgeGui(showPromptBLayout := false, selectedTransformation := "", extraText := "", promptAText := "", promptBText := "", keepOpenValue := 0) {
    global APP_NAME, forgeGui, forgeHwnd, forgeStatusCtrl, forgeTransformCtrl, forgeExtraCtrl, forgePromptACtrl, BRAND_FORGE_ICON_PATH, BRAND_FORGE_BANNER_IMAGE_PATH
    global forgePromptBLabel, forgePromptBCtrl, forgeAddBCtrl, forgeKeepOpenCtrl, forgePromptBVisible

    ClosePromptForgeOnly()
    forgePromptBVisible := showPromptBLayout

    forgeGui := Gui("+AlwaysOnTop", APP_NAME " - Prompt Forge")
    forgeGui.SetFont("s9", "Segoe UI")
    forgeGui.MarginX := 12
    forgeGui.MarginY := 10
    forgeGui.OnEvent("Close", PromptForgeCloseEvent)
    TryApplyWindowIcon(forgeGui)
    if FileExist(BRAND_FORGE_BANNER_IMAGE_PATH) {
        forgeGui.Add("Picture", "xm w470 h118", BRAND_FORGE_BANNER_IMAGE_PATH)
    }
forgeGui.SetFont("s9 Bold", "Segoe UI")
forgeGui.SetFont("s8", "Segoe UI")
    coachBtn := forgeGui.Add("Button", "xm y+8 w470 h30", "Copy Prompt Coach")
    coachBtn.OnEvent("Click", CopyPromptCoach)

    forgeGui.Add("Text", "xm y+10 w105", "Source Mode:")
    sourceDDL := forgeGui.Add("DropDownList", "x+8 yp-3 w250", ["Manual Paste"])
    sourceDDL.Value := 1

    forgeGui.Add("Text", "xm y+8 w105", "Transformation:")
    forgeTransformCtrl := forgeGui.Add("DropDownList", "x+8 yp-3 w250", GetForgeTransformations())
    SetDropDownByText(forgeTransformCtrl, selectedTransformation, 1)
    forgeTransformCtrl.OnEvent("Change", ForgeTransformChanged)

    forgeGui.Add("Text", "xm y+8 w105", "Output:")
    outputDDL := forgeGui.Add("DropDownList", "x+8 yp-3 w250", ["Copy to clipboard"])
    outputDDL.Value := 1

    forgeGui.Add("Text", "xm y+12 w470", "Extra Instructions (optional)")
    forgeExtraCtrl := forgeGui.Add("Edit", "xm y+3 w470 r3", extraText)

    forgeGui.Add("Text", "xm y+10 w470", "Prompt A / Main Source")
    forgePromptACtrl := forgeGui.Add("Edit", "xm y+3 w470 r7", promptAText)

    if showPromptBLayout {
        forgePromptBLabel := forgeGui.Add("Text", "xm y+10 w470", "Prompt B / Optional Second Source")
        forgePromptBCtrl := forgeGui.Add("Edit", "xm y+3 w470 r6", promptBText)
        forgeAddBCtrl := 0
    } else {
        forgeAddBCtrl := forgeGui.Add("Button", "xm y+8 w170 h28", "+ Add Prompt B")
        forgeAddBCtrl.OnEvent("Click", ShowPromptBEvent)
        forgePromptBLabel := 0
        forgePromptBCtrl := 0
    }

    buildBtn := forgeGui.Add("Button", "xm y+10 w225 h30", "Build and Copy")
    buildBtn.OnEvent("Click", BuildPromptForgeOutput)
    closeBtn := forgeGui.Add("Button", "x+20 yp w225 h30", "Close")
    closeBtn.OnEvent("Click", PromptForgeCloseEvent)
    forgeKeepOpenCtrl := forgeGui.Add("Checkbox", "xm y+8 w300", "Keep Prompt Forge open after build")
    forgeKeepOpenCtrl.Value := keepOpenValue ? 1 : 0
    forgeStatusCtrl := forgeGui.Add("Text", "xm y+8 w470", "Ready")

    forgeGui.Show("AutoSize")
    forgeHwnd := forgeGui.Hwnd
}

SetDropDownByText(ctrl, wantedText, fallbackIndex := 1) {
    if !IsObject(ctrl)
        return
    if (Trim(wantedText) = "") {
        ctrl.Value := fallbackIndex
        return
    }
    values := GetForgeTransformations()
    for index, value in values {
        if (value = wantedText) {
            ctrl.Value := index
            return
        }
    }
    ctrl.Value := fallbackIndex
}

GetForgeState(&selectedTransformation, &extraText, &promptAText, &promptBText, &keepOpenValue) {
    global forgeTransformCtrl, forgeExtraCtrl, forgePromptACtrl, forgePromptBCtrl, forgeKeepOpenCtrl
    selectedTransformation := IsObject(forgeTransformCtrl) ? forgeTransformCtrl.Text : "Merge / Combine"
    extraText := IsObject(forgeExtraCtrl) ? forgeExtraCtrl.Text : ""
    promptAText := IsObject(forgePromptACtrl) ? forgePromptACtrl.Text : ""
    promptBText := IsObject(forgePromptBCtrl) ? forgePromptBCtrl.Text : ""
    keepOpenValue := (IsObject(forgeKeepOpenCtrl) && forgeKeepOpenCtrl.Value = 1) ? 1 : 0
}

GetForgeTransformations() {
    return [
        "Merge / Combine",
        "Repair",
        "Compress",
        "Expand",
        "Specialize",
        "Convert to Implementation Prompt",
        "Convert to Design-Doc Prompt",
        "Convert to Test/Debug Prompt",
        "Convert to Release Checklist Prompt",
        "Convert to Current-Session Instruction",
        "Convert to New-Session Prompt"
    ]
}

ForgeTransformChanged(*) {
    global forgeTransformCtrl, forgePromptBVisible
    if !IsObject(forgeTransformCtrl)
        return
    if (forgeTransformCtrl.Text = "Merge / Combine" && !forgePromptBVisible)
        ShowPromptBEvent()
}

ShowPromptBEvent(*) {
    GetForgeState(&selectedTransformation, &extraText, &promptAText, &promptBText, &keepOpenValue)
    BuildPromptForgeGui(true, selectedTransformation, extraText, promptAText, promptBText, keepOpenValue)
}

BuildPromptForgeOutput(*) {
    global forgeTransformCtrl, forgeExtraCtrl, forgePromptACtrl, forgePromptBCtrl, forgePromptBVisible, forgeKeepOpenCtrl, forgeStatusCtrl
    transformation := IsObject(forgeTransformCtrl) ? forgeTransformCtrl.Text : "Merge / Combine"
    extra := IsObject(forgeExtraCtrl) ? Trim(forgeExtraCtrl.Text) : ""
    promptA := IsObject(forgePromptACtrl) ? Trim(forgePromptACtrl.Text) : ""
    promptB := (forgePromptBVisible && IsObject(forgePromptBCtrl)) ? Trim(forgePromptBCtrl.Text) : ""

    if (promptA = "") {
        if IsObject(forgeStatusCtrl)
            forgeStatusCtrl.Text := "Prompt A is required for Build and Copy."
        return
    }

    output := "Task:`r`nCreate a finished reusable prompt from the source material below.`r`n`r`n"
    output .= "Selected transformation:`r`n" transformation "`r`n`r`n"
    output .= "Extra instructions:`r`n" extra "`r`n`r`n"
    output .= "Prompt A / Main Source:`r`n---`r`n" promptA "`r`n---`r`n`r`n"
    if (promptB != "")
        output .= "Prompt B / Optional Second Source:`r`n---`r`n" promptB "`r`n---`r`n`r`n"
    output .= "Output requirements:`r`n"
    output .= "- Produce one complete prompt, not commentary about the prompt.`r`n"
    output .= "- Preserve useful constraints from the source material.`r`n"
    output .= "- Remove duplication and conflicting wording.`r`n"
    output .= "- Resolve conflicts explicitly when Prompt A and Prompt B disagree.`r`n"
    output .= "- Keep the final prompt ready to paste into an AI session.`r`n"
    output .= "- Do not include placeholder text."

    A_Clipboard := output
    if IsObject(forgeStatusCtrl)
        forgeStatusCtrl.Text := "Built and copied to clipboard."
    if (!IsObject(forgeKeepOpenCtrl) || forgeKeepOpenCtrl.Value != 1)
        ClosePromptForgeOnly()
}

CopyPromptCoach(*) {
    global forgeStatusCtrl
    A_Clipboard := GetPromptCoachText()
    if IsObject(forgeStatusCtrl)
        forgeStatusCtrl.Text := "Prompt Coach copied to clipboard."
}

GetPromptCoachText() {
    return JoinLines([
        "You are helping me create a strong reusable AI prompt.",
        "",
        "I am still learning how to write prompts, so do not assume I know the best structure yet. Interview me briefly, one question at a time, until you understand what I am trying to accomplish.",
        "",
        "For each question:",
        "1. Ask the question.",
        "2. Explain why it matters.",
        "3. Give a recommended answer if there is an obvious best practice.",
        "4. Explain what changes based on my answer.",
        "",
        "Help me decide whether this should be:",
        "- a current-session instruction,",
        "- a new-session prompt,",
        "- a reusable workflow prompt,",
        "- a troubleshooting prompt,",
        "- a design prompt,",
        "- an implementation prompt,",
        "- a research prompt,",
        "- or a prompt for another specific task.",
        "",
        "Before producing the final prompt, check for:",
        "- missing context,",
        "- unclear task boundaries,",
        "- output format requirements,",
        "- tone/style requirements,",
        "- tools or files the AI should or should not use,",
        "- constraints,",
        "- failure risks,",
        "- whether the prompt should assume existing chat context or be self-contained.",
        "",
        "When ready, produce:",
        "1. The finished prompt.",
        "2. A short explanation of how to use it.",
        "3. A warning about any assumptions or weak points.",
        "",
        "Important:",
        "If the current chat has a lot of unrelated context, tell me to start a new chat and paste the final prompt there.",
        "Do not overcomplicate the result. Make the final prompt clear, practical, and ready to paste."
    ])
}

ClosePromptForgeOnly(*) {
    global forgeGui, forgeHwnd, forgeStatusCtrl, forgeTransformCtrl, forgeExtraCtrl, forgePromptACtrl
    global forgePromptBLabel, forgePromptBCtrl, forgeAddBCtrl, forgeKeepOpenCtrl, forgePromptBVisible
    if IsObject(forgeGui) {
        try forgeGui.Destroy()
    }
    forgeGui := 0
    forgeHwnd := 0
    forgeStatusCtrl := 0
    forgeTransformCtrl := 0
    forgeExtraCtrl := 0
    forgePromptACtrl := 0
    forgePromptBLabel := 0
    forgePromptBCtrl := 0
    forgeAddBCtrl := 0
    forgeKeepOpenCtrl := 0
    forgePromptBVisible := false
}

PromptForgeCloseEvent(*) {
    ClosePromptForgeOnly()
}

; -----------------------------
; Focus gates and utilities
; -----------------------------

IsBoardFocused() {
    global boardHwnd
    return (boardHwnd && WinActive("ahk_id " boardHwnd))
}

IsBoardNumpadActive() {
    global numpadModeEnabled
    return numpadModeEnabled
}

IsPromptRigWindow(hwnd) {
    global boardHwnd, profileHwnd, forgeHwnd
    return (hwnd && ((boardHwnd && hwnd = boardHwnd) || (profileHwnd && hwnd = profileHwnd) || (forgeHwnd && hwnd = forgeHwnd)))
}

RememberPasteTarget() {
    global pasteTargetHwnd
    try {
        activeHwnd := WinGetID("A")
        if (activeHwnd && !IsPromptRigWindow(activeHwnd))
            pasteTargetHwnd := activeHwnd
    }
}

SendChatUtility(text) {
    SendText text
    Send("{Enter}")
}

JoinLines(lines) {
    out := ""
    for index, line in lines
        out .= (index = 1 ? "" : "`r`n") line
    return out
}


ExitPromptRig(*) {
    RestoreNumLockState()
    ExitApp()
}

RestoreNumLockOnExit(*) {
    RestoreNumLockState()
}

RestoreNumLockState() {
    global originalNumLockState
    try SetNumLockState(originalNumLockState ? "On" : "Off")
}










