# System Guardian - Professional PC Diagnostic Tool

<div align="center">

![System Guardian](https://img.shields.io/badge/System-Guardian-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-teal?style=for-the-badge&logo=fastapi)
![Flask](https://img.shields.io/badge/Flask-latest-black?style=for-the-badge&logo=flask)

**تطبيق احترافي متكامل لفحص أجهزة الحاسوب مع نظام اشتراك**

A comprehensive PC diagnostic application with subscription-based access control

</div>

## 📋 Features | المميزات

### Core Features | الميزات الأساسية

#### 🔍 **Enhanced Hardware Scanning** - فحص محسّن للعتاد
- ✅ **CPU** - معالج
  - Model, Architecture, Physical/Logical Cores
  - Frequencies (Current, Min, Max)
  - Temperature sensors (multiple)
  - Usage per core, System calls, Context switches
  - Health score calculation
  
- ✅ **RAM** - ذاكرة عشوائية
  - Total, Available, Used, Free
  - Cache, Buffers, Shared memory
  - Swap memory details
  - Health score and recommendations
  
- ✅ **Disk** - أقراص التخزين
  - Auto-detect type (HDD/SSD/NVMe/SD)
  - I/O Statistics (read/write counts and bytes)
  - Mount points, File systems
  - Health score based on usage
  
- ✅ **GPU** - كرت الشاشة
  - Name, Memory (Total/Used/Free), UUID
  - Load percentage, Temperature
  - Driver version, Health score
  
- ✅ **Battery** - بطارية
  - Charge level, Power status
  - Time remaining (formatted)
  - Health estimation, Cycle count
  
- ✅ **Network** - شبكة
  - All interfaces with IPv4/IPv6
  - MAC addresses, MTU, Speed
  - I/O counters, Error statistics
  - Connection quality assessment
  
- ✅ **Peripherals** - ملحقات
  - USB devices listing
  - Display information
  - Audio devices, Webcams
  - Keyboard & Mouse detection

#### 🧪 **Advanced Stress Tests** - اختبارات متقدمة
- ⚡ **CPU Stress Test**: Multi-core load testing with temperature monitoring
- 💾 **RAM Stress Test**: Memory allocation and read/write performance
- 💿 **Disk Speed Test**: Real read/write speed measurement (MB/s)
- 🎮 **GPU Stress Test**: GPU load and temperature monitoring
- 🔋 **Battery Drain Test**: Power consumption rate analysis
- 🌐 **Internet Speed Test**: Download/upload speed measurement
- 📡 **Network Ping Test**: Latency, jitter, and packet loss analysis

#### 📄 **Professional Reports** - تقارير احترافية
- PDF reports with color-coded health indicators
- JSON exports with complete raw data
- **Direct download** functionality for reports
- Personalized recommendations based on scan results

#### 🔐 **Subscription Management** - إدارة الاشتراكات
- Code-based access control
- Expiration tracking (7, 30, 90, 365 days)
- Device binding for security
- Scan count tracking

#### 🌐 **Modern Web Interface** - واجهة ويب حديثة
- Dark mode design
- Bootstrap 5 responsive layout
- Real-time scan progress
- Admin panel for subscription management

## 🏗️ Architecture | البنية

```
SystemGuardian/
├── app/                    # FastAPI Backend
│   ├── main.py            # API Server
│   ├── routes/            # API Endpoints
│   ├── core/              # Hardware Scanners
│   ├── models/            # Data Models
│   └── utils/             # PDF, JSON, Database
├── ui/                    # Flask Frontend
│   ├── app.py            # Web Server
│   ├── templates/        # HTML Pages
│   └── static/           # CSS & JavaScript
├── db/                    # SQLite Database
└── reports/               # Generated Reports
```

## 🚀 Quick Start | البدء السريع

### Prerequisites | المتطلبات
- Python 3.11+
- Modern web browser
- For best results: pip, virtualenv

### Easy Setup (Recommended) | التثبيت السريع (موصى به)

#### On Linux/macOS:
```bash
chmod +x start.sh
./start.sh
```

#### On Windows:
```bash
start.bat
```

### Manual Setup | التثبيت اليدوي

1. **Create Virtual Environment** | إنشاء بيئة افتراضية
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. **Install Dependencies** | تثبيت المكتبات
```bash
pip install -r requirements.txt
```

3. **Create Required Directories** | إنشاء المجلدات المطلوبة
```bash
mkdir -p db reports/pdfs reports/json
```

4. **Run Backend API** | تشغيل الخادم الخلفي
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API will run on: `http://localhost:8000`

5. **Run Web Interface** (in new terminal) | تشغيل واجهة الويب
```bash
python ui/app.py
```
Web UI will run on: `http://localhost:5000`

### For VS Code Users | لمستخدمي VS Code
See detailed setup guide: [VSCODE_SETUP.md](VSCODE_SETUP.md)

## 📖 Usage | الاستخدام

### For Users | للمستخدمين
1. Open web interface at `http://localhost:5000`
2. Enter your subscription code
3. Click "Verify & Start Scan"
4. View results and export reports

### For Administrators | للمديرين
1. Go to Admin Panel at `http://localhost:5000/admin`
2. Create new subscriptions
3. View active subscriptions
4. Renew or manage existing codes

## 🔌 API Documentation | توثيق API

### Subscription Endpoints
```http
POST   /api/subscription/create     # Create subscription
POST   /api/subscription/verify     # Verify code
POST   /api/subscription/renew/:code # Renew subscription
GET    /api/subscription/list       # List all subscriptions
```

### Scanning Endpoints
```http
POST   /api/scan/start                    # Start system scan
POST   /api/scan/export-pdf               # Generate PDF report
POST   /api/scan/export-json              # Export JSON data
GET    /api/scan/download/pdf/{filename}  # Download PDF report
GET    /api/scan/download/json/{filename} # Download JSON data
```

### Advanced Testing Endpoints | اختبارات متقدمة
```http
POST   /api/scan/test/cpu-stress          # CPU stress test
POST   /api/scan/test/ram-stress          # RAM stress test
POST   /api/scan/test/disk-speed          # Disk speed test
POST   /api/scan/test/gpu-stress          # GPU stress test
POST   /api/scan/test/battery-drain       # Battery drain test
POST   /api/scan/test/internet-speed      # Internet speed test
POST   /api/scan/test/network-ping        # Network ping test
```

For detailed testing documentation, see: [API_TESTS.md](API_TESTS.md)

### Example Request
```javascript
// Verify subscription
fetch('/api/verify-subscription', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        code: 'YOUR-CODE-HERE',
        device_id: 'optional-device-id'
    })
})
```

## 📊 Scan Components | مكونات الفحص

| Component | Information Collected |
|-----------|----------------------|
| **CPU** | Model, Cores, Frequency, Temperature, Usage |
| **RAM** | Total, Available, Used, Percentage |
| **Disk** | Type, Size, Free Space, Usage |
| **GPU** | Name, Memory, Temperature, Driver |
| **Battery** | Charge Level, Health, Status |
| **Network** | Interface, IP, MAC, Ping, Speed |
| **Peripherals** | Keyboard, Mouse, Displays, USB Devices |

## 🎨 Screenshots | لقطات الشاشة

### Main Interface
- Dark mode design
- Real-time scan progress
- Color-coded health indicators

### Admin Panel
- Create subscriptions
- View subscription list
- Renew codes

## 🛣️ Roadmap | خارطة الطريق

### Current Version (v1.0)
- ✅ Full hardware scanning
- ✅ Subscription management
- ✅ PDF & JSON reports
- ✅ Web interface

### Future Enhancements (v2.0)
- 🔄 Advanced stress testing
- 🔄 IOPS benchmarking
- 🔄 Interactive charts
- 🔄 Docker deployment
- 🔄 Email notifications

## 🔒 Security | الأمان

### ⚠️ Important Security Notice
**This is an MVP version intended for development and testing only.**

The admin panel is currently **NOT authenticated**. For production use:
- Implement authentication system
- Add role-based access control
- Protect subscription management endpoints
- See `SECURITY.md` for detailed security guidelines

### Security Features
- ✅ No personal files are accessed
- ✅ Only hardware information is collected
- ✅ Device ID binding prevents code sharing
- ✅ SQLite database for local storage
- ❌ Admin authentication (planned for v2.0)

## 📝 License | الترخيص

This project is for educational and commercial use.

## 🤝 Contributing | المساهمة

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📧 Support | الدعم

For support and questions:
- Check the documentation
- Review API endpoints
- Contact the administrator

---

<div align="center">

**Built with ❤️ using Python, FastAPI, and Flask**

**تم البناء بـ ❤️ باستخدام Python و FastAPI و Flask**

</div>
