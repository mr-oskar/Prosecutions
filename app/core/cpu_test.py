import psutil
import platform
from typing import Dict, Any, Optional


class CPUScanner:
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        try:
            cpu_freq = psutil.cpu_freq()
            cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
            
            temps = None
            try:
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
            except:
                pass
            
            temperature = None
            if temps:
                for name, entries in temps.items():
                    if entries:
                        temperature = entries[0].current
                        break
            
            processor_id = platform.processor()
            
            cpu_info = {
                "detected": True,
                "model": processor_id if processor_id else "Unknown CPU",
                "cores_physical": psutil.cpu_count(logical=False),
                "cores_logical": psutil.cpu_count(logical=True),
                "frequency_current": round(cpu_freq.current, 2) if cpu_freq else None,
                "frequency_max": round(cpu_freq.max, 2) if cpu_freq else None,
                "frequency_min": round(cpu_freq.min, 2) if cpu_freq else None,
                "cpu_percent": round(cpu_percent, 2),
                "temperature": round(temperature, 2) if temperature else None,
                "processor_id": processor_id,
                "status": CPUScanner._get_status(cpu_percent, temperature)
            }
            
            return cpu_info
            
        except Exception as e:
            return {
                "detected": False,
                "model": None,
                "status": f"Error: {str(e)}"
            }
    
    @staticmethod
    def _get_status(cpu_percent: float, temperature: Optional[float]) -> str:
        if cpu_percent > 80:
            return "High Load"
        elif temperature and temperature > 80:
            return "High Temperature"
        elif cpu_percent > 50:
            return "Moderate Load"
        else:
            return "Good"
    
    @staticmethod
    def perform_stress_test(duration: int = 5) -> Dict[str, Any]:
        import time
        import math
        
        start_time = time.time()
        results = []
        
        while time.time() - start_time < duration:
            _ = [math.sqrt(i) for i in range(10000)]
            cpu_usage = psutil.cpu_percent(interval=0.1)
            results.append(cpu_usage)
        
        return {
            "average_usage": round(sum(results) / len(results), 2),
            "max_usage": round(max(results), 2),
            "min_usage": round(min(results), 2),
            "duration_seconds": duration
        }
