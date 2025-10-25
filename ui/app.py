from flask import Flask, render_template, request, jsonify, send_file
import requests
import uuid
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

API_BASE_URL = "http://localhost:8000"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/api/create-subscription', methods=['POST'])
def create_subscription():
    try:
        data = request.json
        response = requests.post(
            f"{API_BASE_URL}/api/subscription/create",
            json=data
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/verify-subscription', methods=['POST'])
def verify_subscription():
    try:
        data = request.json
        response = requests.post(
            f"{API_BASE_URL}/api/subscription/verify",
            json=data
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/start-scan', methods=['POST'])
def start_scan():
    try:
        data = request.json
        subscription_code = data.get('subscription_code')
        device_id = data.get('device_id', str(uuid.uuid4()))
        
        response = requests.post(
            f"{API_BASE_URL}/api/scan/start",
            params={'subscription_code': subscription_code, 'device_id': device_id}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    try:
        data = request.json
        response = requests.post(
            f"{API_BASE_URL}/api/scan/export-pdf",
            json=data
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/export-json', methods=['POST'])
def export_json():
    try:
        data = request.json
        response = requests.post(
            f"{API_BASE_URL}/api/scan/export-json",
            json=data
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/download/<file_type>/<path:file_name>')
def download_report(file_type, file_name):
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/scan/download/{file_type}/{file_name}",
            stream=True
        )
        
        if response.status_code == 200:
            return response.content, 200, {
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': f'attachment; filename="{file_name}"'
            }
        else:
            return jsonify({"success": False, "error": "File not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/list-subscriptions', methods=['GET'])
def list_subscriptions():
    try:
        response = requests.get(f"{API_BASE_URL}/api/subscription/list")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/renew-subscription/<code>', methods=['POST'])
def renew_subscription(code):
    try:
        data = request.json
        additional_days = data.get('additional_days', 30)
        response = requests.post(
            f"{API_BASE_URL}/api/subscription/renew/{code}",
            params={'additional_days': additional_days}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/test/cpu-stress', methods=['POST'])
def test_cpu_stress():
    try:
        data = request.json or {}
        duration = data.get('duration', 5)
        response = requests.post(
            f"{API_BASE_URL}/api/scan/test/cpu-stress",
            params={'duration': duration}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/test/ram-stress', methods=['POST'])
def test_ram_stress():
    try:
        data = request.json or {}
        duration = data.get('duration', 5)
        test_size_mb = data.get('test_size_mb', 100)
        response = requests.post(
            f"{API_BASE_URL}/api/scan/test/ram-stress",
            params={'duration': duration, 'test_size_mb': test_size_mb}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/test/disk-speed', methods=['POST'])
def test_disk_speed():
    try:
        data = request.json or {}
        mount_point = data.get('mount_point', None)
        test_size_mb = data.get('test_size_mb', 50)
        response = requests.post(
            f"{API_BASE_URL}/api/scan/test/disk-speed",
            params={'mount_point': mount_point, 'test_size_mb': test_size_mb}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/test/gpu-stress', methods=['POST'])
def test_gpu_stress():
    try:
        data = request.json or {}
        duration = data.get('duration', 10)
        gpu_id = data.get('gpu_id', 0)
        response = requests.post(
            f"{API_BASE_URL}/api/scan/test/gpu-stress",
            params={'duration': duration, 'gpu_id': gpu_id}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/test/battery-drain', methods=['POST'])
def test_battery_drain():
    try:
        data = request.json or {}
        duration = data.get('duration', 30)
        response = requests.post(
            f"{API_BASE_URL}/api/scan/test/battery-drain",
            params={'duration': duration}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/test/internet-speed', methods=['POST'])
def test_internet_speed():
    try:
        response = requests.post(f"{API_BASE_URL}/api/scan/test/internet-speed")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/test/network-ping', methods=['POST'])
def test_network_ping():
    try:
        data = request.json or {}
        host = data.get('host', '8.8.8.8')
        count = data.get('count', 20)
        response = requests.post(
            f"{API_BASE_URL}/api/scan/test/network-ping",
            params={'host': host, 'count': count}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
