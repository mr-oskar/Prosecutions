import psutil
import time
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
                    "status": "Not detected - Desktop PC or no battery sensor"
                }
            
            time_left_formatted = None
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft > 0:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                time_left_formatted = f"{int(hours)}h {int(minutes)}m"
            
            health_percent = BatteryScanner._estimate_battery_health(battery.percent, battery.power_plugged)
            
            battery_info = {
                "detected": True,
                "percent": round(battery.percent, 2),
                "power_plugged": battery.power_plugged,
                "time_left_seconds": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft > 0 else None,
                "time_left_formatted": time_left_formatted,
                "capacity_max_wh": None,
                "capacity_current_wh": None,
                "health_percent": health_percent,
                "cycle_count": None,
                "voltage": None,
                "status": BatteryScanner._get_status(battery.percent, battery.power_plugged),
                "health_score": BatteryScanner._calculate_health_score(battery.percent, battery.power_plugged, health_percent)
            }
            
            return battery_info
            
        except Exception as e:
            return {
                "detected": False,
                "percent": None,
                "status": "Not detected"
            }
    
    @staticmethod
    def _estimate_battery_health(percent: float, power_plugged: bool) -> float:
        base_health = 95.0
        
        if percent < 80 and not power_plugged:
            base_health = 90.0
        elif percent < 50 and not power_plugged:
            base_health = 85.0
        
        return base_health
    
    @staticmethod
    def _get_status(percent: float, power_plugged: bool) -> str:
        if power_plugged:
            if percent >= 100:
                return "Fully Charged"
            elif percent >= 95:
                return "Almost Full"
            else:
                return "Charging"
        else:
            if percent < 10:
                return "Critical - Very Low Battery"
            elif percent < 20:
                return "Critical - Low Battery"
            elif percent < 40:
                return "Warning - Low Battery"
            elif percent < 60:
                return "Moderate"
            else:
                return "Good"
    
    @staticmethod
    def _calculate_health_score(percent: float, power_plugged: bool, health_percent: float) -> int:
        score = 100
        
        if not power_plugged:
            if percent < 10:
                score -= 50
            elif percent < 20:
                score -= 30
            elif percent < 40:
                score -= 15
        
        if health_percent < 70:
            score -= 30
        elif health_percent < 85:
            score -= 15
        
        return max(0, score)
    
    @staticmethod
    def perform_battery_drain_test(duration: int = 30) -> Dict[str, Any]:
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                return {
                    "test_passed": False,
                    "error": "No battery detected"
                }
            
            if battery.power_plugged:
                return {
                    "test_passed": False,
                    "error": "Battery is currently charging - Please disconnect power adapter for accurate test"
                }
            
            print(f"Starting battery drain test for {duration} seconds...")
            
            initial_percent = battery.percent
            samples = []
            
            start_time = time.time()
            
            while time.time() - start_time < duration:
                battery = psutil.sensors_battery()
                if battery:
                    samples.append({
                        "timestamp": time.time() - start_time,
                        "percent": battery.percent
                    })
                time.sleep(2)
            
            final_percent = battery.percent
            drain_rate = (initial_percent - final_percent) / (duration / 3600)
            
            estimated_time_remaining_hours = final_percent / drain_rate if drain_rate > 0 else 0
            
            return {
                "test_passed": True,
                "duration_seconds": duration,
                "initial_percent": round(initial_percent, 2),
                "final_percent": round(final_percent, 2),
                "drain_percent": round(initial_percent - final_percent, 4),
                "drain_rate_percent_per_hour": round(drain_rate, 2),
                "estimated_time_remaining_hours": round(estimated_time_remaining_hours, 2),
                "samples_collected": len(samples),
                "performance_rating": BatteryScanner._get_drain_rating(drain_rate)
            }
            
        except Exception as e:
            return {
                "test_passed": False,
                "error": str(e)
            }
    
    @staticmethod
    def _get_drain_rating(drain_rate: float) -> str:
        if drain_rate < 5:
            return "Excellent - Low power consumption"
        elif drain_rate < 10:
            return "Good - Normal power consumption"
        elif drain_rate < 20:
            return "Fair - Moderate power consumption"
        else:
            return "Poor - High power consumption - Check running programs"
