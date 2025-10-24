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
- ✅ **Comprehensive Hardware Scanning** - فحص شامل للعتاد
  - CPU (Model, Cores, Frequency, Temperature, Usage)
  - RAM (Total, Available, Speed, Usage)
  - Disk (Type: HDD/SSD/NVMe, Size, Speed, Usage)
  - GPU (Model, Memory, Temperature, Driver)
  - Battery (Charge, Health, Status)
  - Network (Interface, Speed, Ping, Connection Quality)
  - Peripherals (Keyboard, Mouse, Display, USB Devices)

- 🔐 **Subscription Management** - إدارة الاشتراكات
  - Code-based access control
  - Expiration tracking (7, 30, 90, 365 days)
  - Device binding
  - Scan count tracking

- 📄 **Professional Reports** - تقارير احترافية
  - PDF reports with color-coded status (🟢 Good, 🟡 Warning, 🔴 Critical)
  - JSON exports with raw data
  - Personalized recommendations

- 🌐 **Modern Web Interface** - واجهة ويب حديثة
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

### Installation | التثبيت

1. **Install Dependencies** | تثبيت المكتبات
```bash
pip install flask fastapi uvicorn psutil GPUtil reportlab speedtest-cli requests pydantic python-multipart
```

2. **Run Backend API** | تشغيل الخادم الخلفي
```bash
python app/main.py
```
API will run on: `http://localhost:8000`

3. **Run Web Interface** | تشغيل واجهة الويب
```bash
python ui/app.py
```
Web UI will run on: `http://localhost:5000`

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
POST   /api/scan/start              # Start system scan
POST   /api/scan/export-pdf         # Generate PDF report
POST   /api/scan/export-json        # Export JSON data
```

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
