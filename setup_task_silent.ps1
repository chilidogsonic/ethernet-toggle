# Silent PowerShell Script for Installer - Setup Ethernet Toggle Auto-Startup
# This is called by the Inno Setup installer to configure auto-startup

param(
    [Parameter(Mandatory=$true)]
    [string]$InstallPath
)

$ErrorActionPreference = "Stop"
$TaskName = "NetworkKillSwitchApp"

try {
    # Get the executable path
    $exePath = Join-Path $InstallPath "NetworkKillSwitch.exe"

    # Verify executable exists
    if (-not (Test-Path $exePath)) {
        Write-Error "Executable not found: $exePath"
        exit 1
    }

    # Remove existing task if it exists (including old name)
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false | Out-Null
    }
    # Also remove old task name if it exists
    $oldTask = Get-ScheduledTask -TaskName "EthernetToggleApp" -ErrorAction SilentlyContinue
    if ($oldTask) {
        Unregister-ScheduledTask -TaskName "EthernetToggleApp" -Confirm:$false | Out-Null
    }

    # Create scheduled task action
    $action = New-ScheduledTaskAction -Execute $exePath -WorkingDirectory $InstallPath

    # Create trigger for user logon
    $trigger = New-ScheduledTaskTrigger -AtLogOn

    # Create principal (run with highest privileges)
    $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest

    # Create settings
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 0)

    # Register the task
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description "Auto-start Network Kill Switch system tray application" | Out-Null

    exit 0

} catch {
    # Silent failure - log to event log if possible
    Write-EventLog -LogName Application -Source "Application" -EntryType Error -EventId 1000 -Message "Failed to setup Ethernet Toggle auto-start: $($_.Exception.Message)" -ErrorAction SilentlyContinue
    exit 1
}
