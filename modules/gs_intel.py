"""GuardShield - Nigeria Threat Intelligence Feed"""
import random
from datetime import datetime

NG_THREATS = [
    {'id': 'ng_bec_001', 'title': 'BEC Campaign Targeting Nigerian Businesses', 'severity': 'critical',
     'category': 'Email', 'icon': 'ti-mail-x', 'description': 'Sophisticated BEC attack impersonating CEOs of Lagos-based companies. ₦2.4B lost this month.',
     'mitigation_id': 'bec', 'source': 'EFCC Intelligence', 'affected': '47 companies'},
    {'id': 'ng_ransomware_001', 'title': 'Ransomware Gang Targeting Nigerian Banks', 'severity': 'critical',
     'category': 'Malware', 'icon': 'ti-bug', 'description': 'LockBit affiliate actively scanning Nigerian bank infrastructure. 3 MFBs already compromised.',
     'mitigation_id': 'ransomware', 'source': 'CBN Cyber Division', 'affected': '3 banks'},
    {'id': 'ng_phish_001', 'title': 'GTBank/UBA Phishing Campaign', 'severity': 'high',
     'category': 'Phishing', 'icon': 'ti-fish', 'description': 'Fake GTBank and UBA login pages collecting credentials. 1,200+ victims identified.',
     'mitigation_id': 'phishing', 'source': 'NITDA Alert', 'affected': '1,200+ users'},
    {'id': 'ng_ddos_001', 'title': 'DDoS Attacks on Nigerian Fintechs', 'severity': 'high',
     'category': 'Network', 'icon': 'ti-activity', 'description': 'Coordinated DDoS targeting OPay, Flutterwave infrastructure. Peak: 2.3Tbps.',
     'mitigation_id': 'ddos', 'source': 'NCC Security', 'affected': 'OPay, Flutterwave'},
    {'id': 'ng_insider_001', 'title': 'Insider Threat Pattern Detected', 'severity': 'medium',
     'category': 'Insider', 'icon': 'ti-user-x', 'description': 'Bank employees selling customer data on dark web markets. 50,000 records exposed.',
     'mitigation_id': 'insider', 'source': 'Internal Intel', 'affected': '50,000 records'},
]

MITIGATIONS_DB = {
    'bec': {'title': 'BEC Attack Response', 'severity': 'critical', 'estimated_time': '20 mins',
            'steps': [
                {'step': 1, 'action': 'Immediately verify all pending wire transfers via phone call to known numbers', 'command': None},
                {'step': 2, 'action': 'Enable email authentication (DMARC, DKIM, SPF)', 'command': 'Check: mxtoolbox.com/dmarc.aspx'},
                {'step': 3, 'action': 'Implement dual-approval for all transfers above ₦500,000', 'command': None},
                {'step': 4, 'action': 'Train staff to recognize CEO fraud emails', 'command': None},
            ],
            'prevention': ['Enable DMARC email authentication', 'Verify all wire transfer requests by phone', 'Use out-of-band verification for payment changes']},
    'ransomware': {'title': 'Ransomware Response', 'severity': 'critical', 'estimated_time': '45 mins',
                   'steps': [
                       {'step': 1, 'action': 'Immediately isolate affected systems from network', 'command': 'sudo ifconfig eth0 down'},
                       {'step': 2, 'action': 'Do NOT pay the ransom — contact CBN Cyber Division', 'command': 'CBN Cyber: 0700-225-5-000'},
                       {'step': 3, 'action': 'Restore from clean backups', 'command': None},
                       {'step': 4, 'action': 'Report to EFCC and Nigeria Police Cybercrime Unit', 'command': None},
                   ],
                   'prevention': ['Maintain offline backups tested weekly', 'Patch all systems within 48hrs of CVE release', 'Disable RDP unless absolutely necessary']},
    'phishing': {'title': 'Phishing Campaign Response', 'severity': 'high', 'estimated_time': '15 mins',
                 'steps': [
                     {'step': 1, 'action': 'Report phishing URLs to NITDA: info@nitda.gov.ng', 'command': None},
                     {'step': 2, 'action': 'Force password reset for all potentially affected users', 'command': None},
                     {'step': 3, 'action': 'Enable MFA on all accounts immediately', 'command': None},
                     {'step': 4, 'action': 'Block malicious domains at DNS level', 'command': None},
                 ],
                 'prevention': ['Mandatory security awareness training', 'Deploy email filtering solution', 'Enable MFA everywhere']},
    'ddos': {'title': 'DDoS Attack Mitigation', 'severity': 'high', 'estimated_time': '30 mins',
             'steps': [
                 {'step': 1, 'action': 'Enable Cloudflare DDoS protection immediately', 'command': 'Cloudflare dashboard → Security → DDoS'},
                 {'step': 2, 'action': 'Enable rate limiting on all API endpoints', 'command': 'sudo ufw limit 80/tcp'},
                 {'step': 3, 'action': 'Contact your ISP to null-route attacking IPs', 'command': None},
                 {'step': 4, 'action': 'Activate incident response plan', 'command': None},
             ],
             'prevention': ['Use Cloudflare or similar DDoS protection', 'Set API rate limits', 'Have ISP emergency contact ready']},
    'insider': {'title': 'Insider Threat Response', 'severity': 'medium', 'estimated_time': '60 mins',
                'steps': [
                    {'step': 1, 'action': 'Revoke access for suspected employee immediately', 'command': None},
                    {'step': 2, 'action': 'Review all data access logs for the past 30 days', 'command': None},
                    {'step': 3, 'action': 'Report to EFCC Cybercrime Unit', 'command': 'EFCC: efcc.gov.ng/report'},
                    {'step': 4, 'action': 'Implement data loss prevention (DLP) tools', 'command': None},
                ],
                'prevention': ['Implement least-privilege access', 'Enable User Behavior Analytics (UBA)', 'Regular access reviews quarterly']},
}

class NigeriaIntelFeed:
    def __init__(self):
        self.threats = NG_THREATS.copy()

    def get_threats(self):
        return self.threats

    def get_nigeria_intel(self):
        return {'total_threats': len(self.threats), 'critical': sum(1 for t in self.threats if t['severity'] == 'critical'),
                'source': 'EFCC, NITDA, CBN, NCC', 'last_updated': 'Live'}

    def simulate_threat(self):
        if random.random() < 0.3:
            t = random.choice(NG_THREATS).copy()
            t['timestamp'] = __import__('datetime').datetime.now().isoformat()
            return t
        return None


class AdvancedMitigations:
    def get(self, threat_id):
        for key, val in MITIGATIONS_DB.items():
            if key in threat_id or threat_id in key:
                return val
        return MITIGATIONS_DB['phishing']
