# Check if the Network Kill Switch scheduled task exists and its permissions

$TaskName = "NetworkKillSwitchApp"

Write-Host "=== Network Kill Switch Task Diagnostic ===" -ForegroundColor Cyan
Write-Host ""

# Check if task exists
$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if (-not $task) {
    # Check for old task name
    $oldTask = Get-ScheduledTask -TaskName "EthernetToggleApp" -ErrorAction SilentlyContinue
    if ($oldTask) {
        Write-Host "WARNING: Found old task name 'EthernetToggleApp'" -ForegroundColor Yellow
        Write-Host "Please reinstall the application to update to the new name." -ForegroundColor Yellow
        Write-Host ""
        exit 1
    }

    Write-Host "ERROR: Task '$TaskName' not found!" -ForegroundColor Red
    Write-Host "The scheduled task was not created by the installer." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To fix this:" -ForegroundColor White
    Write-Host "1. Uninstall and reinstall the application" -ForegroundColor Gray
    Write-Host "2. Make sure to check 'Start with Windows' during installation" -ForegroundColor Gray
    exit 1
}

Write-Host "✓ Task exists" -ForegroundColor Green
Write-Host ""

# Display task information
Write-Host "Task Information:" -ForegroundColor Yellow
Write-Host "  Name: $($task.TaskName)" -ForegroundColor Gray
Write-Host "  State: $($task.State)" -ForegroundColor Gray
Write-Host "  Last Run: $($task.LastRunTime)" -ForegroundColor Gray
Write-Host "  Last Result: $($task.LastTaskResult)" -ForegroundColor Gray
Write-Host ""

# Check principal
$principal = $task.Principal
Write-Host "Security Settings:" -ForegroundColor Yellow
Write-Host "  User: $($principal.UserId)" -ForegroundColor Gray
Write-Host "  Run Level: $($principal.RunLevel)" -ForegroundColor Gray
Write-Host "  Logon Type: $($principal.LogonType)" -ForegroundColor Gray
Write-Host ""

if ($principal.RunLevel -ne "Highest") {
    Write-Host "⚠ WARNING: Task is NOT configured to run with highest privileges!" -ForegroundColor Red
    Write-Host "   Current setting: $($principal.RunLevel)" -ForegroundColor Yellow
    Write-Host "   Expected: Highest" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To fix this:" -ForegroundColor White
    Write-Host "1. Uninstall the application" -ForegroundColor Gray
    Write-Host "2. Reinstall and ensure 'Start with Windows' is checked" -ForegroundColor Gray
} else {
    Write-Host "✓ Task is configured to run with highest privileges" -ForegroundColor Green
}

Write-Host ""

# Check action
$action = $task.Actions[0]
Write-Host "Action:" -ForegroundColor Yellow
Write-Host "  Executable: $($action.Execute)" -ForegroundColor Gray
Write-Host "  Arguments: $($action.Arguments)" -ForegroundColor Gray
Write-Host "  WorkingDir: $($action.WorkingDirectory)" -ForegroundColor Gray
Write-Host ""

# Check if executable exists
if (Test-Path $action.Execute) {
    Write-Host "✓ Executable exists" -ForegroundColor Green
} else {
    Write-Host "✗ ERROR: Executable not found at: $($action.Execute)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Recommendation ===" -ForegroundColor Cyan
Write-Host ""

if ($principal.RunLevel -eq "Highest" -and (Test-Path $action.Execute)) {
    Write-Host "The scheduled task appears to be configured correctly." -ForegroundColor Green
    Write-Host ""
    Write-Host "If the app still doesn't work after auto-start:" -ForegroundColor White
    Write-Host "1. Right-click the Start Menu shortcut and check 'Run as administrator'" -ForegroundColor Gray
    Write-Host "2. Check if your user account is in the Administrators group" -ForegroundColor Gray
    Write-Host "3. Try manually running: $($action.Execute)" -ForegroundColor Gray
} else {
    Write-Host "The scheduled task has configuration issues (see above)." -ForegroundColor Red
    Write-Host "Please reinstall the application." -ForegroundColor Yellow
}

Write-Host ""
