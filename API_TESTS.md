# دليل الاختبارات المتقدمة | Advanced Tests Guide

## نظرة عامة | Overview

تم إضافة اختبارات متقدمة (Stress Tests) لجميع قطع الجهاز. هذه الاختبارات تقوم بفحص أداء كل قطعة تحت الضغط أو الاستخدام المكثف.

---

## الاختبارات المتوفرة | Available Tests

### 1. اختبار ضغط المعالج | CPU Stress Test

**الهدف**: قياس أداء المعالج تحت الحمل الكامل وقياس درجة الحرارة

**API Endpoint**:
```http
POST /api/scan/test/cpu-stress
```

**المعاملات**:
- `duration` (int, default=5): مدة الاختبار بالثواني (1-60)

**مثال باستخدام cURL**:
```bash
curl -X POST "http://localhost:8000/api/scan/test/cpu-stress?duration=10"
```

**مثال باستخدام Python**:
```python
import requests
result = requests.post("http://localhost:8000/api/scan/test/cpu-stress", 
                       params={"duration": 10})
print(result.json())
```

**النتائج المتوقعة**:
```json
{
  "test_passed": true,
  "duration_seconds": 10,
  "average_usage_percent": 95.5,
  "max_usage_percent": 98.2,
  "average_temperature_celsius": 72.4,
  "max_temperature_celsius": 78.1,
  "performance_rating": "Excellent - CPU can reach full capacity"
}
```

---

### 2. اختبار ضغط الذاكرة | RAM Stress Test

**الهدف**: اختبار استقرار الذاكرة العشوائية وسرعتها

**API Endpoint**:
```http
POST /api/scan/test/ram-stress
```

**المعاملات**:
- `duration` (int, default=5): مدة الاختبار بالثواني (1-60)
- `test_size_mb` (int, default=100): حجم البيانات المخصصة بالميجابايت (10-1000)

**مثال**:
```bash
curl -X POST "http://localhost:8000/api/scan/test/ram-stress?duration=10&test_size_mb=200"
```

**النتائج المتوقعة**:
```json
{
  "test_passed": true,
  "duration_seconds": 10,
  "memory_allocated_mb": 200,
  "average_usage_percent": 68.4,
  "performance_rating": "Good - Memory allocation successful"
}
```

---

### 3. اختبار سرعة القرص | Disk Speed Test

**الهدف**: قياس سرعات القراءة والكتابة الفعلية للقرص

**API Endpoint**:
```http
POST /api/scan/test/disk-speed
```

**المعاملات**:
- `mount_point` (str, optional): مسار القرص للاختبار
- `test_size_mb` (int, default=50): حجم ملف الاختبار (10-500)

**مثال**:
```bash
curl -X POST "http://localhost:8000/api/scan/test/disk-speed?test_size_mb=100"
```

**النتائج المتوقعة**:
```json
{
  "test_passed": true,
  "write_speed_mbps": 452.3,
  "read_speed_mbps": 498.7,
  "estimated_disk_type": "SATA SSD",
  "performance_rating": "Good - SATA SSD"
}
```

---

### 4. اختبار كرت الشاشة | GPU Stress Test

**الهدف**: مراقبة أداء كرت الشاشة وقياس درجة الحرارة

**API Endpoint**:
```http
POST /api/scan/test/gpu-stress
```

**المعاملات**:
- `duration` (int, default=10): مدة الاختبار بالثواني (1-60)
- `gpu_id` (int, default=0): رقم كرت الشاشة

**مثال**:
```bash
curl -X POST "http://localhost:8000/api/scan/test/gpu-stress?duration=15"
```

**النتائج المتوقعة**:
```json
{
  "test_passed": true,
  "gpu_name": "NVIDIA GeForce RTX 3060",
  "average_load_percent": 45.2,
  "max_temperature_celsius": 68.5,
  "performance_rating": "GPU monitoring successful"
}
```

---

### 5. اختبار استنزاف البطارية | Battery Drain Test

**الهدف**: قياس معدل استهلاك البطارية

**API Endpoint**:
```http
POST /api/scan/test/battery-drain
```

**المعاملات**:
- `duration` (int, default=30): مدة الاختبار بالثواني (10-300)

**ملاحظة**: يجب فصل الشاحن من الجهاز قبل الاختبار

**مثال**:
```bash
curl -X POST "http://localhost:8000/api/scan/test/battery-drain?duration=60"
```

**النتائج المتوقعة**:
```json
{
  "test_passed": true,
  "drain_rate_percent_per_hour": 8.5,
  "estimated_time_remaining_hours": 10.2,
  "performance_rating": "Good - Normal power consumption"
}
```

---

### 6. اختبار سرعة الإنترنت | Internet Speed Test

**الهدف**: قياس سرعة التحميل والرفع الفعلية

**API Endpoint**:
```http
POST /api/scan/test/internet-speed
```

**ملاحظة**: قد يستغرق 30-60 ثانية

**مثال**:
```bash
curl -X POST "http://localhost:8000/api/scan/test/internet-speed"
```

