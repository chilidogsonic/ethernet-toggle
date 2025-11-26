# Troubleshooting Ethernet Toggle

## Problem: Toggle Doesn't Work After Installation

If you installed Ethernet Toggle and it doesn't toggle your adapter on/off, follow these steps:

### Step 1: Verify the App is Running as Administrator

The app **MUST** run with administrator privileges to toggle network adapters.

#### Check if Auto-Start is Configured Correctly

1. Open PowerShell as Administrator
2. Navigate to installation folder: `cd "C:\Program Files\Ethernet Toggle"`
3. Run the diagnostic: `.\check_task_permissions.ps1`

This will tell you if the scheduled task is configured correctly.

**Expected output:**
```
✓ Task exists
✓ Task is configured to run with highest privileges
✓ Executable exists
```

If you see errors, **reinstall the application** and make sure to check "Start with Windows" during installation.

---

### Step 2: Test Manual Launch

Try running the app manually as administrator:

1. Open Start Menu
2. Find "Ethernet Toggle"
3. Right-click → "Run as administrator"
4. The system tray icon should appear
5. Try clicking it to toggle

**If this works:** The app works, but auto-start needs fixing. See Step 1.

**If this doesn't work:** Continue to Step 3.

---

### Step 3: Check Your User Account Permissions

The app requires:
- Your user account must be in the **Administrators** group
- Windows UAC (User Account Control) must be enabled

To check:

1. Open Command Prompt and run: `net user %USERNAME%`
2. Look for "Local Group Memberships"
3. You should see "Administrators" listed

If you're **not** in the Administrators group, you'll need to:
- Ask your system administrator to add you, OR
- Use an administrator account

---

### Step 4: Verify Ethernet Adapter Name

The app automatically detects adapters with "Ethernet" in the name.

1. Open Device Manager (Win+X → Device Manager)
2. Expand "Network adapters"
3. Look for an adapter with "Ethernet" in its name

**If your adapter has a different name** (e.g., "LAN", "Network Connection"), the app won't find it.

**To fix this:** Contact support or modify the adapter detection in the source code.

---

### Step 5: Check Windows Event Logs

If nothing above works, check for error messages:

1. Open Event Viewer (Win+X → Event Viewer)
2. Go to: Windows Logs → Application
3. Look for errors from "EthernetToggle" or "Task Scheduler"

This may reveal why the app is failing.

---

## Problem: Auto-Start Not Working

If the app doesn't start automatically when Windows boots:

### Solution 1: Verify Scheduled Task Exists

1. Open Task Scheduler (search "Task Scheduler" in Start Menu)
2. Look for "EthernetToggleApp" in the task list
3. Check if it's **Enabled**
4. Look at "Last Run Time" and "Last Run Result"

**If task doesn't exist:** Reinstall and check "Start with Windows" during setup.

**If task exists but doesn't run:** Right-click → Properties → Check these settings:
- **General tab:** "Run with highest privileges" should be checked
- **Triggers tab:** Should have "At log on" trigger
- **Actions tab:** Should point to the EXE in Program Files

### Solution 2: Manually Recreate the Task

1. Uninstall Ethernet Toggle
2. Reinstall
3. **Make sure to check** "Start with Windows" during installation
4. Restart Windows
5. Check if icon appears in system tray

---

## Problem: Icons Not Displaying Correctly

If you see wrong icons or generic icons:

1. Check that these files exist in `C:\Program Files\Ethernet Toggle\icons\`:
   - `status_on.ico`
   - `status_off.ico`
   - `status_loading_one.ico`
   - `status_loading_two.ico`
   - `status_timer.ico`

2. If files are missing, **reinstall the application**

---

## Problem: "Access Denied" or Permission Errors

This means the app is **not** running with administrator privileges.

**Fix:**
1. When running manually: Always right-click → "Run as administrator"
2. For auto-start: Verify scheduled task has "Run with highest privileges" (see Step 1 above)

---

## Still Having Issues?

### Reinstall Clean

1. **Uninstall** Ethernet Toggle completely
2. **Restart** Windows
3. **Reinstall** the application
4. During installation: **Check** "Start with Windows"
5. After installation: **Do not** click "Launch" yet
6. **Restart** Windows again
7. The app should auto-start with admin privileges

### Get Support

If none of the above works:

1. Run `check_task_permissions.ps1` and save the output
2. Check Event Viewer for errors
3. Open an issue at: https://github.com/chilidogsonic/ethernet-toggle/issues

Include:
- Windows version (10 or 11)
- Output from `check_task_permissions.ps1`
- Any error messages from Event Viewer
- Whether manual "Run as administrator" works

---

## Quick Reference

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Toggle doesn't work | Not running as admin | Run as admin or fix scheduled task |
| Auto-start doesn't work | Scheduled task not created | Reinstall with "Start with Windows" checked |
| "Adapter not found" | Wrong adapter name | Check adapter name in Device Manager |
| Icons are wrong | Missing icon files | Reinstall application |
| UAC prompt every time | Scheduled task not configured | Use scheduled task instead of shortcut |
