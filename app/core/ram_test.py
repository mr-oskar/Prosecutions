import psutil
import time
from typing import Dict, Any


class RAMScanner:
    @staticmethod
    def get_ram_info() -> Dict[str, Any]:
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            ram_info = {
                "detected": True,
                "total_gb": round(mem.total / (1024**3), 2),
                "available_gb": round(mem.available / (1024**3), 2),
                "used_gb": round(mem.used / (1024**3), 2),
                "free_gb": round(mem.free / (1024**3), 2),
                "percent_used": round(mem.percent, 2),
                "cached_gb": round(mem.cached / (1024**3), 2) if hasattr(mem, 'cached') else None,
                "buffers_gb": round(mem.buffers / (1024**3), 2) if hasattr(mem, 'buffers') else None,
                "shared_gb": round(mem.shared / (1024**3), 2) if hasattr(mem, 'shared') else None,
                "swap_total_gb": round(swap.total / (1024**3), 2),
                "swap_used_gb": round(swap.used / (1024**3), 2),
                "swap_free_gb": round(swap.free / (1024**3), 2),
                "swap_percent_used": round(swap.percent, 2),
                "speed_mhz": None,
                "type": "Unknown",
                "status": RAMScanner._get_status(mem.percent, swap.percent),
                "health_score": RAMScanner._calculate_health_score(mem.percent, swap.percent)
            }
            
            return ram_info
            
        except Exception as e:
            return {
                "detected": False,
                "total_gb": None,
                "status": f"Error: {str(e)}"
            }
    
    @staticmethod
    def _get_status(percent_used: float, swap_percent: float) -> str:
        if percent_used > 95:
            return "Critical - Memory Full"
        elif percent_used > 90:
            return "Critical - Very High Usage"
        elif percent_used > 80:
            return "Warning - High Usage"
        elif percent_used > 60:
            return "Moderate Usage"
        else:
            return "Good"
    
    @staticmethod
    def _calculate_health_score(mem_percent: float, swap_percent: float) -> int:
        score = 100
        
        if mem_percent > 95:
            score -= 40
        elif mem_percent > 90:
            score -= 30
        elif mem_percent > 80:
            score -= 20
        elif mem_percent > 60:
            score -= 10
        
        if swap_percent > 50:
            score -= 20
        elif swap_percent > 25:
            score -= 10
        
        return max(0, score)
    
    @staticmethod
    def perform_memory_stress_test(duration: int = 5, test_size_mb: int = 100) -> Dict[str, Any]:
        try:
            print(f"Starting RAM stress test for {duration} seconds with {test_size_mb}MB allocation...")
            
            mem_before = psutil.virtual_memory()
            test_size_bytes = test_size_mb * 1024 * 1024
            
            start_time = time.time()
            allocations = []
            usage_samples = []
            
            while time.time() - start_time < duration:
                try:
                    allocations.append(bytearray(test_size_bytes))
                    
                    for i in range(0, test_size_bytes, 1024):
                        allocations[-1][i] = (i % 256)
                    
                    mem_current = psutil.virtual_memory()
                    usage_samples.append(mem_current.percent)
                    
                    time.sleep(0.5)
                    
                except MemoryError:
                    break
            
            allocations.clear()
            
            mem_after = psutil.virtual_memory()
            
            return {
                "test_passed": True,
                "duration_seconds": duration,
                "test_size_mb": test_size_mb,
                "allocations_made": len(usage_samples),
                "memory_before_percent": round(mem_before.percent, 2),
                "memory_after_percent": round(mem_after.percent, 2),
                "average_usage_percent": round(sum(usage_samples) / len(usage_samples), 2) if usage_samples else 0,
                "max_usage_percent": round(max(usage_samples), 2) if usage_samples else 0,
                "memory_allocated_mb": len(usage_samples) * test_size_mb,
                "performance_rating": "Good - Memory allocation successful"
            }
            
        except Exception as e:
            return {
                "test_passed": False,
                "error": str(e),
                "performance_rating": "Failed"
            }
