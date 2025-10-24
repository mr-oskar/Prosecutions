import psutil
from typing import Dict, Any, List
import os


class DiskScanner:
    @staticmethod
    def get_disks_info() -> List[Dict[str, Any]]:
        disks = []
        
        try:
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    disk_type = DiskScanner._detect_disk_type(partition.device)
                    
                    disk_info = {
                        "detected": True,
                        "device": partition.device,
                        "mount_point": partition.mountpoint,
                        "type": disk_type,
                        "file_system": partition.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "percent_used": round(usage.percent, 2),
                        "serial_number": None,
                        "interface": "SATA",
                        "read_speed_mbps": None,
                        "write_speed_mbps": None,
                        "status": DiskScanner._get_status(usage.percent)
                    }
                    
                    disks.append(disk_info)
                    
                except PermissionError:
                    continue
                except Exception:
                    continue
            
            if not disks:
                disks.append({
                    "detected": False,
                    "device": None,
                    "status": "Not detected"
                })
            
            return disks
            
        except Exception as e:
            return [{
                "detected": False,
                "device": None,
                "status": f"Error: {str(e)}"
            }]
    
    @staticmethod
    def _detect_disk_type(device: str) -> str:
        device_lower = device.lower()
        if 'nvme' in device_lower:
            return "NVMe"
        elif 'ssd' in device_lower:
            return "SSD"
        else:
            return "HDD"
    
    @staticmethod
    def _get_status(percent_used: float) -> str:
        if percent_used > 90:
            return "Critical - Low Space"
        elif percent_used > 75:
            return "Warning - Limited Space"
        elif percent_used > 50:
            return "Moderate"
        else:
            return "Good"
    
    @staticmethod
    def perform_speed_test(mount_point: str = None) -> Dict[str, Any]:
        import time
        import tempfile
        
        try:
            if mount_point is None:
                mount_point = tempfile.gettempdir()
            
            test_file = os.path.join(mount_point, "speed_test.tmp")
            test_size = 10 * 1024 * 1024
            test_data = os.urandom(test_size)
            
            start_write = time.time()
            with open(test_file, 'wb') as f:
                f.write(test_data)
                f.flush()
                os.fsync(f.fileno())
            write_time = time.time() - start_write
            
            start_read = time.time()
            with open(test_file, 'rb') as f:
                _ = f.read()
            read_time = time.time() - start_read
            
            os.remove(test_file)
            
            write_speed = round((test_size / (1024**2)) / write_time, 2)
            read_speed = round((test_size / (1024**2)) / read_time, 2)
            
            return {
                "write_speed_mbps": write_speed,
                "read_speed_mbps": read_speed,
                "test_size_mb": round(test_size / (1024**2), 2)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "write_speed_mbps": None,
                "read_speed_mbps": None
            }
