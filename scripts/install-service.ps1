# Install Fartlek as a Windows Scheduled Task, autostarted at logon.
# Run from the repo root in PowerShell:  .\scripts\install-service.ps1
# Optional: -Venv C:\path\to\venv  (defaults to .venv in the repo, then ~\.venvs\fartlek)
param(
    [string]$Venv = ""
)

$ErrorActionPreference = "Stop"
$RepoDir = Split-Path -Parent $PSScriptRoot

if (-not $Venv) {
    if (Test-Path (Join-Path $RepoDir ".venv")) {
        $Venv = Join-Path $RepoDir ".venv"
    } else {
        $Venv = Join-Path $HOME ".venvs\fartlek"
    }
}

$Uvicorn = Join-Path $Venv "Scripts\uvicorn.exe"
if (-not (Test-Path $Uvicorn)) {
    Write-Error "No uvicorn found at $Uvicorn - set up the venv first (see README)."
}

$TaskName = "Fartlek"
$Action = New-ScheduledTaskAction -Execute $Uvicorn `
    -Argument "backend.main:app --host 127.0.0.1 --port 8077" `
    -WorkingDirectory $RepoDir
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Days 3650)

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger `
    -Settings $Settings | Out-Null
Start-ScheduledTask -TaskName $TaskName

Write-Host "Installed and started scheduled task '$TaskName'."
Write-Host "App: http://127.0.0.1:8077"
Write-Host "Note: a console window may appear at logon; to hide it, edit the task in"
Write-Host "Task Scheduler and set 'Run whether user is logged on or not'."
