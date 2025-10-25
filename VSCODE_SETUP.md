# دليل التشغيل على Visual Studio Code
# VS Code Setup Guide

<div dir="rtl">

## المتطلبات الأساسية | Prerequisites

### 1. تثبيت البرامج المطلوبة | Required Software Installation

#### Python 3.11 أو أحدث
- **Windows**: قم بتحميل Python من [python.org](https://www.python.org/downloads/)
  - تأكد من تفعيل خيار "Add Python to PATH" أثناء التثبيت
- **macOS**: 
  ```bash
  brew install python@3.11
  ```
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install python3.11 python3.11-venv python3-pip
  ```

#### Visual Studio Code
- قم بتحميل VS Code من [code.visualstudio.com](https://code.visualstudio.com/)
- ثبت الإضافات التالية من VS Code Marketplace:
  - **Python** (من Microsoft)
  - **Pylance** (من Microsoft)
  - **Python Debugger** (من Microsoft - اختياري)

---

## خطوات التثبيت | Installation Steps

### الخطوة 1: نسخ المشروع | Step 1: Clone/Download Project

إذا كان المشروع على GitHub:
```bash
git clone <repository-url>
cd system-guardian
```

أو قم بتحميل المشروع كملف ZIP وفك ضغطه.

---

### الخطوة 2: فتح المشروع في VS Code | Step 2: Open in VS Code

1. افتح VS Code
2. اختر `File` → `Open Folder`
3. اختر مجلد المشروع `system-guardian`

---

### الخطوة 3: إنشاء بيئة افتراضية | Step 3: Create Virtual Environment

افتح Terminal في VS Code (`` Ctrl+` `` أو `View` → `Terminal`) وقم بتنفيذ:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

ستظهر `(venv)` في بداية السطر مما يعني أن البيئة الافتراضية مفعّلة.

---

### الخطوة 4: تثبيت المكتبات المطلوبة | Step 4: Install Dependencies

بعد تفعيل البيئة الافتراضية:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**ملاحظة**: قد تستغرق عملية التثبيت بضع دقائق.

---

### الخطوة 5: إنشاء المجلدات المطلوبة | Step 5: Create Required Directories

```bash
mkdir -p db reports/pdfs reports/json
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path db
New-Item -ItemType Directory -Force -Path reports\pdfs
New-Item -ItemType Directory -Force -Path reports\json
```

---

## تشغيل المشروع | Running the Project

### طريقة 1: تشغيل يدوي من Terminal | Method 1: Manual Terminal Execution

#### تشغيل الخادم الخلفي (FastAPI) | Run Backend Server
افتح Terminal جديد:
```bash
# تفعيل البيئة الافتراضية أولاً
source venv/bin/activate  # macOS/Linux
# أو
venv\Scripts\activate  # Windows

# تشغيل FastAPI
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

الخادم سيعمل على: `http://localhost:8000`

#### تشغيل واجهة الويب (Flask) | Run Web Interface
افتح Terminal ثاني:
```bash
# تفعيل البيئة الافتراضية أولاً
source venv/bin/activate  # macOS/Linux
# أو
venv\Scripts\activate  # Windows

# تشغيل Flask
python ui/app.py
```

واجهة الويب ستعمل على: `http://localhost:5000`

---

### طريقة 2: استخدام VS Code Tasks | Method 2: Using VS Code Tasks

#### إنشاء ملف tasks.json

1. اضغط `Ctrl+Shift+P` (أو `Cmd+Shift+P` على macOS)
2. اكتب `Tasks: Configure Task`
3. اختر `Create tasks.json from template`
4. اختر `Others`

5. استبدل محتوى `.vscode/tasks.json` بالتالي:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run FastAPI Backend",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/python",
            "args": [
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--reload"
            ],
            "windows": {
                "command": "${workspaceFolder}\\venv\\Scripts\\python.exe"
            },
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "dedicated",
                "group": "backend"
            },
            "isBackground": true
        },
        {
            "label": "Run Flask Frontend",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/python",
            "args": [
                "ui/app.py"
            ],
            "windows": {
                "command": "${workspaceFolder}\\venv\\Scripts\\python.exe"
            },
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "dedicated",
                "group": "frontend"
            },
            "isBackground": true
        },
        {
            "label": "Run Both Servers",
            "dependsOn": [
                "Run FastAPI Backend",
                "Run Flask Frontend"
            ],
            "problemMatcher": []
        }
    ]
}
```

#### تشغيل المشروع باستخدام Tasks

1. اضغط `Ctrl+Shift+P` (أو `Cmd+Shift+P`)
2. اكتب `Tasks: Run Task`
3. اختر `Run Both Servers`

سيتم فتح نافذتين في Terminal - واحدة للـ Backend وواحدة للـ Frontend.

---

### طريقة 3: استخدام VS Code Launch Configurations | Method 3: Debug Configurations

#### إنشاء ملف launch.json

1. اذهب إلى قائمة Debug (الأيقونة على الجانب الأيسر)
2. اضغط على `create a launch.json file`
3. استبدل محتواه بالتالي:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI Backend",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": false
        },
        {
            "name": "Flask Frontend",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/ui/app.py",
            "console": "integratedTerminal",
            "jinja": true,
            "justMyCode": false
        }
    ],
    "compounds": [
        {
            "name": "Full Application",
            "configurations": [
                "FastAPI Backend",
                "Flask Frontend"
            ],
            "stopAll": true
        }
    ]
}
```

