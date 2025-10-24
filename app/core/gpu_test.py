from typing import Dict, Any, List

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
                "name": None,
                "status": "GPUtil library not available"
            }]
        
        try:
            gpus = GPUtil.getGPUs()
            
            if not gpus:
                return [{
                    "detected": False,
                    "id": None,
                    "name": None,
                    "status": "No GPU detected"
                }]
            
            gpu_info_list = []
            
            for gpu in gpus:
                gpu_info = {
                    "detected": True,
                    "id": gpu.id,
                    "name": gpu.name,
                    "memory_total_mb": round(gpu.memoryTotal, 2),
                    "memory_used_mb": round(gpu.memoryUsed, 2),
                    "memory_free_mb": round(gpu.memoryFree, 2),
                    "memory_percent": round((gpu.memoryUsed / gpu.memoryTotal) * 100, 2) if gpu.memoryTotal > 0 else 0,
                    "temperature": round(gpu.temperature, 2) if gpu.temperature else None,
                    "driver_version": gpu.driver if hasattr(gpu, 'driver') else "Unknown",
                    "power_usage_w": None,
                    "status": GPUScanner._get_status(gpu.load * 100 if gpu.load else 0, gpu.temperature)
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
        if load_percent > 90:
            return "High Load"
        elif temperature and temperature > 80:
            return "High Temperature"
        elif load_percent > 50:
            return "Moderate Load"
        else:
            return "Good"
