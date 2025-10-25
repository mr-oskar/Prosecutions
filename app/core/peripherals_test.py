import psutil
import platform
import subprocess
from typing import Dict, Any, List


class PeripheralsScanner:
    @staticmethod
    def get_peripherals_info() -> Dict[str, Any]:
        try:
            usb_devices = PeripheralsScanner._get_usb_devices()
            audio_devices = PeripheralsScanner._get_audio_devices()
            displays = PeripheralsScanner._get_display_info()
            
            keyboard_detected = False
            mouse_detected = False
            
            for device in usb_devices:
                device_lower = device.lower()
                if any(keyword in device_lower for keyword in ['keyboard', 'kbd', 'keybrd']):
                    keyboard_detected = True
                if any(keyword in device_lower for keyword in ['mouse', 'pointing', 'trackpad', 'touchpad']):
                    mouse_detected = True
            
            peripherals_info = {
                "keyboard_detected": keyboard_detected,
                "mouse_detected": mouse_detected,
                "displays": displays,
                "audio_devices": audio_devices,
                "usb_devices": usb_devices,
                "usb_device_count": len(usb_devices),
                "bluetooth_devices": [],
                "printers": [],
                "webcams": PeripheralsScanner._detect_webcams(),
                "status": "Good" if keyboard_detected and mouse_detected else "Warning - Some peripherals not detected"
            }
            
            return peripherals_info
            
        except Exception as e:
            return {
                "keyboard_detected": False,
                "mouse_detected": False,
                "displays": [],
                "audio_devices": [],
                "usb_devices": [],
                "usb_device_count": 0,
                "status": f"Error: {str(e)}"
            }
    
    @staticmethod
    def _get_usb_devices() -> List[str]:
        usb_devices = []
        
        try:
            system = platform.system()
            
            if system == 'Windows':
                result = subprocess.run(
                    ['wmic', 'path', 'Win32_USBHub', 'get', 'DeviceID,Description'], 
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]
                    usb_devices = [line.strip() for line in lines if line.strip()]
            
            elif system == 'Linux':
                result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    usb_devices = result.stdout.strip().split('\n')
            
            elif system == 'Darwin':
                result = subprocess.run(['system_profiler', 'SPUSBDataType'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    usb_devices = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        except Exception:
            pass
        
        return usb_devices[:20]
    
    @staticmethod
    def _get_audio_devices() -> List[Dict[str, Any]]:
        audio_devices = []
        
        try:
            system = platform.system()
            
            if system == 'Windows':
                result = subprocess.run(
                    ['wmic', 'path', 'Win32_SoundDevice', 'get', 'Name,Status'], 
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]
                    for line in lines:
                        if line.strip():
                            parts = line.strip().rsplit(None, 1)
                            if len(parts) >= 1:
                                audio_devices.append({
                                    "name": parts[0],
                                    "status": parts[1] if len(parts) > 1 else "Unknown"
                                })
            
            elif system == 'Linux':
                result = subprocess.run(['aplay', '-l'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if 'card' in line.lower():
                            audio_devices.append({
                                "name": line.strip(),
                                "status": "Active"
                            })
        
        except Exception:
            pass
        
        return audio_devices
    
    @staticmethod
    def _get_display_info() -> List[Dict[str, Any]]:
        displays = []
        
        try:
            system = platform.system()
            
            if system == 'Windows':
                result = subprocess.run(
                    ['wmic', 'path', 'Win32_DesktopMonitor', 'get', 'Name,ScreenWidth,ScreenHeight'], 
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]
                    for line in lines:
                        if line.strip():
                            displays.append({
                                "name": line.strip(),
                                "resolution": "Unknown"
                            })
            
            elif system == 'Linux':
                result = subprocess.run(['xrandr'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if ' connected' in line:
                            parts = line.split()
                            display_name = parts[0]
                            resolution = "Unknown"
                            for part in parts:
                                if 'x' in part and part[0].isdigit():
                                    resolution = part.split('+')[0]
                                    break
                            displays.append({
                                "name": display_name,
                                "resolution": resolution
                            })
        
        except Exception:
            pass
        
        if not displays:
            displays.append({
                "name": "Primary Display",
                "resolution": "Unknown"
            })
        
        return displays
    
    @staticmethod
    def _detect_webcams() -> List[Dict[str, Any]]:
        webcams = []
        
        try:
            system = platform.system()
            
            if system == 'Windows':
                result = subprocess.run(
                    ['wmic', 'path', 'Win32_PnPEntity', 'where', "PNPClass='Camera'", 'get', 'Name'], 
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]
                    for line in lines:
                        if line.strip():
                            webcams.append({
                                "name": line.strip(),
                                "status": "Available"
                            })
            
            elif system == 'Linux':
                import os
                video_devices = [f'/dev/video{i}' for i in range(10) if os.path.exists(f'/dev/video{i}')]
                for device in video_devices:
                    webcams.append({
                        "name": device,
                        "status": "Available"
                    })
        
        except Exception:
            pass
        
        return webcams