#### تشغيل المشروع مع Debug

1. اذهب إلى قائمة Debug
2. اختر `Full Application` من القائمة المنسدلة
3. اضغط على زر Play الأخضر (أو F5)

---

## الاستخدام | Usage

### 1. الوصول إلى التطبيق | Accessing the Application

بعد تشغيل كلا الخادمين:

- **واجهة الويب الرئيسية**: http://localhost:5000
- **لوحة الإدارة**: http://localhost:5000/admin
- **واجهة API (Swagger Docs)**: http://localhost:8000/docs

---

### 2. إنشاء اشتراك | Creating a Subscription

1. افتح لوحة الإدارة: http://localhost:5000/admin
2. املأ النموذج:
   - **Email**: عنوان بريد إلكتروني
   - **Duration**: اختر مدة الاشتراك (7, 30, 90, أو 365 يوم)
3. اضغط على "Create Subscription"
4. سيتم إنشاء كود اشتراك فريد - احتفظ به

---

### 3. فحص النظام | Scanning System

1. افتح الواجهة الرئيسية: http://localhost:5000
2. أدخل كود الاشتراك
3. اضغط على "Verify & Start Scan"
4. انتظر حتى يكتمل الفحص (قد يستغرق 10-30 ثانية)
5. ستظهر نتائج الفحص مع معلومات تفصيلية عن:
   - المعالج (CPU)
   - الذاكرة العشوائية (RAM)
   - الأقراص (Disks)
   - كرت الشاشة (GPU)
   - البطارية (Battery)
   - الشبكة (Network)
   - الملحقات (Peripherals)

---

### 4. تصدير التقارير | Exporting Reports

بعد الفحص، يمكنك:

#### تحميل تقرير PDF:
- اضغط على زر "Download PDF Report"
- سيتم تحميل تقرير احترافي بصيغة PDF يحتوي على:
  - معلومات مفصلة عن كل قطعة
  - مؤشرات صحة ملونة (🟢 جيد، 🟡 تحذير، 🔴 حرج)
  - توصيات لتحسين الأداء

#### تحميل بيانات JSON:
- اضغط على زر "Download JSON Data"
- سيتم تحميل ملف JSON يحتوي على جميع البيانات الخام

---

### 5. الاختبارات المتقدمة | Advanced Tests

التطبيق يوفر اختبارات متقدمة لكل قطعة:

#### اختبار ضغط المعالج (CPU Stress Test)
```bash
curl -X POST "http://localhost:8000/api/scan/test/cpu-stress?duration=10"
```
- يقوم بتحميل المعالج بشكل كامل للتأكد من أدائه
- يقيس درجة الحرارة والاستخدام

#### اختبار الذاكرة (RAM Stress Test)
```bash
curl -X POST "http://localhost:8000/api/scan/test/ram-stress?duration=10&test_size_mb=100"
```
- يقوم بتخصيص واستخدام الذاكرة
- يتحقق من سرعة القراءة والكتابة

#### اختبار سرعة القرص (Disk Speed Test)
```bash
curl -X POST "http://localhost:8000/api/scan/test/disk-speed?test_size_mb=50"
```
- يقيس سرعة القراءة والكتابة للقرص
- يحدد نوع القرص (HDD/SSD/NVMe)

#### اختبار سرعة الإنترنت (Internet Speed Test)
```bash
curl -X POST "http://localhost:8000/api/scan/test/internet-speed"
```
- يقيس سرعة التحميل والرفع
- يقيس وقت الاستجابة (Ping)

---

## إعدادات VS Code الموصى بها | Recommended VS Code Settings

### إنشاء ملف settings.json

في مجلد `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true,
        "**/venv": false,
        "**/*.db": false
    },
    "files.watcherExclude": {
        "**/venv/**": true,
        "**/__pycache__/**": true
    }
}
```

---

## حل المشاكل الشائعة | Troubleshooting

### المشكلة: "Module not found"
**الحل**: 
```bash
# تأكد من تفعيل البيئة الافتراضية
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# أعد تثبيت المكتبات
pip install -r requirements.txt
```

