import json
import os
from datetime import datetime
from typing import Dict, Any


class JSONExporter:
    @staticmethod
    def export_scan_result(scan_data: Dict[str, Any], output_dir: str = "reports/json") -> str:
        os.makedirs(output_dir, exist_ok=True)
        
        scan_id = scan_data.get('scan_id', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"scan_{scan_id}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scan_data, f, indent=2, ensure_ascii=False)
        
        return filepath
