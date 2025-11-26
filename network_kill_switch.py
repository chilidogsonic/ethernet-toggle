"""
Network Kill Switch - System Tray Application for Network Control
A lightweight Windows utility to quickly toggle Ethernet and WiFi adapters on/off
Version 2.0.0
"""
import subprocess
import pystray
from PIL import Image
import threading
import time
import sys
import os
import ctypes


def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class NetworkKillSwitch:
    def __init__(self, silent_mode=False):
        self.adapter_names = []  # List of adapter names (Ethernet + WiFi)
        self.is_enabled = False
        self.icon = None
        self.detecting_adapter = True
        self.silent_mode = silent_mode
        self.timer_thread = None
        self.timer_cancel = False
        self.timer_end_time = None
        self.is_loading = False
        self.loading_frame = 0
        self.animation_thread = None
        self.animation_running = False

        # Try to load custom icons using resource path for PyInstaller compatibility
        self.icon_on = self.load_icon('icons/status_on.ico')
        self.icon_off = self.load_icon('icons/status_off.ico')
        self.icon_loading_one = self.load_icon('icons/status_loading_one.ico')
        self.icon_loading_two = self.load_icon('icons/status_loading_two.ico')
        self.icon_timer = self.load_icon('icons/status_timer.ico')

    def load_icon(self, path):
        """Load icon from file if it exists - works with PyInstaller"""
        try:
            # Use get_resource_path for PyInstaller compatibility
            full_path = get_resource_path(path)
            if os.path.exists(full_path):
                return Image.open(full_path)
            # Fallback to relative path for development
            elif os.path.exists(path):
                return Image.open(path)
        except Exception as e:
            if not self.silent_mode:
                print(f"Could not load icon {path}: {e}")
        return None

    def create_icon_image(self):
        """Create or load icon image based on current state"""
        from PIL import ImageDraw

        # Priority 1: Loading state (toggling in progress)
        if self.is_loading:
            if self.loading_frame % 2 == 0:
                if self.icon_loading_one:
                    return self.icon_loading_one
            else:
                if self.icon_loading_two:
                    return self.icon_loading_two

        # Priority 2: Timer active (adapter off, timer running)
        if self.timer_end_time and time.time() < self.timer_end_time:
            if self.icon_timer:
                return self.icon_timer

        # Priority 3: Normal on/off states
        if self.is_enabled and self.icon_on:
            return self.icon_on
        elif not self.is_enabled and self.icon_off:
            return self.icon_off

        # Fallback to generated icon if assets missing
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw a circle
        color = (0, 255, 0, 255) if self.is_enabled else (255, 0, 0, 255)
        draw.ellipse([8, 8, 56, 56], fill=color, outline=(255, 255, 255, 255))

        # Draw ethernet symbol (simplified)
        draw.rectangle([24, 20, 40, 24], fill=(255, 255, 255, 255))
        draw.rectangle([28, 24, 36, 44], fill=(255, 255, 255, 255))

        return image

    def start_loading_animation(self):
        """Start the loading animation thread"""
        if self.animation_running:
            return

        def animate():
            self.animation_running = True
            while self.is_loading:
                self.loading_frame = (self.loading_frame + 1) % 2
                self.update_icon()
                time.sleep(0.2)  # 200ms between frames for visible animation
            self.animation_running = False

        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()

    def find_network_adapters(self):
        """Find all Ethernet and WiFi adapters"""
        try:
            # PowerShell command to get all physical network adapters (Ethernet + WiFi)
            # Exclude virtual adapters, Bluetooth, etc.
            ps_command = "Get-NetAdapter | Where-Object {($_.InterfaceDescription -like '*Ethernet*' -or $_.InterfaceDescription -like '*Wi-Fi*' -or $_.InterfaceDescription -like '*Wireless*' -or $_.Name -like '*Ethernet*' -or $_.Name -like '*Wi-Fi*' -or $_.Name -like '*Wireless*') -and $_.Virtual -eq $false} | ConvertTo-Json"

            result = subprocess.run(
                ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )

            if result.returncode == 0 and result.stdout.strip():
                import json
                data = json.loads(result.stdout)

                # Handle both single adapter (dict) and multiple adapters (list)
                if isinstance(data, dict):
                    adapters = [data]
                else:
                    adapters = data

                self.adapter_names = [adapter['Name'] for adapter in adapters]

                # Check if any adapter is enabled
                self.is_enabled = any(adapter['Status'] == 'Up' for adapter in adapters)

                if not self.silent_mode:
                    print(f"Found {len(self.adapter_names)} adapter(s): {', '.join(self.adapter_names)}")

                return len(self.adapter_names) > 0
        except Exception as e:
            if not self.silent_mode:
                print(f"Error finding adapters: {e}")

        return False

    def get_adapter_status(self):
        """Check if any adapter is currently enabled"""
        if not self.adapter_names:
            return False

        try:
            # Check status of all adapters
            for adapter_name in self.adapter_names:
                ps_command = f"Get-NetAdapter -Name '{adapter_name}' | Select-Object Status"
                result = subprocess.run(
                    ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', ps_command],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
                # If any adapter is up, return True
                if 'Up' in result.stdout:
                    return True
            return False
        except:
            return False

    def verify_status_change(self, expected_status, max_attempts=10, delay=0.5):
        """Verify that the adapter status has changed to expected state"""
        for attempt in range(max_attempts):
            time.sleep(delay)
            current_status = self.get_adapter_status()
            if current_status == expected_status:
                return True
        return False

    def toggle_adapter(self, enable=None):
        """Toggle all network adapters (Ethernet + WiFi) on/off"""
        if not self.adapter_names:
            return

        # Determine target state
        if enable is None:
            target_enabled = not self.is_enabled
        else:
            target_enabled = enable

        # If manually toggling back on while timer is active, cancel the timer
        if target_enabled and self.timer_end_time:
            self.cancel_timer()

        # Show loading indicator with animation
        self.is_loading = True
        self.start_loading_animation()

        try:
            # Toggle all adapters
            for adapter_name in self.adapter_names:
                if target_enabled:
                    # Enable adapter
                    ps_command = f"Enable-NetAdapter -Name '{adapter_name}' -Confirm:$false"
                else:
                    # Disable adapter
                    ps_command = f"Disable-NetAdapter -Name '{adapter_name}' -Confirm:$false"

                result = subprocess.run(
                    ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', ps_command],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )

                # Check for errors in stderr
                if result.returncode != 0 and not self.silent_mode:
                    print(f"PowerShell error for {adapter_name}: {result.stderr}")

            # Verify the status change
            if self.verify_status_change(target_enabled):
                self.is_enabled = target_enabled
            else:
                # Force check current status if verification failed
                self.is_enabled = self.get_adapter_status()

        except subprocess.CalledProcessError as e:
            if not self.silent_mode:
                print(f"Error toggling adapters: {e}")
            # Still update to actual state
            self.is_enabled = self.get_adapter_status()
        except Exception as e:
            if not self.silent_mode:
                print(f"Unexpected error toggling adapters: {e}")
            # Still update to actual state
            self.is_enabled = self.get_adapter_status()
        finally:
            # Clear loading state and update icon to reflect actual state
            self.is_loading = False
            self.update_icon()

    def format_time_remaining(self):
        """Format the remaining time for display"""
        if not self.timer_end_time:
            return ""

        remaining = int(self.timer_end_time - time.time())
        if remaining <= 0:
            return ""

        if remaining >= 3600:
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            return f"{hours}h {minutes}m"
        elif remaining >= 60:
            minutes = remaining // 60
            seconds = remaining % 60
            return f"{minutes}m {seconds}s"
        else:
            return f"{remaining}s"

    def update_tooltip(self):
        """Update only the tooltip text without changing the icon"""
        if self.icon:
            # Build status text for tooltip only
            status = "Enabled" if self.is_enabled else "Disabled"

            # Add timer info to tooltip if active
            if self.timer_end_time and time.time() < self.timer_end_time:
                time_left = self.format_time_remaining()
                if time_left:
                    status += f" (Re-enabling in {time_left})"

            # Add loading indicator to tooltip
            if self.is_loading:
                status += " [Processing...]"

            self.icon.title = f"Network: {status}"

    def update_icon(self):
        """Update the tray icon and tooltip based on adapter state"""
        if self.icon:
            self.icon.icon = self.create_icon_image()
            self.update_tooltip()

    def cancel_timer(self):
        """Cancel any running timer"""
        self.timer_cancel = True
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1)
        self.timer_cancel = False
        self.timer_end_time = None

    def start_timer(self, seconds):
        """Disable adapter for a specified duration, then re-enable"""
        def timer_worker():
            # Disable the adapter
            self.toggle_adapter(enable=False)

            # Set timer end time
            self.timer_end_time = time.time() + seconds

            # Update icon to show timer icon
            self.update_icon()

            # Wait for the specified duration (check for cancellation)
            # Update tooltip every second to show countdown
            while not self.timer_cancel and time.time() < self.timer_end_time:
                self.update_tooltip()
                time.sleep(1)

            # Clear timer end time
            self.timer_end_time = None

            # Re-enable the adapter if timer wasn't cancelled
            if not self.timer_cancel:
                self.toggle_adapter(enable=True)

        # Cancel any existing timer
        self.cancel_timer()

        # Start new timer thread
        self.timer_thread = threading.Thread(target=timer_worker, daemon=True)
        self.timer_thread.start()

    def on_toggle_click(self, icon, item):
        """Handle toggle menu item click"""
        self.toggle_adapter()

    def on_left_click(self, icon, item=None):
        """Handle left-click on icon - quick toggle"""
        self.toggle_adapter()

    def on_timer_click(self, icon, item):
        """Handle timer menu item click"""
        # Extract duration from menu item text
        text = str(item)
        if "1 minute" in text:
            self.start_timer(60)
        elif "2 minutes" in text:
            self.start_timer(120)
        elif "5 minutes" in text:
            self.start_timer(300)
        elif "30 minutes" in text:
            self.start_timer(1800)
        elif "1 hour" in text:
            self.start_timer(3600)

    def on_cancel_timer(self, icon, item):
        """Handle cancel timer menu item"""
        self.cancel_timer()
        self.toggle_adapter(enable=True)  # Ensure adapter is back on

    def on_quit(self, icon, item):
        """Handle quit menu item click"""
        self.cancel_timer()
        icon.stop()

    def setup_icon(self):
        """Setup the system tray icon"""
        # Initial detection
        if not self.find_network_adapters():
            if not self.silent_mode:
                print("Warning: Could not find network adapters")
            self.adapter_names = []  # Empty list if none found

        self.detecting_adapter = False

        # Create flat menu with all options
        menu = pystray.Menu(
            pystray.MenuItem(
                lambda text: f"Toggle Network ({'On' if not self.is_enabled else 'Off'})",
                self.on_toggle_click,
                default=True  # Left-click action
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Disable for 1 minute", self.on_timer_click),
            pystray.MenuItem("Disable for 2 minutes", self.on_timer_click),
            pystray.MenuItem("Disable for 5 minutes", self.on_timer_click),
            pystray.MenuItem("Disable for 30 minutes", self.on_timer_click),
            pystray.MenuItem("Disable for 1 hour", self.on_timer_click),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Cancel Timer", self.on_cancel_timer),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.on_quit)
        )

        # Create icon
        status = "Enabled" if self.is_enabled else "Disabled"
        self.icon = pystray.Icon(
            "network_toggle",
            self.create_icon_image(),
            f"Network: {status}",
            menu
        )

        # Run icon
        self.icon.run()


def main():
    """Main entry point"""
    # Check for silent mode flag
    silent_mode = '--silent' in sys.argv or len(sys.argv) == 1 and os.path.basename(sys.executable) == 'pythonw.exe'

    if not silent_mode:
        print("Starting Network Kill Switch...")
        print("Note: This application requires administrator privileges to toggle network adapters.")

    # Check for admin privileges
    if not is_admin():
        if not silent_mode:
            print("WARNING: Not running as administrator!")
            print("The application will start, but toggle functionality may not work.")
            print("Please run as administrator for full functionality.")

    app = NetworkKillSwitch(silent_mode=silent_mode)
    app.setup_icon()


if __name__ == "__main__":
    main()
