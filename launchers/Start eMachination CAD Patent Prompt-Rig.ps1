$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$runtime = Join-Path $root "src\eMachination_Coding_Prompt_Rig.ahk"
if (-not (Test-Path -LiteralPath $runtime -PathType Leaf)) {
    throw "Runtime not found: $runtime"
}
$exe = (Get-Command AutoHotkey64.exe -ErrorAction SilentlyContinue).Source
if (-not $exe) { $exe = (Get-Command AutoHotkey.exe -ErrorAction SilentlyContinue).Source }
if ($exe) {
    Start-Process -FilePath $exe -ArgumentList "`"$runtime`"" -WorkingDirectory (Split-Path $runtime -Parent)
} else {
    Invoke-Item $runtime
}
