# System Guardian - User Guide | دليل المستخدم

## Table of Contents | جدول المحتويات
1. [Getting Started](#getting-started)
2. [For End Users](#for-end-users)
3. [For Administrators](#for-administrators)
4. [Understanding Scan Results](#understanding-scan-results)
5. [Troubleshooting](#troubleshooting)

---

## Getting Started | البدء

### Prerequisites | المتطلبات الأولية
- Windows operating system (for full hardware detection)
- Python 3.11 or higher
- Internet connection (for initial setup and network tests)

### Starting the Application | تشغيل التطبيق

The application consists of two components:
1. **FastAPI Backend** (Port 8000) - Handles scanning and data processing
2. **Flask Web Interface** (Port 5000) - User-facing web application

Both should start automatically. Access the web interface at:
```
http://localhost:5000
```

---

## For End Users | للمستخدمين النهائيين

### Step 1: Obtain a Subscription Code
Contact your administrator to get a subscription code. The code will look like:
```
ABC123XYZ456QRST
```

### Step 2: Enter Your Code
1. Open the web interface at `http://localhost:5000`
2. In the "Subscription Verification" panel:
   - Enter your subscription code
   - (Optional) Enter a Device ID, or leave empty to auto-generate
3. Click "Verify & Start Scan"

### Step 3: Wait for Scan to Complete
The system will scan your computer hardware:
- CPU information and performance
- RAM usage and capacity
- Disk drives and storage
- GPU details (if available)
- Battery status (for laptops)
- Network connectivity
- Connected peripherals

This typically takes 10-30 seconds.

### Step 4: View Results
After scanning completes, you'll see:
- **Overall Health Status** (Excellent, Good, Fair, or Poor)
- **Component Details** in expandable sections
- **Recommendations** for improving system performance

### Step 5: Export Reports
Click the export buttons to generate:
- **PDF Report** - Professional formatted report with tables and color-coded status
- **JSON Data** - Raw data for technical analysis

---

## For Administrators | للمديرين

### Accessing Admin Panel
Navigate to:
```
http://localhost:5000/admin
```

⚠️ **Note**: In the current MVP version, this panel is not password-protected. Use only in trusted environments.

### Creating Subscriptions

1. Go to Admin Panel
2. Fill in the form:
   - **Email Address**: User's email
   - **Duration**: Select from 7, 30, 90, or 365 days
3. Click "Create Subscription"
4. Copy the generated code and send it to the user

### Managing Existing Subscriptions

The admin panel displays all subscriptions with:
- Subscription code
- Associated email
- Active/Inactive status
- Number of scans performed
- Expiration date

### Renewing Subscriptions

1. Find the subscription in the list
2. Click "Renew" button
3. Enter number of days to add
4. Confirm renewal

---

## Understanding Scan Results | فهم نتائج الفحص

### Overall Health Indicators

| Status | Color | Meaning |
|--------|-------|---------|
| Excellent | 🟢 Green | All components performing optimally |
| Good | 🟢 Green | Minor issues, system running well |
| Fair | 🟡 Yellow | Some components need attention |
| Poor | 🔴 Red | Multiple issues detected, action needed |

### Component Status Codes

#### CPU Status
- **Good**: Usage <50%, temperature normal
- **Moderate Load**: Usage 50-80%
- **High Load**: Usage >80%
- **High Temperature**: Temperature >80°C

#### RAM Status
- **Good**: Usage <50%
- **Moderate**: Usage 50-75%
- **High Usage**: Usage 75-90%
- **Critical**: Usage >90%

#### Disk Status
- **Good**: <50% used
- **Moderate**: 50-75% used
- **Warning**: 75-90% used
- **Critical**: >90% used

#### GPU Status
- **Good**: Normal load and temperature
- **Moderate Load**: 50-90% usage
- **High Load**: >90% usage
- **High Temperature**: >80°C

#### Battery Status (Laptops)
- **Fully Charged**: 100% charge
- **Charging**: Plugged in and charging
- **Good**: >50% charge, not plugged in
- **Low Battery**: 20-50% charge
- **Critical**: <20% charge

#### Network Status
- **Excellent**: Ping <50ms
- **Good**: Ping 50-100ms
- **Fair**: Ping 100-200ms
- **Poor**: Ping >200ms
- **No Connection**: Network unavailable

### Common Recommendations

| Recommendation (Arabic) | Recommendation (English) | Action |
|------------------------|-------------------------|--------|
| وحدة المعالجة المركزية تحت ضغط عالٍ | High CPU usage detected | Close unnecessary programs |
| درجة حرارة المعالج مرتفعة | CPU temperature is high | Check cooling system, clean fans |
| استخدام عالٍ للذاكرة العشوائية | High RAM usage | Close unused applications, consider upgrading RAM |
| مساحة القرص شبه ممتلئة | Disk space critical | Delete unnecessary files, move data to external drive |
| صحة البطارية منخفضة | Battery health degraded | Consider battery replacement |
| جودة الاتصال بالإنترنت ضعيفة | Poor network connection | Check router, contact ISP |

---

## Troubleshooting | حل المشكلات

### Scan Fails to Start

**Problem**: Error when clicking "Verify & Start Scan"

**Solutions**:
1. Check that your subscription code is correct
2. Ensure the code hasn't expired
3. Verify both FastAPI and Flask servers are running
4. Check internet connection

### Component Shows "Not Detected"

**Problem**: GPU, Battery, or other component not found

**Explanation**: This is normal if:
- Desktop PCs don't have batteries
- Older systems may not have dedicated GPUs
- Virtual machines may have limited hardware access

This is not an error - the system correctly identifies missing components.

### PDF/JSON Export Fails

**Problem**: Error when exporting reports

**Solutions**:
1. Check that `reports/pdfs/` and `reports/json/` directories exist
2. Ensure you have write permissions
3. Check available disk space

### Slow Network Speed Test

**Problem**: Network test takes very long

**Explanation**: The speed test component may take 30-60 seconds to complete. This is normal behavior when testing actual download/upload speeds.

### Admin Panel Not Accessible

**Problem**: Can't access `/admin`

**Solutions**:
1. Ensure Flask server is running on port 5000
2. Try accessing `http://localhost:5000/admin` directly
3. Check browser console for errors
4. Restart Flask workflow

### Backend API Not Responding

**Problem**: API errors or timeouts

**Solutions**:
1. Check that FastAPI is running on port 8000
2. Test API directly: `http://localhost:8000/health`
3. Check workflow logs for errors
4. Restart FastAPI Backend workflow

---

## FAQ | الأسئلة الشائعة

**Q: How often can I run scans?**  
A: Unlimited scans during your subscription period.

**Q: Does this work on Mac or Linux?**  
A: Partial support. Best results on Windows. Some features (like Battery health, GPU detection) may have limited functionality on other systems.

**Q: Is my data sent to the internet?**  
A: No. All scanning and processing happens locally. Only hardware metadata is collected, no personal files.

**Q: Can I use one code on multiple computers?**  
A: No. Each code is bound to a single device ID after first use.

**Q: What happens when my subscription expires?**  
A: You won't be able to run new scans, but you can still access previous reports.

**Q: Can I generate reports without a subscription?**  
A: No. A valid subscription code is required to perform scans.

---

## Support | الدعم

For technical support or questions:
- Check this guide first
- Review `README.md` for technical details
- Check `SECURITY.md` for security considerations
- Contact your system administrator

---

**Version**: 1.0 (MVP)  
**Last Updated**: October 2025
