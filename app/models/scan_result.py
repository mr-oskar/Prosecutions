from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class CPUInfo(BaseModel):
    detected: bool = True
    model: Optional[str] = None
    cores_physical: Optional[int] = None
    cores_logical: Optional[int] = None
    frequency_current: Optional[float] = None
    frequency_max: Optional[float] = None
    frequency_min: Optional[float] = None
    cpu_percent: Optional[float] = None
    temperature: Optional[float] = None
    processor_id: Optional[str] = None
    status: str = "Unknown"


class RAMInfo(BaseModel):
    detected: bool = True
    total_gb: Optional[float] = None
    available_gb: Optional[float] = None
    used_gb: Optional[float] = None
    percent_used: Optional[float] = None
    speed_mhz: Optional[int] = None
    type: Optional[str] = None
    status: str = "Unknown"


class DiskInfo(BaseModel):
    detected: bool = True
    device: Optional[str] = None
    mount_point: Optional[str] = None
    type: Optional[str] = None
    file_system: Optional[str] = None
    total_gb: Optional[float] = None
    used_gb: Optional[float] = None
    free_gb: Optional[float] = None
    percent_used: Optional[float] = None
    serial_number: Optional[str] = None
    interface: Optional[str] = None
    read_speed_mbps: Optional[float] = None
    write_speed_mbps: Optional[float] = None
    status: str = "Unknown"


class GPUInfo(BaseModel):
    detected: bool = False
    id: Optional[int] = None
    name: Optional[str] = None
    memory_total_mb: Optional[float] = None
    memory_used_mb: Optional[float] = None
    memory_free_mb: Optional[float] = None
    memory_percent: Optional[float] = None
    temperature: Optional[float] = None
    driver_version: Optional[str] = None
    power_usage_w: Optional[float] = None
    status: str = "Not detected"


class BatteryInfo(BaseModel):
    detected: bool = False
    percent: Optional[float] = None
    power_plugged: Optional[bool] = None
    time_left_seconds: Optional[int] = None
    capacity_max_wh: Optional[float] = None
    capacity_current_wh: Optional[float] = None
    health_percent: Optional[float] = None
    status: str = "Not detected"


class NetworkInfo(BaseModel):
    detected: bool = True
    interface_name: Optional[str] = None
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    download_speed_mbps: Optional[float] = None
    upload_speed_mbps: Optional[float] = None
    ping_ms: Optional[float] = None
    connection_stable: Optional[bool] = None
    status: str = "Unknown"


class PeripheralsInfo(BaseModel):
    keyboard_detected: bool = False
    mouse_detected: bool = False
    display_detected: bool = False
    audio_devices: List[str] = []
    usb_devices: List[str] = []
    printers: List[str] = []
    total_devices: int = 0


class ScanResult(BaseModel):
    scan_id: str
    timestamp: datetime
    device_id: Optional[str] = None
    cpu: CPUInfo
    ram: RAMInfo
    disks: List[DiskInfo]
    gpu: List[GPUInfo]
    battery: BatteryInfo
    network: NetworkInfo
    peripherals: PeripheralsInfo
    overall_health: str = "Unknown"
    recommendations: List[str] = []
