"""
GuardShield - Advanced Organizational Cybersecurity Monitor
Features beyond CyberShieldNG:
- Team threat sharing (if one is attacked, all are alerted)
- Weekly security health email reports
- AI chat assistant for mitigation
- Nigeria-specific threat intelligence
- Mobile companion alerts
- Zero-trust posture scoring
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading, time, random
from datetime import datetime
from modules.gs_monitor import GuardShieldMonitor
from modules.gs_intel import NigeriaIntelFeed
from modules.gs_mitigations import AdvancedMitigations

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guardshield-ng-2026'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

monitor = GuardShieldMonitor()
intel = NigeriaIntelFeed()
mitigations = AdvancedMitigations()

@app.route('/')
def index():
    return render_template('guardshield.html')

@app.route('/api/scan', methods=['POST'])
def scan():
    scan_type = request.json.get('type', 'quick')
    return jsonify(monitor.run_scan(scan_type))

@app.route('/api/threats', methods=['GET'])
def threats():
    return jsonify(intel.get_threats())

@app.route('/api/mitigation/<threat_id>', methods=['GET'])
def mitigation(threat_id):
    return jsonify(mitigations.get(threat_id))

@app.route('/api/team-status', methods=['GET'])
def team_status():
    return jsonify(monitor.get_team_status())

@app.route('/api/zero-trust', methods=['GET'])
def zero_trust():
    return jsonify(monitor.get_zero_trust_score())

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    return jsonify({
        'score': monitor.get_score(),
        'threats': intel.get_threats(),
        'team': monitor.get_team_status(),
        'zero_trust': monitor.get_zero_trust_score(),
        'devices': monitor.get_devices(),
        'intel_feed': intel.get_nigeria_intel()
    })

@socketio.on('connect')
def on_connect():
    emit('connected', {'status': 'GuardShield active — Team protection enabled'})

@socketio.on('start_monitoring')
def start_monitoring():
    def push_threats():
        while True:
            threat = intel.simulate_threat()
            if threat:
                socketio.emit('team_alert', threat)
            time.sleep(random.uniform(8, 18))
    t = threading.Thread(target=push_threats, daemon=True)
    t.start()
    emit('monitoring_started', {'message': 'Team-wide threat monitoring active'})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5003, allow_unsafe_werkzeug=True)
