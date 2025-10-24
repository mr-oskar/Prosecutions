from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from typing import Dict, Any, List
import os


class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate_report(self, scan_data: Dict[str, Any], output_dir: str = "reports/pdfs") -> str:
        os.makedirs(output_dir, exist_ok=True)
        
        scan_id = scan_data.get('scan_id', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{scan_id}_{timestamp}.pdf"
        filepath = os.path.join(output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        title = Paragraph("System Guardian - PC Diagnostic Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        info_data = [
            ['Scan ID:', scan_data.get('scan_id', 'N/A')],
            ['Date:', datetime.fromisoformat(scan_data.get('timestamp', datetime.now().isoformat())).strftime('%Y-%m-%d %H:%M:%S')],
            ['Device ID:', scan_data.get('device_id', 'N/A')],
            ['Overall Health:', scan_data.get('overall_health', 'Unknown')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        cpu = scan_data.get('cpu', {})
        story.append(Paragraph("CPU Information", self.styles['SectionHeader']))
        cpu_data = self._create_cpu_table(cpu)
        story.append(cpu_data)
        story.append(Spacer(1, 0.2*inch))
        
        ram = scan_data.get('ram', {})
        story.append(Paragraph("RAM Information", self.styles['SectionHeader']))
        ram_data = self._create_ram_table(ram)
        story.append(ram_data)
        story.append(Spacer(1, 0.2*inch))
        
        disks = scan_data.get('disks', [])
        story.append(Paragraph("Disk Information", self.styles['SectionHeader']))
        for disk in disks:
            disk_data = self._create_disk_table(disk)
            story.append(disk_data)
            story.append(Spacer(1, 0.1*inch))
        
        gpu_list = scan_data.get('gpu', [])
        story.append(Paragraph("GPU Information", self.styles['SectionHeader']))
        for gpu in gpu_list:
            gpu_data = self._create_gpu_table(gpu)
            story.append(gpu_data)
            story.append(Spacer(1, 0.1*inch))
        
        battery = scan_data.get('battery', {})
        if battery.get('detected'):
            story.append(Paragraph("Battery Information", self.styles['SectionHeader']))
            battery_data = self._create_battery_table(battery)
            story.append(battery_data)
            story.append(Spacer(1, 0.2*inch))
        
        network = scan_data.get('network', {})
        story.append(Paragraph("Network Information", self.styles['SectionHeader']))
        network_data = self._create_network_table(network)
        story.append(network_data)
        story.append(Spacer(1, 0.2*inch))
        
        recommendations = scan_data.get('recommendations', [])
        story.append(Paragraph("Recommendations", self.styles['SectionHeader']))
        rec_data = [[rec] for rec in recommendations]
        rec_table = Table(rec_data, colWidths=[6*inch])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(rec_table)
        
        doc.build(story)
        
        return filepath
    
    def _create_cpu_table(self, cpu: Dict[str, Any]) -> Table:
        status_color = self._get_status_color(cpu.get('status', 'Unknown'))
        
        data = [
            ['Property', 'Value', 'Status'],
            ['Detected', 'Yes' if cpu.get('detected') else 'No', ''],
            ['Model', cpu.get('model', 'N/A'), ''],
            ['Physical Cores', str(cpu.get('cores_physical', 'N/A')), ''],
            ['Logical Cores', str(cpu.get('cores_logical', 'N/A')), ''],
            ['Current Frequency', f"{cpu.get('frequency_current', 'N/A')} MHz", ''],
            ['CPU Usage', f"{cpu.get('cpu_percent', 'N/A')}%", cpu.get('status', 'Unknown')],
            ['Temperature', f"{cpu.get('temperature', 'N/A')} °C" if cpu.get('temperature') else 'N/A', '']
        ]
        
        table = Table(data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (2, -2), (2, -1), status_color),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        return table
    
    def _create_ram_table(self, ram: Dict[str, Any]) -> Table:
        status_color = self._get_status_color(ram.get('status', 'Unknown'))
        
        data = [
            ['Property', 'Value', 'Status'],
            ['Detected', 'Yes' if ram.get('detected') else 'No', ''],
            ['Total', f"{ram.get('total_gb', 'N/A')} GB", ''],
            ['Available', f"{ram.get('available_gb', 'N/A')} GB", ''],
            ['Used', f"{ram.get('used_gb', 'N/A')} GB", ''],
            ['Usage', f"{ram.get('percent_used', 'N/A')}%", ram.get('status', 'Unknown')]
        ]
        
        table = Table(data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (2, -1), (2, -1), status_color),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        return table
    
    def _create_disk_table(self, disk: Dict[str, Any]) -> Table:
        status_color = self._get_status_color(disk.get('status', 'Unknown'))
        
        data = [
            ['Property', 'Value', 'Status'],
            ['Device', disk.get('device', 'N/A'), ''],
            ['Type', disk.get('type', 'N/A'), ''],
            ['File System', disk.get('file_system', 'N/A'), ''],
            ['Total', f"{disk.get('total_gb', 'N/A')} GB", ''],
            ['Used', f"{disk.get('used_gb', 'N/A')} GB", ''],
            ['Free', f"{disk.get('free_gb', 'N/A')} GB", ''],
            ['Usage', f"{disk.get('percent_used', 'N/A')}%", disk.get('status', 'Unknown')]
        ]
        
        table = Table(data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (2, -1), (2, -1), status_color),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        return table
    
    def _create_gpu_table(self, gpu: Dict[str, Any]) -> Table:
        status_color = self._get_status_color(gpu.get('status', 'Unknown'))
        
        data = [
            ['Property', 'Value', 'Status'],
            ['Detected', 'Yes' if gpu.get('detected') else 'No', ''],
            ['Name', gpu.get('name', 'N/A'), ''],
            ['Memory Total', f"{gpu.get('memory_total_mb', 'N/A')} MB" if gpu.get('memory_total_mb') else 'N/A', ''],
            ['Memory Used', f"{gpu.get('memory_used_mb', 'N/A')} MB" if gpu.get('memory_used_mb') else 'N/A', ''],
            ['Temperature', f"{gpu.get('temperature', 'N/A')} °C" if gpu.get('temperature') else 'N/A', gpu.get('status', 'Unknown')]
        ]
        
        table = Table(data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (2, -1), (2, -1), status_color),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        return table
    
    def _create_battery_table(self, battery: Dict[str, Any]) -> Table:
        status_color = self._get_status_color(battery.get('status', 'Unknown'))
        
        data = [
            ['Property', 'Value', 'Status'],
            ['Charge Level', f"{battery.get('percent', 'N/A')}%", ''],
            ['Power Plugged', 'Yes' if battery.get('power_plugged') else 'No', ''],
            ['Health', f"{battery.get('health_percent', 'N/A')}%", battery.get('status', 'Unknown')]
        ]
        
        table = Table(data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (2, -1), (2, -1), status_color),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        return table
    
    def _create_network_table(self, network: Dict[str, Any]) -> Table:
        status_color = self._get_status_color(network.get('status', 'Unknown'))
        
        data = [
            ['Property', 'Value', 'Status'],
            ['Detected', 'Yes' if network.get('detected') else 'No', ''],
            ['Interface', network.get('interface_name', 'N/A'), ''],
            ['IP Address', network.get('ip_address', 'N/A'), ''],
            ['MAC Address', network.get('mac_address', 'N/A'), ''],
            ['Ping', f"{network.get('ping_ms', 'N/A')} ms" if network.get('ping_ms') else 'N/A', network.get('status', 'Unknown')]
        ]
        
        table = Table(data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1abc9c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (2, -1), (2, -1), status_color),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        return table
    
    def _get_status_color(self, status: str) -> colors.Color:
        status_lower = status.lower()
        
        if any(word in status_lower for word in ['good', 'excellent', 'charged', 'charging']):
            return colors.HexColor('#27ae60')
        elif any(word in status_lower for word in ['critical', 'high', 'poor', 'low']):
            return colors.HexColor('#e74c3c')
        elif any(word in status_lower for word in ['moderate', 'fair', 'warning']):
            return colors.HexColor('#f39c12')
        else:
            return colors.HexColor('#95a5a6')