**النتائج المتوقعة**:
```json
{
  "test_passed": true,
  "download_speed_mbps": 95.4,
  "upload_speed_mbps": 45.2,
  "ping_ms": 18.5,
  "server_name": "Speedtest Server",
  "performance_rating": "Excellent - High-speed connection"
}
```

---

### 7. اختبار جودة الشبكة | Network Ping Test

**الهدف**: قياس استقرار الاتصال وجودة الشبكة

**API Endpoint**:
```http
POST /api/scan/test/network-ping
```

**المعاملات**:
- `host` (str, default="8.8.8.8"): الخادم المستهدف
- `count` (int, default=20): عدد الطلبات (5-100)

**مثال**:
```bash
curl -X POST "http://localhost:8000/api/scan/test/network-ping?host=8.8.8.8&count=30"
```

**النتائج المتوقعة**:
```json
{
  "test_passed": true,
  "packets_sent": 30,
  "packets_received": 30,
  "packet_loss_percent": 0,
  "average_ping_ms": 22.3,
  "jitter_ms": 3.2,
  "connection_stability": "Excellent - Very stable",
  "performance_rating": "Excellent - Ideal for gaming"
}
```

---

## استخدام الاختبارات من واجهة الويب | Using Tests from Web UI

يمكنك إضافة أزرار للاختبارات في واجهة الويب:

```javascript
// مثال: اختبار CPU
async function testCPU() {
    const result = await fetch('/api/test/cpu-stress', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({duration: 10})
    });
    const data = await result.json();
    console.log(data);
}

// مثال: اختبار سرعة الإنترنت
async function testInternetSpeed() {
    showLoading("Testing internet speed... This may take 30-60 seconds");
    const result = await fetch('/api/test/internet-speed', {
        method: 'POST'
    });
    const data = await result.json();
    hideLoading();
    displayResults(data);
}
```

---

## دمج الاختبارات في سكريبت Python | Integration in Python Script

```python
import requests
import time

API_BASE = "http://localhost:8000"

def run_all_tests():
    print("Running comprehensive hardware tests...")
    
    # CPU Test
    print("\n1. Testing CPU...")
    cpu_result = requests.post(f"{API_BASE}/api/scan/test/cpu-stress",
                               params={"duration": 10}).json()
    print(f"CPU Test: {cpu_result['data']['performance_rating']}")
    
    # RAM Test
    print("\n2. Testing RAM...")
    ram_result = requests.post(f"{API_BASE}/api/scan/test/ram-stress",
                               params={"duration": 10, "test_size_mb": 100}).json()
    print(f"RAM Test: {ram_result['data']['performance_rating']}")
    
    # Disk Test
    print("\n3. Testing Disk...")
    disk_result = requests.post(f"{API_BASE}/api/scan/test/disk-speed",
                                params={"test_size_mb": 50}).json()
    print(f"Disk Test: {disk_result['data']['performance_rating']}")
    
    # Network Test
    print("\n4. Testing Network...")
    network_result = requests.post(f"{API_BASE}/api/scan/test/network-ping",
                                   params={"count": 20}).json()
    print(f"Network Test: {network_result['data']['performance_rating']}")
    
    print("\n✓ All tests completed!")

if __name__ == "__main__":
    run_all_tests()
```

---

## ملاحظات هامة | Important Notes

### التحذيرات | Warnings

1. **اختبار CPU Stress**: سيرفع استخدام المعالج إلى 100% - قد يصبح الجهاز بطيئاً مؤقتاً
2. **اختبار RAM**: قد يستهلك ذاكرة كبيرة - تأكد من إغلاق التطبيقات المهمة
3. **اختبار Battery**: يجب فصل الشاحن للحصول على نتائج دقيقة
4. **اختبار Internet Speed**: يستهلك بيانات إنترنت (حوالي 100-500 MB)

### التوصيات | Recommendations

- لا تشغل اختبارات متعددة في نفس الوقت
- راقب درجة الحرارة خلال الاختبارات
- أغلق التطبيقات الأخرى للحصول على نتائج دقيقة
- استخدم مدة اختبار قصيرة (5-10 ثواني) في البداية

---

## معلومات إضافية | Additional Information

### تفسير النتائج | Interpreting Results

#### CPU Performance Rating:
- **Excellent**: 90%+ استخدام - المعالج يعمل بكامل طاقته
- **Good**: 70-90% استخدام - أداء جيد
- **Fair**: 50-70% استخدام - أداء متوسط
- **Poor**: <50% استخدام - قد يكون هناك Thermal Throttling

#### Disk Performance Rating:
- **Excellent**: >1500 MB/s - NVMe SSD عالي الأداء
- **Very Good**: >800 MB/s - NVMe SSD
- **Good**: >400 MB/s - SATA SSD
- **Fair**: >150 MB/s - SSD أو HDD سريع
- **Poor**: <80 MB/s - قرص بطيء

#### Network Connection Quality:
- **Excellent**: <20ms ping, 0% packet loss
- **Good**: <50ms ping, <1% packet loss
- **Fair**: <100ms ping, <3% packet loss
- **Poor**: >100ms ping أو >5% packet loss

---

**تم إنشاؤه مع ❤️ لمشروع System Guardian**
