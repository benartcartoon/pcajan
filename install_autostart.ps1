# One-time setup. Run in PowerShell while logged in as the Windows user.
$ErrorActionPreference = 'Stop'
$repo = Join-Path $env:USERPROFILE 'pcajan'
if (-not (Test-Path (Join-Path $repo 'agent.py'))) { throw "Missing agent.py in $repo" }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Install Git first.' }
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Install GitHub CLI (gh) first.' }
    winget install --id GitHub.cli --exact --accept-package-agreements --accept-source-agreements
    $env:Path += ';' + $env:ProgramFiles + '\GitHub CLI'
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw 'Restart PowerShell and run installer again: gh not found.' }
Push-Location $repo
try { git pull --ff-only; if ($LASTEXITCODE -ne 0) { throw 'Git pull failed.' } } finally { Pop-Location }
if (-not (Test-Path (Join-Path $repo 'remote_agent.py'))) { throw 'remote_agent.py missing after git pull.' }
# PowerShell 5 can turn native stderr output into a terminating error under Stop.
# Check exit status via stdout-only redirection to avoid aborting before gh auth login.
$authStatus = & gh auth status 2>&1 | Out-String
if ($LASTEXITCODE -ne 0) {
    Write-Host 'GitHub sign-in required. A browser sign-in will open; do not share authentication codes.'
    & gh auth login --hostname github.com --git-protocol https --web
    if ($LASTEXITCODE -ne 0) { throw 'GitHub login failed.' }
}
& gh api repos/benartcartoon/kontrol --jq .full_name | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'No access to private control repository.' }
$pythonCommand = Get-Command pythonw.exe -ErrorAction SilentlyContinue
if (-not $pythonCommand) { $pythonCommand = Get-Command python.exe -ErrorAction Stop }
$python = $pythonCommand.Source
$taskName = 'PC-Ajan-Remote'
$action = New-ScheduledTaskAction -Execute $python -Argument ('"' + (Join-Path $repo 'remote_agent.py') + '"') -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$settings = New-ScheduledTaskSettingsSet -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit (New-TimeSpan -Seconds 0) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description 'Restricted GitHub issue Colab controller' -Force | Out-Null
Start-ScheduledTask -TaskName $taskName
Write-Host 'Remote controller installed and started. GitHub issues in private kontrol repo can request COLAB_OPEN.'
Write-Host 'COLAB_CLOSE is intentionally disabled until verified browser/runtime integration is implemented.'
Write-Host 'Existing agent.py and its scheduled tasks were not modified.'
