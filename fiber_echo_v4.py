#!/usr/bin/env python3
"""
FIBER-ECHO v4 - INTERNATIONAL EDITION with ISP EVIDENCE
==============================================================================
"Separating bufferbloat from the speed of light, anywhere on Earth"

Now with professional ISP evidence reporting - turn data into proof they can't ignore!
"""

import subprocess
import time
import statistics
import math
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
from collections import defaultdict
import json
import os
import socket

# Try for scientific packages (optional)
try:
    import numpy as np
    from scipy import stats
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


class ISPEvidenceReport:
    """
    Turns raw network data into professional ISP-facing evidence.
    Now integrated directly into FiberEcho!
    """
    
    def __init__(self, fiber_echo_parent=None):
        self.parent = fiber_echo_parent
        self.report_data = {
            'executive_summary': {},
            'technical_findings': [],
            'evidence_logs': [],
            'sla_comparison': {},
            'recommendations': [],
            'metadata': {
                'generated': datetime.now().isoformat(),
                'tool_version': 'FIBER-ECHO v4 - ISP Evidence Edition',
                'analyst': socket.gethostname()
            }
        }
        
        # SLA benchmarks (adjustable per region)
        self.sla_benchmarks = {
            'pacific': {'local': 20, 'isp': 80, 'international': 250, 'bufferbloat': 50},
            'australia': {'local': 10, 'isp': 50, 'international': 200, 'bufferbloat': 50},
            'asia': {'local': 10, 'isp': 40, 'international': 180, 'bufferbloat': 50},
            'europe': {'local': 5, 'isp': 30, 'international': 100, 'bufferbloat': 30},
            'north_america': {'local': 5, 'isp': 30, 'international': 120, 'bufferbloat': 30},
            'south_america': {'local': 15, 'isp': 70, 'international': 220, 'bufferbloat': 50},
            'africa': {'local': 20, 'isp': 100, 'international': 300, 'bufferbloat': 70},
            'middle_east': {'local': 15, 'isp': 80, 'international': 250, 'bufferbloat': 50},
            'global': {'local': 10, 'isp': 50, 'international': 200, 'bufferbloat': 50},
        }
    
    def analyze_for_isp(self, results: Dict, region: str) -> Dict:
        """Analyze results specifically for ISP evidence"""
        
        findings = []
        evidence = []
        benchmarks = self.sla_benchmarks.get(region, self.sla_benchmarks['global'])
        
        for target_name, target_data in results.items():
            if 'error' in target_data:
                continue
            
            rtt_stats = target_data['rtt_stats']
            decomposition = target_data['decomposition']
            
            # Check for excessive latency
            if rtt_stats['min'] > benchmarks['international']:
                findings.append({
                    'severity': 'CRITICAL' if rtt_stats['min'] > benchmarks['international']*1.5 else 'HIGH',
                    'target': target_name,
                    'issue': 'Excessive baseline latency',
                    'measured': f"{rtt_stats['min']:.1f}ms",
                    'threshold': f"{benchmarks['international']}ms",
                    'evidence': f"Min RTT of {rtt_stats['min']:.1f}ms exceeds reasonable {region} transit"
                })
            
            # Bufferbloat detection
            blob = decomposition['queuing_delay_ms']
            if blob > benchmarks['bufferbloat']:
                severity = 'CRITICAL' if blob > benchmarks['bufferbloat']*3 else 'HIGH'
                findings.append({
                    'severity': severity,
                    'target': target_name,
                    'issue': 'Bufferbloat',
                    'measured': f"{blob:.1f}ms",
                    'threshold': f"{benchmarks['bufferbloat']}ms",
                    'evidence': f"Bufferbloat of {blob:.1f}ms indicates router congestion"
                })
            
            # Packet loss
            loss = rtt_stats['loss_percent']
            if loss > 1:
                severity = 'HIGH' if loss > 5 else 'MEDIUM'
                findings.append({
                    'severity': severity,
                    'target': target_name,
                    'issue': 'Packet loss',
                    'measured': f"{loss:.1f}%",
                    'threshold': "1%",
                    'evidence': f"Loss of {loss:.1f}% indicates connection instability"
                })
            
            # Jitter
            jitter = rtt_stats['jitter']
            if jitter > 20:
                findings.append({
                    'severity': 'MEDIUM',
                    'target': target_name,
                    'issue': 'High jitter',
                    'measured': f"{jitter:.1f}ms",
                    'threshold': "20ms",
                    'evidence': f"Jitter of {jitter:.1f}ms affects real-time applications"
                })
            
            # Create evidence log entry
            evidence.append({
                'timestamp': datetime.now().isoformat(),
                'target': target_name,
                'min_rtt_ms': rtt_stats['min'],
                'mean_rtt_ms': rtt_stats['mean'],
                'p95_rtt_ms': rtt_stats['p95'],
                'jitter_ms': jitter,
                'loss_percent': loss,
                'bufferbloat_ms': blob,
                'propagation_ms': decomposition['propagation_rtt_ms'],
                'distance_km': decomposition['distance_km']
            })
        
        self.report_data['technical_findings'] = findings
        self.report_data['evidence_logs'] = evidence
        
        # Generate executive summary
        critical = len([f for f in findings if f['severity'] == 'CRITICAL'])
        high = len([f for f in findings if f['severity'] == 'HIGH'])
        medium = len([f for f in findings if f['severity'] == 'MEDIUM'])
        
        if critical > 0:
            summary = f"🚨 URGENT: {critical} critical issues detected - Your connection is severely degraded"
        elif high > 0:
            summary = f"⚠️ Attention needed: {high} high-priority issues affecting performance"
        elif medium > 0:
            summary = f"📊 Minor issues detected: {medium} medium-priority items to check"
        else:
            summary = "✅ Your connection looks healthy! No issues detected"
        
        self.report_data['executive_summary'] = {
            'critical_issues': critical,
            'high_issues': high,
            'medium_issues': medium,
            'total_issues': len(findings),
            'affected_targets': len(set(f['target'] for f in findings)),
            'summary': summary
        }
        
        return self.report_data
    
    def isolate_responsibility(self, results: Dict) -> Dict:
        """Determine if issue is local network or ISP responsibility using hop analysis"""
        responsibility = {
            'local_network': [],
            'isp_network': [],
            'international': [],
            'unclear': []
        }
        
        for target_name, target_data in results.items():
            if 'error' in target_data or 'hops' not in target_data:
                continue
            
            hops = target_data.get('hops', [])
            if not hops:
                continue
            
            # First hop is usually local router
            if len(hops) >= 2:
                first_hop_delta = hops[1].get('delta', 0)
                if first_hop_delta > 10:
                    responsibility['local_network'].append({
                        'target': target_name,
                        'hop': 1,
                        'ip': hops[1].get('ip', 'unknown'),
                        'delta_ms': first_hop_delta,
                        'evidence': f"Large delay ({first_hop_delta:.1f}ms) at first hop - check your router/WiFi"
                    })
            
            # Look for ISP aggregation point delays (hops 2-4 typically)
            for hop in hops[1:4]:
                if hop.get('delta', 0) > 30:
                    responsibility['isp_network'].append({
                        'target': target_name,
                        'hop': hop.get('hop', 0),
                        'ip': hop.get('ip', 'unknown'),
                        'delta_ms': hop.get('delta', 0),
                        'evidence': f"ISP equipment at hop {hop.get('hop', 0)} adding {hop.get('delta', 0):.1f}ms delay"
                    })
            
            # Check for international delays (beyond hop 4 typically)
            for hop in hops[4:]:
                if hop.get('delta', 0) > 25:
                    responsibility['international'].append({
                        'target': target_name,
                        'hop': hop.get('hop', 0),
                        'ip': hop.get('ip', 'unknown'),
                        'delta_ms': hop.get('delta', 0),
                        'evidence': f"International hop adding {hop.get('delta', 0):.1f}ms (check submarine cables)"
                    })
        
        # Determine primary responsibility
        total_local = len(responsibility['local_network'])
        total_isp = len(responsibility['isp_network'])
        total_intl = len(responsibility['international'])
        
        if total_isp > total_local and total_isp > total_intl:
            primary = "ISP NETWORK"
            explanation = f"Evidence shows {total_isp} delays at ISP aggregation points"
        elif total_local > total_isp and total_local > total_intl:
            primary = "LOCAL NETWORK"
            explanation = f"Found {total_local} issues at first hop - check your router/WiFi setup"
        elif total_intl > total_isp and total_intl > total_local:
            primary = "INTERNATIONAL TRANSIT"
            explanation = "Delays consistent with submarine cable distances - likely normal"
        elif total_isp + total_intl > total_local:
            primary = "MIXED (ISP + INTERNATIONAL)"
            explanation = "Issues found both in ISP network and international transit"
        else:
            primary = "UNCLEAR"
            explanation = "More data needed to pinpoint responsibility"
        
        self.report_data['responsibility'] = {
            'primary': primary,
            'explanation': explanation,
            'local_count': total_local,
            'isp_count': total_isp,
            'international_count': total_intl,
            'details': responsibility
        }
        
        return responsibility
    
    def generate_recommendations(self, region: str, findings: List[Dict]) -> List[str]:
        """Generate region-specific recommendations"""
        recommendations = []
        
        if not findings:
            recommendations.append("✓ Your connection looks healthy! No action needed.")
            recommendations.append("📊 Run tests at different times of day to establish baseline")
            return recommendations
        
        # Check responsibility
        resp = self.report_data.get('responsibility', {})
        primary = resp.get('primary', '')
        
        # Region-specific ISP contact info
        isp_contacts = {
            'pacific': "Digicel Fiji (132) / Vodafone Fiji (888)",
            'australia': "Telstra (13 22 00) / Optus (13 39 37)",
            'asia': "your local ISP support",
            'europe': "your ISP support",
            'north_america': "Comcast (1-800-COMCAST) / AT&T (1-800-288-2020)",
            'south_america': "your local ISP support",
            'africa': "your local ISP support",
            'middle_east': "your local ISP support",
            'global': "your ISP support"
        }
        
        isp_name = isp_contacts.get(region, "your ISP support")
        
        # Check what issues we found
        has_bufferbloat = any('bufferbloat' in f['issue'].lower() for f in findings)
        has_loss = any('loss' in f['issue'].lower() for f in findings)
        has_latency = any('latency' in f['issue'].lower() for f in findings)
        
        if primary == "ISP NETWORK":
            recommendations.append(f"📞 Contact {isp_name} immediately with this evidence")
            recommendations.append("🔧 Request they check your line card at the exchange")
            if has_bufferbloat:
                recommendations.append("📦 Ask them to enable QoS or reduce buffer sizes")
            if has_loss:
                recommendations.append("📉 Request they test the physical line for faults")
            recommendations.append("📈 Ask about upgrading your service tier (may have higher priority)")
        
        elif primary == "LOCAL NETWORK":
            recommendations.append("🔄 Restart your router and modem (unplug for 30 seconds)")
            recommendations.append("📶 Check WiFi interference - try 5GHz instead of 2.4GHz")
            recommendations.append("🔌 Test with wired Ethernet connection to eliminate WiFi")
            recommendations.append("⚙️ Check for router firmware updates")
            if has_bufferbloat:
                recommendations.append("🎮 Enable QoS in your router settings if available")
        
        elif primary == "INTERNATIONAL TRANSIT":
            recommendations.append("🌐 Your international connection appears normal for your location")
            recommendations.append("🕐 Test at different times of day - international congestion varies")
            recommendations.append("🔒 Consider a VPN if specific international services are slow")
        
        elif primary == "MIXED (ISP + INTERNATIONAL)":
            recommendations.append(f"📞 Contact {isp_name} - issues in their network")
            recommendations.append("🌐 International delays are partly expected for your region")
        
        # DeepSeek AI Analysis option
        recommendations.append("")
        recommendations.append("🤖 Want expert AI analysis?")
        recommendations.append("   Run: deepseek-chat < ISP_Evidence_*.txt")
        recommendations.append("   Or paste the report into chat.deepseek.com")
        recommendations.append("   Ask: 'Analyze this ISP evidence report and tell me what to do'")
        
        return recommendations
    
    def generate_text_report(self, results: Dict, region: str, filename: str = None) -> str:
        """Generate plain text report for easy sharing"""
        if not filename:
            filename = f"ISP_Evidence_{region}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Run analysis
        self.analyze_for_isp(results, region)
        self.isolate_responsibility(results)
        findings = self.report_data.get('technical_findings', [])
        recommendations = self.generate_recommendations(region, findings)
        
        region_name = self.parent.region_targets[region]['name'] if self.parent else region
        
        lines = []
        lines.append("=" * 70)
        lines.append("📋 INTERNET SERVICE PROVIDER - EVIDENCE REPORT")
        lines.append("=" * 70)
        lines.append(f"Region: {region_name}")
        lines.append(f"Generated: {self.report_data['metadata']['generated']}")
        lines.append(f"Analyst: {self.report_data['metadata']['analyst']}")
        lines.append("")
        
        # Executive Summary
        lines.append("-" * 70)
        lines.append("📊 EXECUTIVE SUMMARY")
        lines.append("-" * 70)
        exec_sum = self.report_data.get('executive_summary', {})
        lines.append(f"{exec_sum.get('summary', '')}")
        lines.append("")
        lines.append(f"Critical Issues: {exec_sum.get('critical_issues', 0)}")
        lines.append(f"High Issues: {exec_sum.get('high_issues', 0)}")
        lines.append(f"Medium Issues: {exec_sum.get('medium_issues', 0)}")
        lines.append(f"Affected Targets: {exec_sum.get('affected_targets', 0)}")
        lines.append("")
        
        # Responsibility
        lines.append("-" * 70)
        lines.append("🎯 PRIMARY RESPONSIBILITY")
        lines.append("-" * 70)
        resp = self.report_data.get('responsibility', {})
        lines.append(f"Primary: {resp.get('primary', 'Unknown')}")
        lines.append(f"Explanation: {resp.get('explanation', '')}")
        lines.append("")
        lines.append(f"  • Local Network Issues: {resp.get('local_count', 0)}")
        lines.append(f"  • ISP Network Issues: {resp.get('isp_count', 0)}")
        lines.append(f"  • International Issues: {resp.get('international_count', 0)}")
        lines.append("")
        
        # Detailed Findings
        if findings:
            lines.append("-" * 70)
            lines.append("🔍 DETAILED TECHNICAL FINDINGS")
            lines.append("-" * 70)
            
            for f in findings:
                if f['severity'] == 'CRITICAL':
                    emoji = "🔴🔴"
                elif f['severity'] == 'HIGH':
                    emoji = "🟡"
                else:
                    emoji = "🟢"
                
                lines.append(f"{emoji} [{f['severity']}] {f['issue']} - {f['target']}")
                lines.append(f"      Measured: {f['measured']}  (Expected: <{f['threshold']})")
                lines.append(f"      Evidence: {f['evidence']}")
                lines.append("")
        else:
            lines.append("✅ No technical issues detected!")
            lines.append("")
        
        # Evidence Log (Top 5 entries)
        lines.append("-" * 70)
        lines.append("📝 EVIDENCE LOG (Most Recent)")
        lines.append("-" * 70)
        evidence = self.report_data.get('evidence_logs', [])[:5]
        if evidence:
            for e in evidence:
                lines.append(f"  • {e['target']}:")
                lines.append(f"      Min RTT: {e['min_rtt_ms']:.1f}ms | Loss: {e['loss_percent']:.1f}%")
                lines.append(f"      Bufferbloat: {e['bufferbloat_ms']:.1f}ms | Distance: {e['distance_km']:.0f}km")
                lines.append("")
        else:
            lines.append("  No evidence logs recorded")
            lines.append("")
        
        # Recommendations
        lines.append("-" * 70)
        lines.append("💡 RECOMMENDATIONS")
        lines.append("-" * 70)
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. {rec}")
        
        lines.append("")
        lines.append("-" * 70)
        lines.append("📎 HOW TO USE THIS REPORT")
        lines.append("-" * 70)
        lines.append("1. Save this text file to your computer")
        lines.append("2. Email it to your ISP's technical support")
        lines.append("3. Include your account number and location")
        lines.append("4. Ask them to investigate the specific issues")
        lines.append("")
        lines.append("🤖 For AI-powered analysis:")
        lines.append("   • Visit: https://chat.deepseek.com")
        lines.append("   • Upload this file and ask:")
        lines.append("     'Analyze this ISP evidence report and tell me what to do'")
        lines.append("")
        lines.append("=" * 70)
        lines.append("END OF REPORT - Good luck! 🍀")
        lines.append("=" * 70)
        
        report_text = "\n".join(lines)
        
        with open(filename, 'w') as f:
            f.write(report_text)
        
        print(f"\n{self.parent.colors['green'] if self.parent else ''}✅ ISP Evidence Report saved: {filename}{self.parent.colors['end'] if self.parent else ''}")
        return filename


