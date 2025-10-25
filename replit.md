# System Guardian - Professional PC Diagnostic Tool

## Overview
System Guardian is a comprehensive PC diagnostic application with subscription-based access control. It provides detailed hardware scanning, performance testing, and generates professional PDF and JSON reports.

## Project Structure
```
/SystemGuardian
├── app/                 # FastAPI backend
│   ├── main.py          # FastAPI server entry point
│   ├── routes/          # API endpoints
│   │   ├── scan.py      # Scanning operations
│   │   └── subscription.py  # Subscription management
│   ├── core/            # Hardware scanning modules
│   │   ├── cpu_test.py
│   │   ├── ram_test.py
│   │   ├── disk_test.py
│   │   ├── gpu_test.py
│   │   ├── battery_test.py
│   │   ├── network_test.py
│   │   ├── peripherals_test.py
│   │   └── system_scanner.py
│   ├── models/          # Pydantic data models
│   └── utils/           # Helper utilities (PDF, JSON, Database)
├── ui/                  # Flask web interface
│   ├── app.py           # Flask application
│   ├── templates/       # HTML templates
│   └── static/          # CSS and JavaScript
├── db/                  # SQLite database
├── reports/             # Generated reports
│   ├── pdfs/            # PDF reports
│   └── json/            # JSON exports
└── .gitignore
```

## Features
- ✅ Comprehensive hardware scanning (CPU, RAM, Disk, GPU, Battery, Network, Peripherals)
- ✅ Subscription-based access control with expiration dates
- ✅ Professional PDF reports with color-coded status indicators
- ✅ JSON data export for raw scan results
- ✅ Dark mode web interface with Bootstrap 5
- ✅ RESTful API with FastAPI
- ✅ SQLite database for subscription management
- ✅ Real-time scan progress and results display

## Technology Stack
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Flask + Bootstrap 5 + JavaScript
- **Database**: SQLite3
- **Hardware Scanning**: psutil, GPUtil
- **Reports**: ReportLab (PDF), JSON
- **Network Testing**: speedtest-cli

## Setup & Running
1. FastAPI backend runs on port 8000
2. Flask web interface runs on port 5000
3. Access the web interface at http://localhost:5000

## API Endpoints
### Subscription Management
- POST `/api/subscription/create` - Create new subscription
- POST `/api/subscription/verify` - Verify subscription code
- POST `/api/subscription/renew/{code}` - Renew subscription
- GET `/api/subscription/list` - List all subscriptions

### Scanning
- POST `/api/scan/start` - Start system scan
- POST `/api/scan/export-pdf` - Generate PDF report
- POST `/api/scan/export-json` - Export JSON data

## Recent Changes
- 2025-10-25: **MAJOR UPDATE** - Enhanced all hardware scanners with detailed telemetry
- 2025-10-25: Added 7 working stress test API endpoints for comprehensive testing
- 2025-10-25: Fixed critical path traversal security vulnerability in download endpoint
- 2025-10-25: Created complete VS Code setup with configuration files and scripts
- 2025-10-25: Added API_TESTS.md with comprehensive testing documentation
- 2025-10-24: Initial project setup with full hardware scanning capability
- 2025-10-24: Implemented subscription management system
- 2025-10-24: Created Flask web interface with dark mode
- 2025-10-24: Added PDF and JSON report generation

## User Preferences
- Dark mode interface preferred
- Professional color-coded status indicators (Green/Yellow/Red)
- Bilingual support (Arabic/English)

## Important Notes

### Security Notice ⚠️
**This MVP version does NOT have authentication on the admin panel.** 
- Admin panel at `/admin` is accessible without login
- Subscription management endpoints are unprotected
- Suitable for: Development, Testing, Local Use Only
- NOT suitable for: Public deployment without adding authentication
- See `SECURITY.md` for production deployment guidelines

### Known Limitations
- Docker support planned for future phases
- Advanced stress tests and IOPS testing planned for next phase
- Network speed test may take 30-60 seconds to complete
- Some features work best on Windows (battery detection, GPU detection)
- Admin authentication system planned for v2.0

### Files to Review
- `README.md` - Project overview and quick start
- `SECURITY.md` - Security considerations and recommendations
- `USAGE.md` - Detailed user guide and troubleshooting