### المشكلة: "Port already in use"
**الحل**: 
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### المشكلة: البيئة الافتراضية لا تعمل في VS Code
**الحل**:
1. اضغط `Ctrl+Shift+P`
2. اكتب `Python: Select Interpreter`
3. اختر المسار: `./venv/bin/python` (أو `.\venv\Scripts\python.exe` على Windows)

### المشكلة: لا يمكن الوصول إلى الخادم من متصفح آخر
**الحل**:
- تأكد من أن الخادم يعمل على `0.0.0.0` وليس `localhost`
- تحقق من إعدادات الجدار الناري (Firewall)

---

## هيكل المشروع | Project Structure

```
system-guardian/
├── app/                    # FastAPI Backend
│   ├── core/              # Hardware Scanners
│   │   ├── cpu_test.py
│   │   ├── ram_test.py
│   │   ├── disk_test.py
│   │   ├── gpu_test.py
│   │   ├── battery_test.py
│   │   ├── network_test.py
│   │   ├── peripherals_test.py
│   │   └── system_scanner.py
│   ├── routes/            # API Endpoints
│   │   ├── scan.py
│   │   └── subscription.py
│   ├── models/            # Data Models
│   ├── utils/             # Utilities
│   │   ├── database.py
│   │   ├── pdf_generator.py
│   │   └── json_exporter.py
│   └── main.py           # FastAPI App
├── ui/                    # Flask Frontend
│   ├── templates/        # HTML Templates
│   ├── static/          # CSS & JavaScript
│   └── app.py          # Flask App
├── db/                   # Database Files
├── reports/             # Generated Reports
│   ├── pdfs/
│   └── json/
├── venv/                # Virtual Environment
├── requirements.txt     # Python Dependencies
├── README.md
├── VSCODE_SETUP.md     # هذا الملف
└── .gitignore
```

---

## أوامر مفيدة | Useful Commands

### تحديث المكتبات | Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### إنشاء قائمة بالمكتبات المثبتة | Generate Requirements File
```bash
pip freeze > requirements.txt
```

### تنظيف الملفات المؤقتة | Clean Temporary Files
```bash
# macOS/Linux
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Windows PowerShell
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
```

### فحص الأخطاء البرمجية | Linting
```bash
pip install flake8
flake8 app/ ui/
```

---

## الميزات المتقدمة | Advanced Features

### 1. اختبارات شاملة لجميع القطع
- **CPU Stress Test**: اختبار تحمل المعالج تحت الضغط
- **RAM Stress Test**: اختبار سرعة وثبات الذاكرة
- **Disk Speed Test**: قياس سرعة القراءة/الكتابة
- **GPU Monitoring**: مراقبة أداء كرت الشاشة
- **Battery Drain Test**: قياس معدل استهلاك البطارية
- **Network Ping Test**: اختبار جودة واستقرار الاتصال
- **Internet Speed Test**: قياس سرعة الإنترنت الفعلية

### 2. تقارير احترافية
- **PDF Reports**: تقارير ملونة بمؤشرات صحية
- **JSON Export**: بيانات خام للتحليل البرمجي
- **تحميل مباشر**: إمكانية تحميل التقارير مباشرة من الواجهة

### 3. نظام اشتراكات متقدم
- **Device Binding**: ربط الاشتراك بجهاز معين
- **Expiration Tracking**: تتبع انتهاء الاشتراكات
- **Scan Counter**: حساب عدد الفحوصات المنفذة

---

## الأمان | Security

⚠️ **تحذير مهم**: هذه نسخة تطويرية (MVP)

للاستخدام الإنتاجي، يجب:
1. إضافة نظام مصادقة لللوحة الإدارة
2. استخدام HTTPS
3. تشفير قاعدة البيانات
4. إضافة معدل محدد للطلبات (Rate Limiting)
5. استخدام متغيرات بيئة للأسرار (Secrets)

---

## الدعم والمساعدة | Support

إذا واجهت أي مشكلة:

1. **تحقق من الـ Terminal Logs**: راجع رسائل الخطأ في نافذة Terminal
2. **راجع الوثائق**: اقرأ `README.md` و `SECURITY.md`
3. **افحص الـ API Docs**: زر http://localhost:8000/docs للاطلاع على توثيق API

---

## التطوير المستقبلي | Future Development

### النسخة 2.0
- [ ] إضافة مصادقة للمستخدمين
- [ ] لوحة تحكم متقدمة
- [ ] رسوم بيانية تفاعلية
- [ ] إشعارات بالبريد الإلكتروني
- [ ] دعم قواعد بيانات PostgreSQL
- [ ] واجهة برمجية (API) موسعة
- [ ] تطبيق سطح المكتب بـ Electron

---

## الترخيص | License

هذا المشروع متاح للاستخدام التعليمي والتجاري.

---

**تم البناء بـ ❤️ باستخدام Python, FastAPI, و Flask**

**Built with ❤️ using Python, FastAPI, and Flask**

</div>