class FiberEchoInternational:
    """
    The complete international package with integrated ISP evidence reporting.
    """
    
    def __init__(self):
        # =====================================================================
        # PHYSICAL CONSTANTS (Universal)
        # =====================================================================
        self.physics = {
            'c_vacuum': 299792.458,           # km/s - speed of light in vacuum
            'fiber_refractive_index': 1.468,   # Standard single-mode fiber
            'copper_refractive_index': 1.77,   # For last-mile copper
            'router_processing_min': 0.2,       # ms - absolute minimum
            'router_processing_max': 2.0,       # ms - worst-case
            'typical_hops_to_internet': 12,     # Global average
        }
        
        # Derived values
        self.physics['fiber_speed'] = (
            self.physics['c_vacuum'] / self.physics['fiber_refractive_index']
        )  # ≈ 204,190 km/s
        
        # =====================================================================
        # REGIONAL TARGETS - For users worldwide
        # =====================================================================
        self.region_targets = {
            'pacific': {
                'name': '🌊 Pacific Islands (Fiji, PNG, Pacific)',
                'targets': {
                    "Cloudflare": "1.1.1.1",
                    "Google": "8.8.8.8",
                    "Quad9": "9.9.9.9",
                    "Fiji_ISP": "10.150.102.13",
                    "Australia": "1.1.1.2",
                    "US_West": "8.8.4.4",
                }
            },
            'australia': {
                'name': '🦘 Australia / New Zealand',
                'targets': {
                    "Cloudflare": "1.1.1.1",
                    "Google": "8.8.8.8",
                    "Quad9": "9.9.9.9",
                    "Telstra": "1.1.1.2",
                    "NZ": "202.46.32.3",
                    "Asia": "1.1.1.2",
                }
            },
            'asia': {
                'name': '🌏 Asia (China, Japan, Korea, SE Asia)',
                'targets': {
                    "Cloudflare": "1.1.1.1",
                    "Google": "8.8.8.8",
                    "China_Baidu": "180.76.76.76",
                    "China_114": "114.114.114.114",
                    "Japan": "1.1.1.2",
                    "Singapore": "1.1.1.2",
                }
            },
            'europe': {
                'name': '🇪🇺 Europe',
                'targets': {
                    "Cloudflare": "1.1.1.1",
                    "Google": "8.8.8.8",
                    "Quad9": "9.9.9.9",
                    "Europe_Yandex": "77.88.8.8",
                    "Germany": "8.8.4.4",
                    "UK": "1.1.1.2",
                }
            },
            'north_america': {
                'name': '🇺🇸 North America',
                'targets': {
                    "Cloudflare": "1.1.1.1",
                    "Google": "8.8.8.8",
                    "Quad9": "9.9.9.9",
                    "US_East": "8.8.4.4",
                    "US_West": "1.1.1.2",
                    "Canada": "208.67.222.222",
                }
            },
            'south_america': {
                'name': '🌎 South America',
                'targets': {
                    "Cloudflare": "1.1.1.1",
                    "Google": "8.8.8.8",
                    "Quad9": "9.9.9.9",
                    "Brazil": "8.8.4.4",
                    "Argentina": "1.1.1.2",
                    "Chile": "208.67.222.222",
                }
            },
            'africa': {
                'name': '🌍 Africa',
                'targets': {
                    "Cloudflare": "1.1.1.1",
                    "Google": "8.8.8.8",
                    "Quad9": "9.9.9.9",
                    "South_Africa": "8.8.4.4",
                    "Nigeria": "1.1.1.2",
                    "Kenya": "208.67.222.222",
                }
            },
            'middle_east': {
                'name': '🕌 Middle East',
                'targets': {
                    "Cloudflare": "1.1.1.1",
                    "Google": "8.8.8.8",
                    "Quad9": "9.9.9.9",
                    "Israel": "8.8.4.4",
                    "UAE": "1.1.1.2",
                    "Saudi": "208.67.222.222",
                }
            },
            'global': {
                'name': '🌐 Global (All regions)',
                'targets': {
                    "Cloudflare": "1.1.1.1",
                    "Google": "8.8.8.8",
                    "Quad9": "9.9.9.9",
                    "Europe": "77.88.8.8",
                    "Asia": "1.1.1.2",
                    "US_West": "8.8.4.4",
                    "Australia": "1.1.1.2",
                }
            }
        }
        
        # Current selected region
        self.current_region = 'global'
        self.targets = self.region_targets['global']['targets']
        
        # =====================================================================
        # ANSI COLORS
        # =====================================================================
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'bold': '\033[1m',
            'dim': '\033[2m',
            'end': '\033[0m'
        }
        
        # Storage
        self.results = {}
        self.alerts = []
        
        # Initialize evidence reporter
        self.evidence_reporter = ISPEvidenceReport(self)
        
        # First run check - create HOW_TO_USE.txt for script kiddies
        self.check_first_run()
    
    def check_first_run(self):
        """Create a helpful guide for first-time users"""
        if not os.path.exists('HOW_TO_USE.txt'):
            with open('HOW_TO_USE.txt', 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("FIBER-ECHO v4 - QUICK START GUIDE FOR SCRIPT KIDDIES\n")
                f.write("=" * 60 + "\n\n")
                f.write("🔰 NEW TO THIS? DON'T PANIC! HERE'S HOW TO USE IT:\n\n")
                f.write("STEP 1: RUN THE TOOL\n")
                f.write("-" * 30 + "\n")
                f.write("python fiber_echo_v4.py\n\n")
                f.write("STEP 2: SELECT YOUR REGION\n")
                f.write("-" * 30 + "\n")
                f.write("• Type the number for your part of the world\n")
                f.write("• Or choose 'Auto-detect' (it's pretty smart)\n\n")
                f.write("STEP 3: CHOOSE 'GLOBAL RADAR' (option 1)\n")
                f.write("-" * 30 + "\n")
                f.write("• This tests all the important servers for your region\n")
                f.write("• Takes about 2 minutes - go grab a coffee ☕\n\n")
                f.write("STEP 4: SAY 'YES' TO THE ISP REPORT\n")
                f.write("-" * 30 + "\n")
                f.write("• When it asks 'Generate ISP evidence report?' type 'y'\n")
                f.write("• It creates a file like: ISP_Evidence_pacific_20240115_143023.txt\n\n")
                f.write("STEP 5: GET AI POWERED ANALYSIS (OPTIONAL BUT AWESOME)\n")
                f.write("-" * 30 + "\n")
                f.write("OPTION A - Use DeepSeek Chat (FREE):\n")
                f.write("   1. Go to https://chat.deepseek.com\n")
                f.write("   2. Upload the .txt report file\n")
                f.write("   3. Ask: 'Analyze this ISP evidence report and tell me what to do'\n\n")
                f.write("OPTION B - Use DeepSeek CLI (if you're fancy):\n")
                f.write("   deepseek-chat < ISP_Evidence_*.txt\n\n")
                f.write("STEP 6: SEND TO YOUR ISP\n")
                f.write("-" * 30 + "\n")
                f.write("• Email the .txt file to your ISP's support\n")
                f.write("• Include your account number\n")
                f.write("• Ask them to fix the specific issues\n\n")
                f.write("=" * 60 + "\n")
                f.write("🤔 WHAT IF I BREAK SOMETHING?\n")
                f.write("=" * 60 + "\n")
                f.write("• You can't break anything - it just reads data!\n")
                f.write("• Ctrl+C stops it at any time\n")
                f.write("• Delete the .txt files if you don't want them\n")
                f.write("• Run it again if you're not sure\n\n")
                f.write("=" * 60 + "\n")
                f.write("🚀 PRO TIPS FOR NOOBS\n")
                f.write("=" * 60 + "\n")
                f.write("• Run it at different times of day (evening = more bufferbloat)\n")
                f.write("• Test both WiFi and wired connections\n")
                f.write("• Share the report on Reddit r/HomeNetworking for help\n")
                f.write("• The bigger the bufferbloat number, the angrier you should be\n\n")
                f.write("Built with ❤️  in Fiji, for script kiddies worldwide!\n")
                f.write("Now stop reading and run the damn thing! 🚀\n")
            
            print(f"\n{self.colors['green']}📝 Created HOW_TO_USE.txt - A guide for script kiddies!{self.colors['end']}")
            print(f"{self.colors['dim']}   (Read it if you're new to this){self.colors['end']}")
    
    # =========================================================================
    # REGION SELECTION
    # =========================================================================
    
    def select_region(self):
        """Let user choose their region"""
        print(f"\n{self.colors['bold']}{self.colors['cyan']}🌍 SELECT YOUR REGION{self.colors['end']}")
        print("=" * 60)
        
        regions = list(self.region_targets.items())
        for i, (key, data) in enumerate(regions, 1):
            print(f"  {i}. {data['name']}")
        
        print(f"  {len(regions)+1}. 🔍 Auto-detect (recommended for noobs)")
        
        choice = input(f"\n{self.colors['green']}Choice{self.colors['end']} [1]: ").strip() or "1"
        
        try:
            idx = int(choice) - 1
            if idx < len(regions):
                self.current_region = regions[idx][0]
            elif choice == str(len(regions) + 1):
                self.auto_detect_region()
                return
            else:
                self.current_region = 'global'
        except:
            self.current_region = 'global'
        
        self.targets = self.region_targets[self.current_region]['targets']
        print(f"\n{self.colors['green']}✓{self.colors['end']} Region set to: {self.region_targets[self.current_region]['name']}")
    
    def auto_detect_region(self):
        """Simple auto-detection based on latency"""
        print(f"\n{self.colors['cyan']}🔍 Auto-detecting region...{self.colors['end']}")
        
        test_targets = {
            'pacific': '103.246.24.1',    # PNG
            'australia': '1.1.1.2',        # Cloudflare AU
            'asia': '180.76.76.76',        # Baidu (China)
            'europe': '77.88.8.8',         # Yandex (Russia)
            'north_america': '8.8.4.4',    # Google US
        }
        
        latencies = {}
        for region, ip in test_targets.items():
            try:
                cmd = ['ping', '-c', '3', '-W', '2', ip]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                
                for line in result.stdout.splitlines():
                    if 'avg' in line or 'min/avg/max' in line:
                        parts = line.split('/')
                        if len(parts) >= 2:
                            avg = float(parts[1])
                            latencies[region] = avg
                            break
            except:
                pass
        
        if latencies:
            best = min(latencies, key=latencies.get)
            print(f"  Best match: {self.region_targets[best]['name']}")
            print(f"  Latency: {latencies[best]:.0f}ms")
            
            confirm = input(f"  Use this region? [Y/n]: ").strip().lower()
            if confirm != 'n':
                self.current_region = best
                self.targets = self.region_targets[best]['targets']
                print(f"{self.colors['green']}✓{self.colors['end']} Region set")
                return
        
        print(f"{self.colors['yellow']}Using global targets{self.colors['end']}")
        self.current_region = 'global'
        self.targets = self.region_targets['global']['targets']
    
    # =========================================================================
    # CORE MEASUREMENT ENGINE
    # =========================================================================
    
    def measure_rtt_statistics(self, target: str, count: int = 100, 
                               interval: float = 0.1, quiet: bool = False) -> Dict[str, float]:
        """Measure RTT statistics with progress bar"""
        if not quiet:
            print(f"\n{self.colors['cyan']}📡 Measuring to {target}{self.colors['end']}")
        
        rtts = []
        lost = 0
        
        for i in range(count):
            if not quiet and i % 10 == 0:
                progress = (i + 1) / count
                bar_width = 30
                bar_filled = int(progress * bar_width)
                bar = '█' * bar_filled + '░' * (bar_width - bar_filled)
                sys.stdout.write(f'\r   [{bar}] {i+1}/{count}')
                sys.stdout.flush()
            
            try:
                cmd = ['ping', '-c', '1', '-W', '1', target]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
                
                if result.returncode == 0 and 'time=' in result.stdout:
                    rtt = float(result.stdout.split('time=')[1].split(' ms')[0])
                    rtts.append(rtt)
                else:
                    lost += 1
            except:
                lost += 1
            
            time.sleep(interval)
        
        if not quiet:
            print()
        
        if not rtts:
            return {'error': 'No responses received'}
        
        rtts.sort()
        n = len(rtts)
        
        stats_dict = {
            'count': n,
            'loss_percent': (lost / count) * 100,
            'min': rtts[0],
            'max': rtts[-1],
            'mean': statistics.mean(rtts),
            'median': rtts[n // 2],
            'std_dev': statistics.stdev(rtts) if n > 1 else 0,
            'p95': rtts[int(n * 0.95)],
            'p99': rtts[int(n * 0.99)],
            'samples': rtts,
        }
        
        # Jitter calculation
        if n > 1:
            jitter_sum = 0
            for i in range(1, n):
                jitter_sum += abs(rtts[i] - rtts[i-1])
            stats_dict['jitter'] = jitter_sum / (n - 1)
        else:
            stats_dict['jitter'] = 0
        
        return stats_dict
    
    # =========================================================================
    # PHYSICAL LAYER DECOMPOSITION
    # =========================================================================
    
    def decompose_rtt(self, rtt_stats: Dict[str, float], 
                      hop_count: Optional[int] = None) -> Dict[str, Any]:
        """Separate RTT into propagation, processing, and queuing"""
        if 'error' in rtt_stats:
            return {'error': rtt_stats['error']}
        
        if hop_count is None:
            hop_count = self.physics['typical_hops_to_internet']
        
        min_processing = hop_count * self.physics['router_processing_min']
        max_processing = hop_count * self.physics['router_processing_max']
        
        propagation_one_way = max(0, (rtt_stats['min'] - min_processing) / 2)
        propagation_rtt = propagation_one_way * 2
        
        processing_variance = max_processing - min_processing
        queuing_delay = max(0, rtt_stats['p99'] - rtt_stats['min'] - processing_variance)
        
        distance_km = propagation_one_way / 1000 * self.physics['fiber_speed']
        distance_error = distance_km * 0.15
        
        # Bufferbloat classification
        if queuing_delay < 10:
            severity = f"{self.colors['green']}NONE{self.colors['end']}"
        elif queuing_delay < 50:
            severity = f"{self.colors['yellow']}MILD{self.colors['end']}"
        elif queuing_delay < 200:
            severity = f"{self.colors['red']}SEVERE{self.colors['end']}"
        else:
            severity = f"{self.colors['red']}{self.colors['bold']}CATASTROPHIC{self.colors['end']}"
            self.alerts.append(f"🔥 CATASTROPHIC bufferbloat: {queuing_delay:.0f}ms")
        
        return {
            'min_rtt_ms': rtt_stats['min'],
            'p99_rtt_ms': rtt_stats['p99'],
            'propagation_rtt_ms': propagation_rtt,
            'propagation_one_way_ms': propagation_one_way,
            'processing_min_ms': min_processing,
            'processing_max_ms': max_processing,
            'queuing_delay_ms': queuing_delay,
            'bufferbloat_ms': queuing_delay,
            'distance_km': distance_km,
            'distance_error_km': distance_error,
            'bufferbloat_severity': severity,
        }
    
    # =========================================================================
    # TRACEROUTE ANALYSIS
    # =========================================================================
    
    def analyze_path_hops(self, target: str) -> Tuple[List[Dict], int]:
        """Hop-by-hop analysis to find delay location"""
        cmd = ['traceroute', '-n', '-q', '1', '-w', '2', target]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except:
            return [], 0
        
        hops = []
        prev_rtt = 0
        
        print(f"\n{self.colors['blue']}🌊 HOP-BY-HOP ANALYSIS{self.colors['end']}")
        print("-" * 65)
        print(f"  {'Hop':<4} {'IP':<15} {'RTT':<8} {'Δ from prev':<10}")
        print("-" * 65)
        
        for line in result.stdout.splitlines()[1:]:
            if '*' in line:
                continue
            
            parts = line.split()
            if len(parts) < 3:
                continue
            
            try:
                hop = int(parts[0])
                ip = parts[1]
                rtt = float(parts[2].replace('ms', '')) if parts[2] != '*' else None
                
                if rtt is None:
                    continue
                
                delta = rtt - prev_rtt if prev_rtt > 0 else 0
                
                # Color code based on delta
                if delta > 50:
                    color = self.colors['red']
                elif delta > 20:
                    color = self.colors['yellow']
                elif delta > 5:
                    color = self.colors['cyan']
                else:
                    color = self.colors['green']
                
                print(f"  {hop:<4} {ip:<15} {rtt:<8.2f} {color}+{delta:<9.2f}{self.colors['end']}")
                
                hops.append({
                    'hop': hop,
                    'ip': ip,
                    'rtt': rtt,
                    'delta': delta,
                })
                
                prev_rtt = rtt
                
            except (ValueError, IndexError):
                continue
        
        return hops, len(hops)
    
    # =========================================================================
    # TARGET ANALYSIS
    # =========================================================================
    
    def analyze_target(self, name: str, ip: str, do_rate_sweep: bool = False) -> Dict:
        """Complete analysis of one target"""
        print(f"\n{self.colors['bold']}{self.colors['purple']}{'='*70}{self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['purple']}🔍 {name} ({ip}){self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['purple']}{'='*70}{self.colors['end']}")
        
        # Step 1: Path analysis
        hops, hop_count = self.analyze_path_hops(ip)
        
        # Step 2: RTT measurement
        rtt_stats = self.measure_rtt_statistics(ip, count=100, interval=0.1)
        
        if 'error' in rtt_stats:
            print(f"{self.colors['red']}Measurement failed{self.colors['end']}")
            return {'error': rtt_stats['error']}
        
        # Step 3: Decomposition
        decomposition = self.decompose_rtt(rtt_stats, hop_count or 12)
        
        # Display results
        self._display_results(rtt_stats, decomposition)
        
        return {
            'name': name,
            'ip': ip,
            'rtt_stats': rtt_stats,
            'decomposition': decomposition,
            'hops': hops,
        }
    
    def _display_results(self, rtt_stats: Dict, decomposition: Dict):
        """Display analysis results"""
        print(f"\n{self.colors['bold']}{self.colors['green']}📋 RESULTS{self.colors['end']}")
        print("=" * 70)
        
        # RTT stats
        print(f"\n{self.colors['cyan']}📊 RTT STATISTICS (ms){self.colors['end']}")
        print(f"  Min:     {rtt_stats['min']:7.2f}   Max:     {rtt_stats['max']:7.2f}")
        print(f"  Mean:    {rtt_stats['mean']:7.2f}   Median:  {rtt_stats['median']:7.2f}")
        print(f"  p95:     {rtt_stats['p95']:7.2f}   p99:     {rtt_stats['p99']:7.2f}")
        print(f"  Jitter:  {rtt_stats['jitter']:7.2f}   Loss:    {rtt_stats['loss_percent']:5.1f}%")
        
        # Decomposition
        print(f"\n{self.colors['yellow']}🔬 PHYSICAL LAYER{self.colors['end']}")
        print(f"  Propagation (one-way): {decomposition['propagation_one_way_ms']:6.2f} ms")
        print(f"  Propagation (RTT):     {decomposition['propagation_rtt_ms']:6.2f} ms")
        print(f"  Bufferbloat:           {decomposition['queuing_delay_ms']:6.2f} ms {decomposition['bufferbloat_severity']}")
        
        # Distance
        print(f"\n{self.colors['purple']}📏 DISTANCE ESTIMATE{self.colors['end']}")
        print(f"  Fiber path: {decomposition['distance_km']:.0f} km ± {decomposition['distance_error_km']:.0f} km")
    
    # =========================================================================
    # GLOBAL RADAR
    # =========================================================================
    
    def global_radar(self):
        """Analyze all targets in current region"""
        region_name = self.region_targets[self.current_region]['name']
        
        print(f"\n{self.colors['bold']}{self.colors['purple']}{'='*70}{self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['purple']}🌍 GLOBAL RADAR - {region_name}{self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['purple']}{'='*70}{self.colors['end']}")
        print(f"Testing {len(self.targets)} targets relevant to your region")
        print(f"This will take about {len(self.targets) * 15} seconds...")
        
        results = {}
        for name, ip in self.targets.items():
            results[name] = self.analyze_target(name, ip, do_rate_sweep=False)
            time.sleep(1)  # Pause between targets
        
        # Summary
        print(f"\n{self.colors['bold']}{self.colors['green']}{'='*70}{self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['green']}📊 REGIONAL SUMMARY{self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['green']}{'='*70}{self.colors['end']}")
        
        print(f"\n{'Target':<15} {'Min RTT':>8} {'Bufferbloat':>12} {'Distance':>10}")
        print("-" * 55)
        
        for name, data in results.items():
            if 'decomposition' in data:
                d = data['decomposition']
                bb = d['queuing_delay_ms']
                bb_color = self.colors['red'] if bb > 100 else self.colors['yellow'] if bb > 30 else self.colors['green']
                print(f"  {name:<15} {d['min_rtt_ms']:8.1f}ms  {bb_color}{bb:10.1f}ms{self.colors['end']} {d['distance_km']:9.0f}km")
        
        if self.alerts:
            print(f"\n{self.colors['red']}🚨 ALERTS{self.colors['end']}")
            for alert in self.alerts[-5:]:
                print(f"  • {alert}")
        
        self.results = results
        
        # ===== INTEGRATED ISP EVIDENCE REPORTING =====
        print(f"\n{self.colors['bold']}{self.colors['cyan']}{'='*70}{self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['cyan']}📋 ISP EVIDENCE REPORT{self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['cyan']}{'='*70}{self.colors['end']}")
        print("Would you like to generate a professional report")
        print("to send to your ISP? This will show them exactly")
        print("what's wrong with your connection.")
        
        generate_report = input(f"\n{self.colors['green']}Generate ISP evidence report? (y/n){self.colors['end']} [y]: ").strip().lower()
        
        if generate_report != 'n':
            filename = self.generate_isp_report()
            
            # Suggest DeepSeek analysis
            print(f"\n{self.colors['cyan']}🤖 Want AI-powered analysis?{self.colors['end']}")
            print("  1. Go to https://chat.deepseek.com")
            print(f"  2. Upload the file: {filename}")
            print("  3. Ask: 'Analyze this ISP evidence report and tell me what to do'")
            print("\n  (It's free and really helpful for noobs!)")
        
        return results
    
    def generate_isp_report(self):
        """Generate ISP evidence report from current results"""
        if not self.results:
            print(f"{self.colors['yellow']}No results to report. Run Global Radar first.{self.colors['end']}")
            return None
        
        print(f"\n{self.colors['cyan']}📊 Generating ISP evidence report...{self.colors['end']}")
        
        # Generate the report
        filename = self.evidence_reporter.generate_text_report(
            self.results, 
            self.current_region
        )
        
        # Show summary
        findings = self.evidence_reporter.report_data.get('technical_findings', [])
        critical = len([f for f in findings if f['severity'] == 'CRITICAL'])
        high = len([f for f in findings if f['severity'] == 'HIGH'])
        
        print(f"\n{self.colors['green']}✓ Report complete!{self.colors['end']}")
        print(f"  Found {critical} critical and {high} high priority issues")
        print(f"\n{self.colors['cyan']}📧 Next steps:{self.colors['end']}")
        print("  1. Email the .txt file to your ISP's technical support")
        print("  2. Include your account number and location")
        print("  3. Ask them to investigate the specific issues")
        print("\n  Example ISP contacts:")
        if self.current_region == 'pacific':
            print("     • Digicel Fiji: 132 or support@digicelfiji.com")
            print("     • Vodafone Fiji: 888 or support@vodafone.com.fj")
        elif self.current_region == 'australia':
            print("     • Telstra: 13 22 00")
            print("     • Optus: 13 39 37")
        elif self.current_region == 'north_america':
            print("     • Comcast: 1-800-COMCAST")
            print("     • AT&T: 1-800-288-2020")
        
        return filename
    
    # =========================================================================
    # MAIN INTERFACE
    # =========================================================================
    
    def run(self):
        """Main menu"""
        print(f"{self.colors['bold']}{self.colors['purple']}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║     FIBER-ECHO v4 - INTERNATIONAL EDITION                   ║")
        print("║     'Separating bufferbloat from the speed of light'        ║")
        print("║                                                              ║")
        print("║     🌊 Pacific   🇦🇺 Australia   🌏 Asia   🇪🇺 Europe        ║")
        print("║     🇺🇸 N America 🌎 S America   🌍 Africa  🕌 Middle East   ║")
        print("║                                                              ║")
        print("║     🆕 NEW: ISP Evidence Reports + DeepSeek AI Analysis     ║")
        print("║     Built with ❤️  in Fiji, for script kiddies worldwide!   ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{self.colors['end']}")
        
        # Check if first run - show quick tip
        if os.path.exists('HOW_TO_USE.txt'):
            print(f"{self.colors['dim']}📖 New? Check HOW_TO_USE.txt for help{self.colors['end']}")
        
        # Select region first
        self.select_region()
        
        while True:
            print(f"\n{self.colors['cyan']}{'='*50}{self.colors['end']}")
            print(f"{self.colors['bold']}{self.colors['cyan']}📋 MAIN MENU{self.colors['end']}")
            print(f"{self.colors['cyan']}{'='*50}{self.colors['end']}")
            print(f"  Current region: {self.colors['bold']}{self.region_targets[self.current_region]['name']}{self.colors['end']}")
            print()
            print("  1. 🌍 Global radar (test all targets in your region)")
            print("  2. 🎯 Single target test")
            print("  3. 🔄 Change region")
            print("  4. 📊 Generate ISP evidence report (from last test)")
            print("  5. 📖 Show quick guide (HOW_TO_USE.txt)")
            print("  6. 🚪 Exit")
            
            choice = input(f"\n{self.colors['green']}Choice{self.colors['end']} [1]: ").strip() or "1"
            
            if choice == "6":
                print(f"\n{self.colors['purple']}Aloha! May your packets always find the shortest path.{self.colors['end']}")
                print(f"{self.colors['dim']}And remember - bufferbloat is the enemy! 🎯{self.colors['end']}")
                break
            
            elif choice == "1":
                self.global_radar()
            
            elif choice == "2":
                ip = input("Enter IP or domain: ").strip()
                if ip:
                    name = input("Name [Custom]: ").strip() or "Custom"
                    result = self.analyze_target(name, ip)
                    self.results[name] = result
                    
                    # Ask if they want ISP report for this target
                    if input(f"\n{self.colors['green']}Generate ISP report from this test? (y/n){self.colors['end']} [n]: ").strip().lower() == 'y':
                        self.generate_isp_report()
                else:
                    print("No target entered")
            
            elif choice == "3":
                self.select_region()
            
            elif choice == "4":
                self.generate_isp_report()
            
            elif choice == "5":
                if os.path.exists('HOW_TO_USE.txt'):
                    print(f"\n{self.colors['cyan']}📖 QUICK GUIDE:{self.colors['end']}")
                    with open('HOW_TO_USE.txt', 'r') as f:
                        print(f.read())
                else:
                    self.check_first_run()


def main():
    """Entry point"""
    try:
        tool = FiberEchoInternational()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n\n{colors['yellow']}Interrupted - See you next time!{colors['end']}")
    except Exception as e:
        print(f"\n{colors['red']}Error: {e}{colors['end']}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
