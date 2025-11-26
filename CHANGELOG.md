# Changelog

All notable changes to Network Kill Switch will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-XX

### 🎉 Major Release: Ethernet Toggle → Network Kill Switch

This release represents a complete evolution of the project from a simple Ethernet toggle utility to a full-featured network management tool. The application has been rebranded as **Network Kill Switch** to better reflect its expanded capabilities.

### Added

#### Core Features
- **WiFi Support** - Now controls WiFi adapters in addition to Ethernet adapters
- **Multi-Adapter Control** - Simultaneously manages all physical network adapters (Ethernet + WiFi)
- **Timer Function** - Temporarily disable network with automatic restoration:
  - 1 minute preset
  - 2 minutes preset
  - 5 minutes preset
  - 30 minutes preset
  - 1 hour preset
- **Live Countdown Display** - Real-time countdown in system tray tooltip showing time remaining
- **Cancel Timer Option** - Ability to stop timer and immediately restore network
- **Left-Click Quick Toggle** - Instant network toggle without opening menu
- **Loading Animation** - Visual feedback during network state transitions
- **Status Verification** - Automatic verification of adapter state after each toggle operation

#### User Interface
- **Custom Icon States** - Distinct icons for different operational states:
  - Green icon (network enabled)
  - Red icon (network disabled)
  - Loading animation frames (operation in progress)
  - Timer icon (temporary disable mode)
- **Enhanced Tooltips** - Informative hover text showing current state and countdown
- **Improved Menu Structure** - Organized right-click menu with clear options

#### Technical Improvements
- **Better Error Handling** - More robust PowerShell execution with better error messages
- **ARM64 Compatibility** - Confirmed support for Windows on ARM via x64 emulation
- **Resource Path Resolution** - Proper icon loading in both development and compiled environments
- **Background Threading** - Non-blocking operations for smoother user experience
- **Admin Privilege Detection** - Automatic checking and warning for administrator rights

### Changed

#### Branding & Naming
- **Project renamed** from "Ethernet Toggle" to "Network Kill Switch"
- **Class renamed** from `EthernetToggle` to `NetworkKillSwitch`
- **Executable renamed** from `EthernetToggle.exe` to `NetworkKillSwitch.exe`
- **Installer renamed** to `NetworkKillSwitch-Setup.exe`
- **Repository URL** updated to reflect new name
- **All documentation** updated with new branding

#### Functionality
- **Expanded adapter support** - Now targets both Ethernet and WiFi (previously Ethernet only)
- **Improved adapter detection** - More comprehensive PowerShell query for finding adapters
- **Enhanced PowerShell execution** - Array-based arguments instead of shell=True for reliability
- **Window suppression** - Added CREATE_NO_WINDOW flag to prevent console flash
- **Status monitoring** - Continuous status tracking with real-time updates

#### User Experience
- **Simplified menu** - Flat structure instead of nested submenus
- **Clearer labeling** - More descriptive menu item text
- **Better feedback** - Visual and textual indicators for all states
- **Default action** - Left-click performs most common operation (toggle)

### Fixed

#### Critical Bugs
- **Icon loading in compiled EXE** - Fixed path resolution using PyInstaller's `_MEIPASS`
- **PowerShell subprocess failures** - Replaced shell=True with proper array-based arguments
- **Console window flashing** - Added CREATE_NO_WINDOW flag for clean execution
- **Missing resources** - Properly bundle all icon files in PyInstaller spec

#### Minor Issues
- **Admin privilege warnings** - Added explicit detection and user notifications
- **Silent mode detection** - Improved logic for console-less execution
- **Error message handling** - Better stderr capture and reporting

### Security

- **UAC Integration** - Automatic elevation prompt via embedded manifest
- **No registry modifications** - Uses Task Scheduler instead for auto-startup
- **Clean uninstall** - Removes all traces including scheduled tasks

### Documentation

- **Complete README rewrite** - Comprehensive documentation with:
  - Feature overview with screenshots
  - Installation instructions for users and developers
  - Usage guide with tips and tricks
  - Troubleshooting section with common issues
  - Technical architecture explanation
  - Contributing guidelines
