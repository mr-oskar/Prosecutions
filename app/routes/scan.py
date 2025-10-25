from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.system_scanner import SystemScanner
from app.core.cpu_test import CPUScanner
from app.core.ram_test import RAMScanner
from app.core.disk_test import DiskScanner
from app.core.gpu_test import GPUScanner
from app.core.battery_test import BatteryScanner
from app.core.network_test import NetworkScanner
from app.utils.pdf_generator import PDFGenerator
from app.utils.json_exporter import JSONExporter
from app.utils.database import Database
from typing import Dict, Any, Optional
import uuid
import os


router = APIRouter(prefix="/api/scan", tags=["scan"])
db = Database()


@router.post("/start")
async def start_scan(subscription_code: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    try:
        if device_id is None:
            device_id = str(uuid.uuid4())
        
        verification = db.verify_subscription(subscription_code, device_id)
        
        if not verification.get('valid'):
            raise HTTPException(status_code=403, detail=verification.get('message'))
        
        scanner = SystemScanner()
        scan_result = scanner.perform_full_scan(device_id)
        
        db.increment_scan_count(subscription_code)
        db.save_scan_result(
            scan_id=scan_result['scan_id'],
            subscription_code=subscription_code,
            device_id=device_id,
            scan_data=scan_result
        )
        
        return {
            "success": True,
            "message": "تم الفحص بنجاح / Scan completed successfully",
            "data": scan_result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export-pdf")
async def export_pdf(scan_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        pdf_gen = PDFGenerator()
        pdf_path = pdf_gen.generate_report(scan_data)
        
        return {
            "success": True,
            "message": "تم توليد التقرير PDF بنجاح / PDF report generated successfully",
            "file_path": pdf_path,
            "file_name": os.path.basename(pdf_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export-json")
async def export_json(scan_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        json_exporter = JSONExporter()
        json_path = json_exporter.export_scan_result(scan_data)
        
        return {
            "success": True,
            "message": "تم تصدير البيانات JSON بنجاح / JSON data exported successfully",
            "file_path": json_path,
            "file_name": os.path.basename(json_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{file_type}/{file_name}")
async def download_report(file_type: str, file_name: str):
    try:
        if ".." in file_name or "/" in file_name or "\\" in file_name:
            raise HTTPException(status_code=400, detail="Invalid file name")
        
        if file_type == "pdf":
            base_dir = os.path.abspath("reports/pdfs")
            file_path = os.path.join(base_dir, file_name)
        elif file_type == "json":
            base_dir = os.path.abspath("reports/json")
            file_path = os.path.join(base_dir, file_name)
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        file_path = os.path.abspath(file_path)
        
        if not file_path.startswith(base_dir):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=file_name,
            media_type='application/octet-stream'
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/cpu-stress")
async def test_cpu_stress(duration: int = 5) -> Dict[str, Any]:
    try:
        if duration < 1 or duration > 60:
            raise HTTPException(status_code=400, detail="Duration must be between 1 and 60 seconds")
        
        result = CPUScanner.perform_stress_test(duration)
        
        return {
            "success": True,
            "message": "اختبار الضغط على المعالج اكتمل / CPU stress test completed",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/ram-stress")
async def test_ram_stress(duration: int = 5, test_size_mb: int = 100) -> Dict[str, Any]:
    try:
        if duration < 1 or duration > 60:
            raise HTTPException(status_code=400, detail="Duration must be between 1 and 60 seconds")
        
        if test_size_mb < 10 or test_size_mb > 1000:
            raise HTTPException(status_code=400, detail="Test size must be between 10 and 1000 MB")
        
        result = RAMScanner.perform_memory_stress_test(duration, test_size_mb)
        
        return {
            "success": True,
            "message": "اختبار الذاكرة العشوائية اكتمل / RAM stress test completed",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/disk-speed")
async def test_disk_speed(mount_point: Optional[str] = None, test_size_mb: int = 50) -> Dict[str, Any]:
    try:
        if test_size_mb < 10 or test_size_mb > 500:
            raise HTTPException(status_code=400, detail="Test size must be between 10 and 500 MB")
        
        result = DiskScanner.perform_speed_test(mount_point, test_size_mb)
        
        return {
            "success": True,
            "message": "اختبار سرعة القرص اكتمل / Disk speed test completed",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/gpu-stress")
async def test_gpu_stress(duration: int = 10, gpu_id: int = 0) -> Dict[str, Any]:
    try:
        if duration < 1 or duration > 60:
            raise HTTPException(status_code=400, detail="Duration must be between 1 and 60 seconds")
        
        result = GPUScanner.perform_gpu_stress_test(duration, gpu_id)
        
        return {
            "success": True,
            "message": "اختبار كرت الشاشة اكتمل / GPU stress test completed",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/battery-drain")
async def test_battery_drain(duration: int = 30) -> Dict[str, Any]:
    try:
        if duration < 10 or duration > 300:
            raise HTTPException(status_code=400, detail="Duration must be between 10 and 300 seconds")
        
        result = BatteryScanner.perform_battery_drain_test(duration)
        
        return {
            "success": True,
            "message": "اختبار استهلاك البطارية اكتمل / Battery drain test completed",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/internet-speed")
async def test_internet_speed() -> Dict[str, Any]:
    try:
        result = NetworkScanner.test_internet_speed()
        
        return {
            "success": True,
            "message": "اختبار سرعة الإنترنت اكتمل / Internet speed test completed",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/network-ping")
async def test_network_ping(host: str = "8.8.8.8", count: int = 20) -> Dict[str, Any]:
    try:
        if count < 5 or count > 100:
            raise HTTPException(status_code=400, detail="Count must be between 5 and 100")
        
        result = NetworkScanner.perform_advanced_ping_test(host, count)
        
        return {
            "success": True,
            "message": "اختبار الاتصال بالشبكة اكتمل / Network ping test completed",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
