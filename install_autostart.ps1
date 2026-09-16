# Run once in PowerShell after reviewing this script.
# Installs a per-user Windows logon scheduled task; does not alter agent.py.
$ErrorActionPreference = 'Stop'
$repo = Join-Path $env:USERPROFILE 'pcajan'
$agent = Join-Path $repo 'agent.py'
if (-not (Test-Path $agent)) { throw "Agent not found: $agent" }
$python = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $python) { $python = (Get-Command python.exe -ErrorAction Stop).Source }
$taskName = 'PC-Ajan-Autostart'
$action = New-ScheduledTaskAction -Execute $python -Argument ('"' + $agent + '"') -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$settings = New-ScheduledTaskSettingsSet -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit (New-TimeSpan -Seconds 0) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description 'Start PC agent at Windows logon' -Force | Out-Null
Write-Host "Installed $taskName. Agent will start automatically at next sign-in."
Write-Host 'This only configures startup. It does not connect ChatGPT to the remote job queue or fix Chrome tab targeting.'