# One-time installer for the restricted remote controller.
$ErrorActionPreference = 'Stop'
$repo = Join-Path $env:USERPROFILE 'pcajan'
if (-not (Test-Path (Join-Path $repo 'remote_agent.py'))) { throw "Missing remote_agent.py in $repo. Pull repository first." }
$ghCommand = Get-Command gh.exe -ErrorAction SilentlyContinue
$gh = if ($ghCommand) { $ghCommand.Source } else { Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe' }
if (-not (Test-Path $gh)) { throw 'GitHub CLI is not installed. Install it first, then retry.' }
$env:Path = (Split-Path $gh) + ';' + $env:Path
# PowerShell 5 may promote native stderr to an error under Stop. Probe authentication without stderr.
$oldPreference = $ErrorActionPreference
try {
    $ErrorActionPreference = 'Continue'
    & $gh auth token 2>$null | Out-Null
    $signedIn = ($LASTEXITCODE -eq 0)
} finally { $ErrorActionPreference = $oldPreference }
if (-not $signedIn) {
    Write-Host 'GitHub login required. Complete authentication in your browser; never share codes.'
    & $gh auth login --hostname github.com --git-protocol https --web
    if ($LASTEXITCODE -ne 0) { throw 'GitHub login failed.' }
}
& $gh api repos/benartcartoon/kontrol --jq .full_name | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Private control repository is inaccessible.' }
$pythonCommand = Get-Command pythonw.exe -ErrorAction SilentlyContinue
if (-not $pythonCommand) { $pythonCommand = Get-Command python.exe -ErrorAction Stop }
$python = $pythonCommand.Source
$taskName = 'PC-Ajan-Remote'
$action = New-ScheduledTaskAction -Execute $python -Argument ('"' + (Join-Path $repo 'remote_agent.py') + '"') -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$settings = New-ScheduledTaskSettingsSet -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit (New-TimeSpan -Seconds 0) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description 'Restricted GitHub issue Colab controller' -Force | Out-Null
Start-ScheduledTask -TaskName $taskName
Start-Sleep -Seconds 3
$task = Get-ScheduledTask -TaskName $taskName
$info = Get-ScheduledTaskInfo -TaskName $taskName
Write-Host "TASK_STATE=$($task.State) LAST_RESULT=$($info.LastTaskResult)"
Write-Host 'COLAB_OPEN enabled (browser launch only, page load unverified). COLAB_CLOSE disabled.'
Write-Host 'Old agent and its tasks unchanged.'
