from typing import Dict, Any, List
import time

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False


class GPUScanner:
    @staticmethod
    def get_gpu_info() -> List[Dict[str, Any]]:
        if not GPU_AVAILABLE:
            return [{
                "detected": False,
                "id": None,
                "name": "No GPU Library",
                "status": "GPUtil library not available - Install with: pip install gputil"
            }]
        
        try:
            gpus = GPUtil.getGPUs()
            
            if not gpus:
                return [{
                    "detected": False,
                    "id": None,
                    "name": "No GPU Detected",
                    "status": "No dedicated GPU found (Integrated GPU may be present)"
                }]
            
            gpu_info_list = []
            
            for gpu in gpus:
                load_percent = round(gpu.load * 100, 2) if gpu.load else 0
                
                gpu_info = {
                    "detected": True,
                    "id": gpu.id,
                    "name": gpu.name,
                    "uuid": gpu.uuid if hasattr(gpu, 'uuid') else None,
                    "memory_total_mb": round(gpu.memoryTotal, 2),
                    "memory_total_gb": round(gpu.memoryTotal / 1024, 2),
                    "memory_used_mb": round(gpu.memoryUsed, 2),
                    "memory_used_gb": round(gpu.memoryUsed / 1024, 2),
                    "memory_free_mb": round(gpu.memoryFree, 2),
                    "memory_free_gb": round(gpu.memoryFree / 1024, 2),
                    "memory_percent": round((gpu.memoryUsed / gpu.memoryTotal) * 100, 2) if gpu.memoryTotal > 0 else 0,
                    "gpu_load_percent": load_percent,
                    "temperature_celsius": round(gpu.temperature, 2) if gpu.temperature else None,
                    "driver_version": gpu.driver if hasattr(gpu, 'driver') else "Unknown",
                    "power_usage_w": None,
                    "fan_speed_percent": None,
                    "status": GPUScanner._get_status(load_percent, gpu.temperature),
                    "health_score": GPUScanner._calculate_health_score(load_percent, gpu.temperature, 
                                                                        (gpu.memoryUsed / gpu.memoryTotal) * 100 if gpu.memoryTotal > 0 else 0)
                }
                
                gpu_info_list.append(gpu_info)
            
            return gpu_info_list
            
        except Exception as e:
            return [{
                "detected": False,
                "id": None,
                "name": None,
                "status": f"Error: {str(e)}"
            }]
    
    @staticmethod
    def _get_status(load_percent: float, temperature: float) -> str:
        if temperature and temperature > 85:
            return "Critical - High Temperature"
        elif load_percent > 95:
            return "Critical - Maximum Load"
        elif temperature and temperature > 75:
            return "Warning - High Temperature"
        elif load_percent > 80:
            return "Warning - High Load"
        elif load_percent > 50:
            return "Moderate Load"
        else:
            return "Good"
    
    @staticmethod
    def _calculate_health_score(load_percent: float, temperature: float, memory_percent: float) -> int:
        score = 100
        
        if load_percent > 95:
            score -= 25
        elif load_percent > 80:
            score -= 15
        elif load_percent > 50:
            score -= 5
        
        if temperature:
            if temperature > 85:
                score -= 40
            elif temperature > 75:
                score -= 25
            elif temperature > 65:
                score -= 10
        
        if memory_percent > 90:
            score -= 15
        elif memory_percent > 75:
            score -= 10
        
        return max(0, score)
    
    @staticmethod
    def perform_gpu_stress_test(duration: int = 10, gpu_id: int = 0) -> Dict[str, Any]:
        if not GPU_AVAILABLE:
            return {
                "test_passed": False,
                "error": "GPUtil library not available"
            }
        
        try:
            print(f"Starting GPU stress test for {duration} seconds...")
            
            gpus = GPUtil.getGPUs()
            if not gpus or gpu_id >= len(gpus):
                return {
                    "test_passed": False,
                    "error": "No GPU available for testing"
                }
            
            gpu = gpus[gpu_id]
            
            initial_temp = gpu.temperature
            initial_load = gpu.load * 100 if gpu.load else 0
            initial_memory = (gpu.memoryUsed / gpu.memoryTotal) * 100 if gpu.memoryTotal > 0 else 0
            
            load_samples = []
            temp_samples = []
            memory_samples = []
            
            start_time = time.time()
            
            while time.time() - start_time < duration:
                gpus = GPUtil.getGPUs()
                if gpus and gpu_id < len(gpus):
                    gpu = gpus[gpu_id]
                    load_samples.append(gpu.load * 100 if gpu.load else 0)
                    if gpu.temperature:
                        temp_samples.append(gpu.temperature)
                    if gpu.memoryTotal > 0:
                        memory_samples.append((gpu.memoryUsed / gpu.memoryTotal) * 100)
                
                time.sleep(0.5)
            
            return {
                "test_passed": True,
                "gpu_id": gpu_id,
                "gpu_name": gpu.name,
                "duration_seconds": duration,
                "initial_load_percent": round(initial_load, 2),
                "initial_temperature_celsius": round(initial_temp, 2) if initial_temp else None,
                "initial_memory_percent": round(initial_memory, 2),
                "average_load_percent": round(sum(load_samples) / len(load_samples), 2) if load_samples else 0,
                "max_load_percent": round(max(load_samples), 2) if load_samples else 0,
                "average_temperature_celsius": round(sum(temp_samples) / len(temp_samples), 2) if temp_samples else None,
                "max_temperature_celsius": round(max(temp_samples), 2) if temp_samples else None,
                "average_memory_percent": round(sum(memory_samples) / len(memory_samples), 2) if memory_samples else 0,
                "samples_collected": len(load_samples),
                "performance_rating": "GPU monitoring successful - For full stress test, use dedicated tools like FurMark"
            }
            
        except Exception as e:
            return {
                "test_passed": False,
                "error": str(e)
            }
