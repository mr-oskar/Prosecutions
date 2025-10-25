import psutil
import platform
import time
import math
import multiprocessing
from typing import Dict, Any, Optional, List


class CPUScanner:
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        try:
            cpu_freq = psutil.cpu_freq()
            cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
            cpu_percent_per_core = psutil.cpu_percent(interval=0.5, percpu=True)
            
            temps = None
            try:
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
            except:
                pass
            
            temperature = None
            temp_sensors = []
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        temp_sensors.append({
                            "label": entry.label if entry.label else name,
                            "current": round(entry.current, 2),
                            "high": round(entry.high, 2) if entry.high else None,
                            "critical": round(entry.critical, 2) if entry.critical else None
                        })
                        if temperature is None:
                            temperature = entry.current
            
            processor_id = platform.processor()
            
            cpu_stats = psutil.cpu_stats()
            cpu_times = psutil.cpu_times()
            
            cpu_info = {
                "detected": True,
                "model": processor_id if processor_id else "Unknown CPU",
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "cores_physical": psutil.cpu_count(logical=False),
                "cores_logical": psutil.cpu_count(logical=True),
                "frequency_current_mhz": round(cpu_freq.current, 2) if cpu_freq else None,
                "frequency_max_mhz": round(cpu_freq.max, 2) if cpu_freq else None,
                "frequency_min_mhz": round(cpu_freq.min, 2) if cpu_freq else None,
                "cpu_percent_overall": round(cpu_percent, 2),
                "cpu_percent_per_core": [round(p, 2) for p in cpu_percent_per_core],
                "temperature_celsius": round(temperature, 2) if temperature else None,
                "temperature_sensors": temp_sensors,
                "processor_id": processor_id,
                "context_switches": cpu_stats.ctx_switches,
                "interrupts": cpu_stats.interrupts,
                "soft_interrupts": cpu_stats.soft_interrupts,
                "system_calls": cpu_stats.syscalls,
                "cpu_times": {
                    "user": round(cpu_times.user, 2),
                    "system": round(cpu_times.system, 2),
                    "idle": round(cpu_times.idle, 2)
                },
                "status": CPUScanner._get_status(cpu_percent, temperature),
                "health_score": CPUScanner._calculate_health_score(cpu_percent, temperature)
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
        if temperature and temperature > 85:
            return "Critical - High Temperature"
        elif cpu_percent > 90:
            return "Critical - Very High Load"
        elif temperature and temperature > 75:
            return "Warning - High Temperature"
        elif cpu_percent > 80:
            return "Warning - High Load"
        elif cpu_percent > 50:
            return "Moderate Load"
        else:
            return "Good"
    
    @staticmethod
    def _calculate_health_score(cpu_percent: float, temperature: Optional[float]) -> int:
        score = 100
        
        if cpu_percent > 90:
            score -= 30
        elif cpu_percent > 80:
            score -= 20
        elif cpu_percent > 50:
            score -= 10
        
        if temperature:
            if temperature > 85:
                score -= 40
            elif temperature > 75:
                score -= 25
            elif temperature > 65:
                score -= 15
        
        return max(0, score)
    
    @staticmethod
    def perform_stress_test(duration: int = 5) -> Dict[str, Any]:
        start_time = time.time()
        results = []
        temp_results = []
        
        def cpu_intensive_task():
            end = time.time() + duration
            while time.time() < end:
                _ = [math.sqrt(i) * math.sin(i) for i in range(10000)]
        
        num_processes = multiprocessing.cpu_count()
        processes = []
        
        print(f"Starting CPU stress test with {num_processes} processes for {duration} seconds...")
        
        for _ in range(num_processes):
            p = multiprocessing.Process(target=cpu_intensive_task)
            p.start()
            processes.append(p)
        
        while time.time() - start_time < duration:
            cpu_usage = psutil.cpu_percent(interval=0.1)
            results.append(cpu_usage)
            
            try:
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
                    if temps:
                        for name, entries in temps.items():
                            if entries:
                                temp_results.append(entries[0].current)
                                break
            except:
                pass
            
            time.sleep(0.1)
        
        for p in processes:
            p.terminate()
            p.join()
        
        avg_temp = round(sum(temp_results) / len(temp_results), 2) if temp_results else None
        max_temp = round(max(temp_results), 2) if temp_results else None
        
        return {
            "test_passed": True,
            "duration_seconds": duration,
            "average_usage_percent": round(sum(results) / len(results), 2) if results else 0,
            "max_usage_percent": round(max(results), 2) if results else 0,
            "min_usage_percent": round(min(results), 2) if results else 0,
            "average_temperature_celsius": avg_temp,
            "max_temperature_celsius": max_temp,
            "processes_used": num_processes,
            "samples_collected": len(results),
            "performance_rating": CPUScanner._get_performance_rating(
                round(sum(results) / len(results), 2) if results else 0
            )
        }
    
    @staticmethod
    def _get_performance_rating(avg_usage: float) -> str:
        if avg_usage > 90:
            return "Excellent - CPU can reach full capacity"
        elif avg_usage > 70:
            return "Good - CPU performs well under load"
        elif avg_usage > 50:
            return "Fair - CPU has some limitations"
        else:
            return "Poor - CPU may have thermal throttling or issues"
