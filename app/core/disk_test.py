import psutil
import os
import time
import tempfile
import platform
from typing import Dict, Any, List, Optional


class DiskScanner:
    @staticmethod
    def get_disks_info() -> List[Dict[str, Any]]:
        disks = []
        
        try:
            partitions = psutil.disk_partitions()
            io_counters = psutil.disk_io_counters(perdisk=True) if hasattr(psutil, 'disk_io_counters') else {}
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    disk_type = DiskScanner._detect_disk_type(partition.device)
                    
                    device_name = partition.device.split('/')[-1] if '/' in partition.device else partition.device
                    
                    io_stats = None
                    if io_counters:
                        for disk_name, counters in io_counters.items():
                            if device_name in disk_name or disk_name in device_name:
                                io_stats = {
                                    "read_count": counters.read_count,
                                    "write_count": counters.write_count,
                                    "read_bytes": round(counters.read_bytes / (1024**3), 2),
                                    "write_bytes": round(counters.write_bytes / (1024**3), 2),
                                    "read_time_ms": counters.read_time,
                                    "write_time_ms": counters.write_time
                                }
                                break
                    
                    disk_info = {
                        "detected": True,
                        "device": partition.device,
                        "device_name": device_name,
                        "mount_point": partition.mountpoint,
                        "type": disk_type,
                        "file_system": partition.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "percent_used": round(usage.percent, 2),
                        "serial_number": None,
                        "interface": DiskScanner._get_interface(disk_type),
                        "io_stats": io_stats,
                        "read_speed_mbps": None,
                        "write_speed_mbps": None,
                        "status": DiskScanner._get_status(usage.percent),
                        "health_score": DiskScanner._calculate_health_score(usage.percent)
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
            return "NVMe SSD"
        elif 'ssd' in device_lower:
            return "SATA SSD"
        elif 'mmc' in device_lower or 'sd' in device_lower:
            return "SD/MMC"
        else:
            try:
                if platform.system() == 'Linux':
                    device_name = device.split('/')[-1]
                    rotational_file = f'/sys/block/{device_name}/queue/rotational'
                    if os.path.exists(rotational_file):
                        with open(rotational_file, 'r') as f:
                            if f.read().strip() == '0':
                                return "SSD"
                            else:
                                return "HDD"
            except:
                pass
            
            return "HDD"
    
    @staticmethod
    def _get_interface(disk_type: str) -> str:
        if 'NVMe' in disk_type:
            return "PCIe NVMe"
        elif 'SSD' in disk_type:
            return "SATA"
        elif 'SD' in disk_type or 'MMC' in disk_type:
            return "SD/MMC"
        else:
            return "SATA"
    
    @staticmethod
    def _get_status(percent_used: float) -> str:
        if percent_used > 95:
            return "Critical - Nearly Full"
        elif percent_used > 90:
            return "Critical - Low Space"
        elif percent_used > 75:
            return "Warning - Limited Space"
        elif percent_used > 50:
            return "Moderate"
        else:
            return "Good"
    
    @staticmethod
    def _calculate_health_score(percent_used: float) -> int:
        score = 100
        
        if percent_used > 95:
            score -= 50
        elif percent_used > 90:
            score -= 40
        elif percent_used > 75:
            score -= 25
        elif percent_used > 50:
            score -= 10
        
        return max(0, score)
    
    @staticmethod
    def perform_speed_test(mount_point: Optional[str] = None, test_size_mb: int = 50) -> Dict[str, Any]:
        try:
            if mount_point is None:
                mount_point = tempfile.gettempdir()
            
            print(f"Starting disk speed test on {mount_point} with {test_size_mb}MB test file...")
            
            test_file = os.path.join(mount_point, "disk_speed_test.tmp")
            test_size = test_size_mb * 1024 * 1024
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
            
            try:
                os.remove(test_file)
            except:
                pass
            
            write_speed = round((test_size / (1024**2)) / write_time, 2)
            read_speed = round((test_size / (1024**2)) / read_time, 2)
            
            disk_type = DiskScanner._determine_disk_type_by_speed(write_speed, read_speed)
            
            return {
                "test_passed": True,
                "mount_point": mount_point,
                "test_size_mb": test_size_mb,
                "write_speed_mbps": write_speed,
                "read_speed_mbps": read_speed,
                "write_time_seconds": round(write_time, 2),
                "read_time_seconds": round(read_time, 2),
                "estimated_disk_type": disk_type,
                "performance_rating": DiskScanner._get_performance_rating(write_speed, read_speed)
            }
            
        except Exception as e:
            return {
                "test_passed": False,
                "error": str(e),
                "write_speed_mbps": None,
                "read_speed_mbps": None
            }
    
    @staticmethod
    def _determine_disk_type_by_speed(write_speed: float, read_speed: float) -> str:
        avg_speed = (write_speed + read_speed) / 2
        
        if avg_speed > 1000:
            return "NVMe SSD"
        elif avg_speed > 300:
            return "SATA SSD"
        elif avg_speed > 100:
            return "Fast HDD/Hybrid"
        else:
            return "HDD"
    
    @staticmethod
    def _get_performance_rating(write_speed: float, read_speed: float) -> str:
        avg_speed = (write_speed + read_speed) / 2
        
        if avg_speed > 1500:
            return "Excellent - High-end NVMe SSD"
        elif avg_speed > 800:
            return "Very Good - NVMe SSD"
        elif avg_speed > 400:
            return "Good - SATA SSD"
        elif avg_speed > 150:
            return "Fair - Entry-level SSD or Fast HDD"
        elif avg_speed > 80:
            return "Moderate - Standard HDD"
        else:
            return "Poor - Slow drive or heavy system load"
