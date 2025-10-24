from fastapi import APIRouter, HTTPException
from app.core.system_scanner import SystemScanner
from app.utils.pdf_generator import PDFGenerator
from app.utils.json_exporter import JSONExporter
from app.utils.database import Database
from typing import Dict, Any
import uuid

router = APIRouter(prefix="/api/scan", tags=["scan"])
db = Database()


@router.post("/start")
async def start_scan(subscription_code: str, device_id: str = None) -> Dict[str, Any]:
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
            "file_path": pdf_path
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
            "file_path": json_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
