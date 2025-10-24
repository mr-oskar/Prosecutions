from datetime import datetime
import uuid
from typing import Dict, Any, List
from .cpu_test import CPUScanner
from .ram_test import RAMScanner
from .disk_test import DiskScanner
from .gpu_test import GPUScanner
from .battery_test import BatteryScanner
from .network_test import NetworkScanner
from .peripherals_test import PeripheralsScanner


class SystemScanner:
    def __init__(self):
        self.cpu_scanner = CPUScanner()
        self.ram_scanner = RAMScanner()
        self.disk_scanner = DiskScanner()
        self.gpu_scanner = GPUScanner()
        self.battery_scanner = BatteryScanner()
        self.network_scanner = NetworkScanner()
        self.peripherals_scanner = PeripheralsScanner()
    
    def perform_full_scan(self, device_id: str = None) -> Dict[str, Any]:
        if device_id is None:
            device_id = str(uuid.uuid4())
        
        scan_id = f"SCAN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
        
        print("Starting system scan...")
        
        print("Scanning CPU...")
        cpu_info = self.cpu_scanner.get_cpu_info()
        
        print("Scanning RAM...")
        ram_info = self.ram_scanner.get_ram_info()
        
        print("Scanning Disks...")
        disks_info = self.disk_scanner.get_disks_info()
        
        print("Scanning GPU...")
        gpu_info = self.gpu_scanner.get_gpu_info()
        
        print("Scanning Battery...")
        battery_info = self.battery_scanner.get_battery_info()
        
        print("Scanning Network...")
        network_info = self.network_scanner.get_network_info()
        
        print("Scanning Peripherals...")
        peripherals_info = self.peripherals_scanner.get_peripherals_info()
        
        overall_health, recommendations = self._analyze_system_health(
            cpu_info, ram_info, disks_info, gpu_info, battery_info, network_info
        )
        
        scan_result = {
            "scan_id": scan_id,
            "timestamp": datetime.now().isoformat(),
            "device_id": device_id,
            "cpu": cpu_info,
            "ram": ram_info,
            "disks": disks_info,
            "gpu": gpu_info,
            "battery": battery_info,
            "network": network_info,
            "peripherals": peripherals_info,
            "overall_health": overall_health,
            "recommendations": recommendations
        }
        
        print("Scan completed successfully!")
        
        return scan_result
    
    def _analyze_system_health(
        self, cpu: Dict, ram: Dict, disks: List[Dict], 
        gpu: List[Dict], battery: Dict, network: Dict
    ) -> tuple:
        issues = []
        recommendations = []
        
        if cpu.get('cpu_percent', 0) > 80:
            issues.append("high_cpu")
            recommendations.append("وحدة المعالجة المركزية تحت ضغط عالٍ - High CPU usage detected")
        
        if cpu.get('temperature') and cpu['temperature'] > 80:
            issues.append("high_cpu_temp")
            recommendations.append("درجة حرارة المعالج مرتفعة - CPU temperature is high")
        
        if ram.get('percent_used', 0) > 90:
            issues.append("critical_ram")
            recommendations.append("الذاكرة العشوائية ممتلئة تقريباً - RAM usage critical")
        elif ram.get('percent_used', 0) > 75:
            issues.append("high_ram")
            recommendations.append("استخدام عالٍ للذاكرة العشوائية - High RAM usage")
        
        for disk in disks:
            if disk.get('percent_used', 0) > 90:
                issues.append("critical_disk")
                recommendations.append(f"مساحة القرص {disk.get('device')} شبه ممتلئة - Disk space critical")
        
        if battery.get('detected') and battery.get('health_percent', 100) < 70:
            issues.append("battery_health")
            recommendations.append("صحة البطارية منخفضة - Battery health degraded")
        
        if network.get('ping_ms') and network['ping_ms'] > 200:
            issues.append("poor_network")
            recommendations.append("جودة الاتصال بالإنترنت ضعيفة - Poor network connection")
        
        if not recommendations:
            recommendations.append("النظام يعمل بشكل جيد - System is running well")
        
        if len(issues) == 0:
            overall_health = "Excellent"
        elif len(issues) <= 2:
            overall_health = "Good"
        elif len(issues) <= 4:
            overall_health = "Fair"
        else:
            overall_health = "Poor"
        
        return overall_health, recommendations
