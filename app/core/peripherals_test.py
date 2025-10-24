import psutil
from typing import Dict, Any, List


class PeripheralsScanner:
    @staticmethod
    def get_peripherals_info() -> Dict[str, Any]:
        try:
            usb_devices = []
            audio_devices = []
            
            try:
                import subprocess
                import platform
                
                if platform.system() == 'Windows':
                    result = subprocess.run(['wmic', 'path', 'Win32_USBHub', 'get', 'DeviceID'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')[1:]
                        usb_devices = [line.strip() for line in lines if line.strip()]
                elif platform.system() == 'Linux':
                    result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        usb_devices = result.stdout.strip().split('\n')
            except:
                pass
            
            keyboard_detected = False
            mouse_detected = False
            display_detected = False
            
            for device in usb_devices:
                device_lower = device.lower()
                if 'keyboard' in device_lower or 'kbd' in device_lower:
                    keyboard_detected = True
                if 'mouse' in device_lower or 'pointing' in device_lower:
                    mouse_detected = True
            
            try:
                import subprocess
                import platform
                
                if platform.system() == 'Windows':
                    result = subprocess.run(['wmic', 'path', 'Win32_DesktopMonitor', 'get', 'DeviceID'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0 and len(result.stdout.strip().split('\n')) > 1:
                        display_detected = True
            except:
                pass
            
            peripherals_info = {
                "keyboard_detected": keyboard_detected,
                "mouse_detected": mouse_detected,
                "display_detected": display_detected,
                "audio_devices": audio_devices,
                "usb_devices": usb_devices[:10],
                "printers": [],
                "total_devices": len(usb_devices)
            }
            
            return peripherals_info
            
        except Exception as e:
            return {
                "keyboard_detected": False,
                "mouse_detected": False,
                "display_detected": False,
                "audio_devices": [],
                "usb_devices": [],
                "printers": [],
                "total_devices": 0
            }
