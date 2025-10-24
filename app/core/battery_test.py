import psutil
from typing import Dict, Any


class BatteryScanner:
    @staticmethod
    def get_battery_info() -> Dict[str, Any]:
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                return {
                    "detected": False,
                    "percent": None,
                    "power_plugged": None,
                    "status": "Not detected"
                }
            
            health_percent = 100.0
            
            battery_info = {
                "detected": True,
                "percent": round(battery.percent, 2),
                "power_plugged": battery.power_plugged,
                "time_left_seconds": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None,
                "capacity_max_wh": None,
                "capacity_current_wh": None,
                "health_percent": health_percent,
                "status": BatteryScanner._get_status(battery.percent, battery.power_plugged)
            }
            
            return battery_info
            
        except Exception as e:
            return {
                "detected": False,
                "percent": None,
                "status": f"Not detected"
            }
    
    @staticmethod
    def _get_status(percent: float, power_plugged: bool) -> str:
        if power_plugged:
            if percent >= 100:
                return "Fully Charged"
            else:
                return "Charging"
        else:
            if percent < 20:
                return "Critical - Low Battery"
            elif percent < 50:
                return "Low Battery"
            else:
                return "Good"
