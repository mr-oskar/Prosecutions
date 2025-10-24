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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