- **New CHANGELOG** - This file, following Keep a Changelog format
- **Updated BUILD.md** - Build instructions for developers
- **Enhanced TROUBLESHOOTING.md** - Expanded troubleshooting scenarios

### Deprecated

- **Old batch files** - Removed `run_ethernet_toggle.bat` (obsolete)
- **Development notes** - Removed internal documentation files:
  - FIXES_APPLIED.md (content integrated into CHANGELOG)
  - NEW_FEATURES.md (content integrated into CHANGELOG)
  - UPDATES_V2.md (consolidated)
  - INSTALLER_FIXES.md (consolidated)
  - MANIFEST_SOLUTION.md (consolidated)
  - FINAL_SOLUTION.md (consolidated)
  - WIFI_AND_ARM_SUPPORT.md (integrated into README)

### Removed

- **Test scripts** - Removed `test_toggle.py` (developer utility, not needed in releases)
- **Icon generation script** - Removed `create_icons.py` (one-time utility)
- **Build artifacts** - Cleaned up old build directories

---

## [1.0.0] - 2025-01-XX

### Initial Release: Ethernet Toggle

The first public release of the project under the name "Ethernet Toggle".

### Added

- **Basic Ethernet Control** - Enable/disable Ethernet adapter via system tray
- **System Tray Icon** - Persistent system tray presence
- **Right-Click Menu** - Simple menu for toggling adapter
- **Status Indicators** - Green (enabled) and red (disabled) icons
- **PowerShell Integration** - Uses native Windows commands for adapter control
- **PyInstaller Packaging** - Standalone executable for end users
- **Inno Setup Installer** - Professional Windows installer
- **Auto-Startup Option** - Optional start with Windows via Task Scheduler
- **Administrator Support** - Runs with elevated privileges

### Technical

- **Python 3.7+** - Modern Python codebase
- **pystray** - System tray library
- **Pillow** - Icon rendering
- **Windows 10/11** - Target platform

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version (X.0.0) - Incompatible API changes or major feature additions
- **MINOR** version (0.X.0) - New features in a backwards-compatible manner
- **PATCH** version (0.0.X) - Backwards-compatible bug fixes

---

## Upgrade Notes

### Upgrading from 1.x to 2.0

**Breaking Changes:**
- Executable name changed from `EthernetToggle.exe` to `NetworkKillSwitch.exe`
- Scheduled task name changed from "EthernetToggleApp" to "NetworkKillSwitchApp"
- Installation directory changed to `C:\Program Files\Network Kill Switch`

**Migration Steps:**
1. Uninstall version 1.x using Windows Settings
2. Install version 2.0 using the new installer
3. Reconfigure auto-startup if desired (handled by installer)

**Note:** There is no automatic migration. Version 2.0 is a clean install.

---

## Future Roadmap

Potential features for future releases (not committed):

### Version 2.1 (Potential)
- Custom timer durations (user input)
- Keyboard shortcuts / hotkeys
- Toast notifications for state changes
- System startup behavior options
- Settings configuration UI

### Version 2.2 (Potential)
- Network statistics tracking
- Connection history log
- Scheduled enable/disable times
- Per-adapter individual control
- Profile-based configurations

### Version 3.0 (Potential)
- GUI configuration window
- Advanced filtering (per-adapter control)
- Integration with VPN services
- Firewall rule management
- Network traffic monitoring

---

## Links

- **Repository:** https://github.com/chilidogsonic/network-kill-switch
- **Issue Tracker:** https://github.com/chilidogsonic/network-kill-switch/issues
- **Releases:** https://github.com/chilidogsonic/network-kill-switch/releases
- **Documentation:** https://github.com/chilidogsonic/network-kill-switch#readme

---

## Credits

Developed by the Network Kill Switch team.
Originally created as "Ethernet Toggle" and evolved into a comprehensive network management tool.

**Contributors:**
- Primary development and maintenance
- Community feedback and testing
- Bug reports and feature suggestions

Thank you to all users and contributors who made this project possible!
