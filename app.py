"""GuardShield - Advanced Organizational Cybersecurity Monitor"""
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import threading, time, random
from datetime import datetime
from modules.gs_monitor import GuardShieldMonitor
from modules.gs_intel import NigeriaIntelFeed, AdvancedMitigations

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guardshield-ng-2026'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

monitor = GuardShieldMonitor()
intel = NigeriaIntelFeed()
mitigations = AdvancedMitigations()

LANDING = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>GuardShield — Team Cybersecurity Monitor</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
<style>
:root{--bg:#030810;--s:#080f1c;--s2:#0d1628;--b:#162030;--acc:#00d4ff;--a2:#7c3aed;--r:#ef4444;--w:#f59e0b;--gr:#10b981;--t:#e0eeff;--m:#4a6080;}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);color:var(--t);font-family:'Space Grotesk',sans-serif;min-height:100vh;}
body::before{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(0,212,255,.03)1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,.03)1px,transparent 1px);background-size:50px 50px;pointer-events:none;}
header{padding:16px 28px;display:flex;align-items:center;justify-content:space-between;background:rgba(3,8,16,.9);border-bottom:1px solid var(--b);position:sticky;top:0;z-index:100;}
.logo{display:flex;align-items:center;gap:10px;font-size:20px;font-weight:700;color:var(--acc);}
.logo-icon{width:36px;height:36px;background:linear-gradient(135deg,var(--acc),var(--a2));border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px;}
.pd{width:7px;height:7px;border-radius:50%;background:var(--gr);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.live{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--gr);font-family:'DM Mono',monospace;}
.btn{padding:9px 20px;background:linear-gradient(135deg,var(--acc),#0099bb);color:#030810;border:none;border-radius:8px;font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:700;cursor:pointer;transition:all .2s;}
.btn:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(0,212,255,.3);}
main{max-width:1280px;margin:0 auto;padding:28px 24px;}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;}
.metric{background:var(--s);border:1px solid var(--b);border-radius:12px;padding:16px;position:relative;overflow:hidden;}
.metric::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--acc),var(--a2));}
.ml{font-size:10px;color:var(--m);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;}
.mv{font-size:26px;font-weight:700;}
.ms{font-size:11px;color:var(--m);margin-top:3px;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px;}
.card{background:var(--s);border:1px solid var(--b);border-radius:16px;padding:20px;}
.ct{font-size:11px;font-weight:600;color:var(--m);text-transform:uppercase;letter-spacing:.5px;margin-bottom:14px;font-family:'DM Mono',monospace;display:flex;align-items:center;gap:6px;}
.dot{width:6px;height:6px;border-radius:50%;background:var(--acc);box-shadow:0 0 6px var(--acc);}
.tabs{display:flex;gap:4px;background:var(--s);border:1px solid var(--b);border-radius:9px;padding:4px;width:fit-content;margin-bottom:20px;}
.tab{padding:7px 16px;border-radius:6px;font-size:13px;border:none;background:transparent;color:var(--m);cursor:pointer;font-family:'Space Grotesk',sans-serif;font-weight:500;}
.tab.active{background:var(--s2);color:var(--acc);}
.page{display:none;}
.page.active{display:block;}
.al{background:var(--s2);border-radius:10px;padding:12px 14px;margin-bottom:8px;border-left:3px solid;}
.al.critical{border-color:var(--r);}
.al.high{border-color:var(--w);}
.al.medium{border-color:var(--acc);}
.at{font-size:13px;font-weight:600;margin-bottom:3px;}
.ad{font-size:11px;color:var(--m);margin-bottom:5px;}
.badge{font-size:10px;padding:2px 7px;border-radius:20px;font-family:'DM Mono',monospace;}
.bc{background:rgba(239,68,68,.15);color:#ef4444;}
.bw{background:rgba(245,158,11,.15);color:#f59e0b;}
.ba{background:rgba(0,212,255,.15);color:var(--acc);}
.bs{background:rgba(16,185,129,.15);color:#10b981;}
.team-item{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--b);}
.team-item:last-child{border-bottom:none;}
.team-avatar{width:36px;height:36px;border-radius:50%;background:var(--s2);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;}
.team-name{font-size:13px;font-weight:500;}
.team-device{font-size:11px;color:var(--m);}
.team-score{font-family:'DM Mono',monospace;font-size:13px;font-weight:700;}
.scan-item{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid rgba(22,32,48,.5);}
.scan-item:last-child{border-bottom:none;}
.scan-icon{width:30px;height:30px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}
.si-ok{background:rgba(16,185,129,.15);color:#10b981;}
.si-warn{background:rgba(245,158,11,.15);color:#f59e0b;}
.scan-name{font-size:13px;font-weight:500;flex:1;}
.scan-score{font-size:11px;color:var(--m);font-family:'DM Mono',monospace;}
.prog-wrap{margin-bottom:10px;}
.prog-label{display:flex;justify-content:space-between;font-size:11px;color:var(--m);margin-bottom:5px;}
.prog-bar{height:5px;background:var(--s2);border-radius:3px;overflow:hidden;}
.prog-fill{height:100%;border-radius:3px;}
.intel-card{background:var(--s2);border:1px solid var(--b);border-radius:10px;padding:14px;margin-bottom:10px;}
.mit-step{display:flex;gap:10px;margin-bottom:12px;}
.mit-num{width:24px;height:24px;border-radius:50%;background:rgba(0,212,255,.15);color:var(--acc);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;}
.mit-action{font-size:13px;font-weight:500;margin-bottom:3px;}
.mit-cmd{background:var(--bg);border-radius:7px;padding:7px 10px;font-family:'DM Mono',monospace;font-size:11px;color:var(--acc);margin-top:3px;white-space:pre-wrap;}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.8);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(6px);}
.modal-overlay.open{display:flex;}
.modal{background:var(--s);border:1px solid var(--b);border-radius:18px;padding:28px;max-width:520px;width:90%;max-height:80vh;overflow-y:auto;}
.modal-close{background:none;border:1px solid var(--b);color:var(--m);padding:4px 10px;border-radius:6px;cursor:pointer;font-size:12px;float:right;}
.mit-title{font-size:17px;font-weight:700;margin-bottom:4px;}
.mit-sub{font-size:12px;color:var(--acc);font-family:'DM Mono',monospace;margin-bottom:18px;}
.prev-item{display:flex;gap:8px;font-size:12px;color:var(--m);padding:4px 0;}
.prev-item i{color:var(--gr);flex-shrink:0;}
@media(max-width:768px){.metrics{grid-template-columns:repeat(2,1fr);}.grid2{grid-template-columns:1fr;}}
</style>
</head>
<body>
<header>
  <div class="logo"><div class="logo-icon">🛡️</div>GuardShield</div>
  <div style="display:flex;align-items:center;gap:14px;">
    <div class="live"><span class="pd"></span>Team Protection Active</div>
    <button class="btn" onclick="runScan()">🔍 Run Scan</button>
  </div>
</header>
<main>
  <div class="tabs">
    <button class="tab active" onclick="showTab('dashboard',this)">Dashboard</button>
    <button class="tab" onclick="showTab('scan',this)">Scanner</button>
    <button class="tab" onclick="showTab('team',this)">Team Status</button>
    <button class="tab" onclick="showTab('intel',this)">Nigeria Intel</button>
    <button class="tab" onclick="showTab('zt',this)">Zero-Trust</button>
  </div>

  <div class="page active" id="page-dashboard">
    <div class="metrics">
      <div class="metric"><div class="ml">Security Score</div><div class="mv" style="color:var(--gr)" id="m-score">--</div><div class="ms">Overall posture</div></div>
      <div class="metric"><div class="ml">Active Threats</div><div class="mv" style="color:var(--r)" id="m-threats">--</div><div class="ms">Nigeria intel</div></div>
      <div class="metric"><div class="ml">Team Members</div><div class="mv" style="color:var(--acc)" id="m-team">4</div><div class="ms">Monitored</div></div>
      <div class="metric"><div class="ml">Zero-Trust Score</div><div class="mv" style="color:var(--w)">72</div><div class="ms">Needs improvement</div></div>
    </div>
    <div class="grid2">
      <div class="card"><div class="ct"><span class="dot"></span>Live Threat Alerts</div><div id="alertFeed"><div style="text-align:center;padding:20px;color:var(--m);font-size:13px;">Monitoring for threats...</div></div></div>
      <div class="card"><div class="ct"><span class="dot"></span>Nigeria Threat Intel</div><div id="intelFeed"><div style="text-align:center;padding:20px;color:var(--m);font-size:13px;">Loading intel...</div></div></div>
    </div>
  </div>

  <div class="page" id="page-scan">
    <div class="grid2">
      <div class="card">
        <div class="ct"><span class="dot"></span>Security Scanner</div>
        <div style="display:flex;gap:10px;margin-bottom:18px;">
          <button class="btn" onclick="runScan('quick')" style="flex:1">⚡ Quick Scan</button>
          <button class="btn" onclick="runScan('deep')" style="flex:1;background:linear-gradient(135deg,var(--a2),#5b21b6)">🔬 Deep Scan</button>
        </div>
        <div id="scanResults"><div style="text-align:center;padding:30px;color:var(--m);">Click scan to start</div></div>
      </div>
      <div class="card">
        <div class="ct"><span class="dot"></span>Security Posture</div>
        <div id="postureSection"><div style="text-align:center;padding:30px;color:var(--m);">Run a scan to see breakdown</div></div>
      </div>
    </div>
  </div>

  <div class="page" id="page-team">
    <div class="card"><div class="ct"><span class="dot"></span>Team Security Status</div><div id="teamList"><div style="text-align:center;padding:20px;color:var(--m);">Loading team...</div></div></div>
  </div>

  <div class="page" id="page-intel">
    <div class="card"><div class="ct"><span class="dot"></span>Nigeria Threat Intelligence — EFCC · NITDA · CBN · NCC</div><div id="intelList"><div style="text-align:center;padding:20px;color:var(--m);">Loading...</div></div></div>
  </div>

  <div class="page" id="page-zt">
    <div class="card">
      <div class="ct"><span class="dot"></span>Zero-Trust Posture Score</div>
      <div id="ztSection"><div style="text-align:center;padding:20px;color:var(--m);">Loading...</div></div>
    </div>
  </div>
</main>

<div class="modal-overlay" id="modal" onclick="closeModal(event)">
  <div class="modal">
    <button class="modal-close" onclick="closeModal()">✕ Close</button>
    <div id="modalContent"></div>
  </div>
</div>

<script>
const socket=io();
socket.on('connect',()=>{socket.emit('start_monitoring');loadDashboard();});
socket.on('team_alert',t=>addAlert(t));
function showTab(id,btn){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.getElementById('page-'+id).classList.add('active');if(btn)btn.classList.add('active');if(id==='team')loadTeam();if(id==='intel')loadIntel();if(id==='zt')loadZeroTrust();}
async function loadDashboard(){try{const r=await fetch('/api/dashboard');const d=await r.json();document.getElementById('m-score').textContent=(d.score||{}).score||'--';document.getElementById('m-threats').textContent=(d.intel_feed||{}).critical||'--';renderAlerts(d.threats||[]);renderMiniIntel(d.intel_feed||{});}catch(e){console.log(e);}}
function renderAlerts(t){const f=document.getElementById('alertFeed');if(!t.length){f.innerHTML='<div style="text-align:center;padding:20px;color:var(--m);font-size:13px;">No active threats ✓</div>';return;}f.innerHTML=t.slice(0,4).map(x=>`<div class="al ${x.severity}" style="cursor:pointer" onclick="showMitigation('${x.mitigation_id||'phishing'}')"><div class="at">${x.title}</div><div class="ad">${x.description||x.desc||''}</div><div style="display:flex;align-items:center;gap:8px;"><span class="badge ${x.severity==='critical'?'bc':x.severity==='high'?'bw':'ba'}">${x.severity}</span><button style="font-size:10px;padding:2px 8px;border-radius:20px;border:1px solid var(--b);background:transparent;color:var(--acc);cursor:pointer;" onclick="event.stopPropagation();showMitigation('${x.mitigation_id||'phishing'}')">Mitigate →</button></div></div>`).join('');}
function renderMiniIntel(d){document.getElementById('intelFeed').innerHTML=`<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;"><div class="intel-card" style="text-align:center"><div style="font-size:24px;font-weight:700;color:var(--r)">${d.critical||0}</div><div style="font-size:11px;color:var(--m);">Critical Threats</div></div><div class="intel-card" style="text-align:center"><div style="font-size:24px;font-weight:700;color:var(--acc)">${d.total_threats||0}</div><div style="font-size:11px;color:var(--m);">Total Threats</div></div></div><div style="margin-top:10px;font-size:11px;color:var(--m);font-family:'DM Mono',monospace;">Sources: ${d.source||'EFCC, NITDA, CBN, NCC'}</div>`;}
function addAlert(t){const f=document.getElementById('alertFeed');const d=document.createElement('div');d.className=`al ${t.severity||'medium'}`;d.innerHTML=`<div class="at">${t.title}</div><div class="ad">${t.description||''}</div><span class="badge ${t.severity==='critical'?'bc':'bw'}">${t.severity||'high'}</span> <span style="font-size:10px;color:var(--m);font-family:'DM Mono',monospace;">Just now</span>`;f.insertBefore(d,f.firstChild);}
async function runScan(type='quick'){const btn=event.target;btn.textContent='Scanning...';btn.disabled=true;try{const r=await fetch('/api/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type})});const d=await r.json();renderScan(d);}catch(e){console.log(e);}btn.textContent=type==='quick'?'⚡ Quick Scan':'🔬 Deep Scan';btn.disabled=false;}
function renderScan(d){const cats=d.categories||[];document.getElementById('scanResults').innerHTML=cats.map(c=>`<div class="scan-item"><div class="scan-icon ${c.status==='ok'?'si-ok':'si-warn'}"><i class="ti ${c.icon||'ti-shield'}"></i></div><div style="flex:1"><div class="scan-name">${c.name}</div><div class="scan-score">Score: ${c.score}/100</div></div><span class="badge ${c.status==='ok'?'bs':'bw'}">${c.status==='ok'?'Secure':'Warning'}</span></div>`).join('');document.getElementById('postureSection').innerHTML=cats.map(c=>`<div class="prog-wrap"><div class="prog-label"><span>${c.name}</span><span>${c.score}%</span></div><div class="prog-bar"><div class="prog-fill" style="width:${c.score}%;background:${c.score>=80?'var(--gr)':c.score>=60?'var(--w)':'var(--r)'}"></div></div></div>`).join('');}
async function loadTeam(){try{const r=await fetch('/api/team-status');const t=await r.json();document.getElementById('teamList').innerHTML=t.map(m=>`<div class="team-item"><div class="team-avatar">${m.status==='secure'?'🟢':m.status==='warning'?'🟡':'🔴'}</div><div style="flex:1"><div class="team-name">${m.name}</div><div class="team-device">${m.device} · ${m.last_seen}</div></div><div style="text-align:right"><div class="team-score" style="color:${m.score>=80?'var(--gr)':m.score>=60?'var(--w)':'var(--r)'}">${m.score}</div><span class="badge ${m.status==='secure'?'bs':m.status==='warning'?'bw':'bc'}">${m.status}</span></div></div>`).join('');}catch(e){console.log(e);}}
async function loadIntel(){try{const r=await fetch('/api/threats');const t=await r.json();document.getElementById('intelList').innerHTML=t.map(x=>`<div class="al ${x.severity}" style="margin-bottom:10px;cursor:pointer" onclick="showMitigation('${x.mitigation_id||'phishing'}')"><div style="display:flex;justify-content:space-between;margin-bottom:5px;"><div class="at">${x.title}</div><span class="badge ${x.severity==='critical'?'bc':x.severity==='high'?'bw':'ba'}">${x.severity.toUpperCase()}</span></div><div class="ad">${x.description||x.desc||''}</div><div style="margin-top:6px;font-size:11px;color:var(--acc);font-family:'DM Mono',monospace;">${x.mitigation||''}</div><div style="margin-top:3px;font-size:10px;color:var(--m);">Affected: ${(x.affected_banks||[x.affected||'Multiple']).join?.(', ')}</div></div>`).join('');}catch(e){console.log(e);}}
async function loadZeroTrust(){try{const r=await fetch('/api/zero-trust');const d=await r.json();document.getElementById('ztSection').innerHTML=`<div style="text-align:center;margin-bottom:20px"><div style="font-size:52px;font-weight:700;color:${d.overall>=80?'var(--gr)':d.overall>=60?'var(--w)':'var(--r)'}">${d.overall}</div><div style="font-size:13px;color:var(--m)">Zero-Trust Score</div></div>${[['Identity',d.identity],['Device',d.device],['Network',d.network],['Application',d.application],['Data',d.data]].map(([k,v])=>`<div class="prog-wrap"><div class="prog-label"><span>${k}</span><span>${v}%</span></div><div class="prog-bar"><div class="prog-fill" style="width:${v}%;background:${v>=80?'var(--gr)':v>=60?'var(--w)':'var(--r)'}"></div></div></div>`).join('')}<div style="margin-top:14px;background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.2);border-radius:9px;padding:12px;font-size:12px;color:var(--t);">${d.recommendation||''}</div>`;}catch(e){console.log(e);}}
async function showMitigation(id){try{const r=await fetch('/api/mitigation/'+id);const m=await r.json();document.getElementById('modalContent').innerHTML=`<div class="mit-title">🛡️ ${m.title}</div><div class="mit-sub">Est. time: ${m.estimated_time} · Severity: ${m.severity}</div><div style="font-size:11px;font-weight:600;color:var(--acc);margin-bottom:10px;font-family:'DM Mono',monospace;">MITIGATION STEPS</div>${(m.steps||[]).map(s=>`<div class="mit-step"><div class="mit-num">${s.step}</div><div><div class="mit-action">${s.action}</div>${s.command?`<div class="mit-cmd">${s.command}</div>`:''}</div></div>`).join('')}<div style="margin-top:14px;"><div style="font-size:11px;font-weight:600;color:var(--gr);margin-bottom:8px;font-family:'DM Mono',monospace;">PREVENTION</div>${(m.prevention||[]).map(p=>`<div class="prev-item"><i class="ti ti-check"></i>${p}</div>`).join('')}</div>`;document.getElementById('modal').classList.add('open');}catch(e){console.log(e);}}
function closeModal(e){if(!e||e.target===document.getElementById('modal'))document.getElementById('modal').classList.remove('open');}
</script>
</body>
</html>"""

@app.route('/')
def index():
    return LANDING

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
    emit('connected', {'status': 'GuardShield active'})

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
    emit('monitoring_started', {'message': 'Team monitoring active'})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5003, allow_unsafe_werkzeug=True)
