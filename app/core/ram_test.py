import psutil
from typing import Dict, Any


class RAMScanner:
    @staticmethod
    def get_ram_info() -> Dict[str, Any]:
        try:
            mem = psutil.virtual_memory()
            
            ram_info = {
                "detected": True,
                "total_gb": round(mem.total / (1024**3), 2),
                "available_gb": round(mem.available / (1024**3), 2),
                "used_gb": round(mem.used / (1024**3), 2),
                "percent_used": round(mem.percent, 2),
                "speed_mhz": None,
                "type": "DDR4",
                "status": RAMScanner._get_status(mem.percent)
            }
            
            return ram_info
            
        except Exception as e:
            return {
                "detected": False,
                "total_gb": None,
                "status": f"Error: {str(e)}"
            }
    
    @staticmethod
    def _get_status(percent_used: float) -> str:
        if percent_used > 90:
            return "Critical"
        elif percent_used > 75:
            return "High Usage"
        elif percent_used > 50:
            return "Moderate"
        else:
            return "Good"
    
    @staticmethod
    def perform_read_write_test() -> Dict[str, Any]:
        import time
        
        test_size = 100 * 1024 * 1024
        test_data = bytearray(test_size)
        
        start_write = time.time()
        for i in range(0, test_size, 1024):
            test_data[i] = i % 256
        write_time = time.time() - start_write
        
        start_read = time.time()
        total = 0
        for i in range(0, test_size, 1024):
            total += test_data[i]
        read_time = time.time() - start_read
        
        write_speed_mbps = round((test_size / (1024**2)) / write_time, 2)
        read_speed_mbps = round((test_size / (1024**2)) / read_time, 2)
        
        return {
            "write_speed_mbps": write_speed_mbps,
            "read_speed_mbps": read_speed_mbps,
            "test_size_mb": round(test_size / (1024**2), 2)
        }
