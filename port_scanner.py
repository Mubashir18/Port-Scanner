#!/usr/bin/env python3
"""
Simple Port Scanner v3.0
A network reconnaissance tool for identifying open TCP ports on a target host.
Supports multiple output formats, scan profiles, rate limiting, and advanced filtering.
"""

import socket
import sys
import argparse
import json
import csv
import threading
import time
import html
import socket as socket_lib
from datetime import datetime
from queue import Queue, Empty
from typing import Tuple, List, Dict, Set
from urllib.parse import quote

# ANSI color codes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'

# Scan profiles for different speed/accuracy tradeoffs
SCAN_PROFILES = {
    'quick': {
        'description': 'Fast scan of 100 common ports',
        'port_count': 100,
        'timeout': 0.5,
        'threads': 50,
        'rate_limit': 0.001,
    },
    'normal': {
        'description': 'Balanced scan of 1000 common ports',
        'port_count': 1000,
        'timeout': 1.0,
        'threads': 100,
        'rate_limit': 0.005,
    },
    'thorough': {
        'description': 'Complete scan of all 65535 ports',
        'port_count': 65535,
        'timeout': 2.0,
        'threads': 50,
        'rate_limit': 0.01,
    },
    'paranoid': {
        'description': 'Slow scan for IDS evasion',
        'port_count': 1000,
        'timeout': 3.0,
        'threads': 5,
        'rate_limit': 0.5,
    }
}

# Well-known ports reference
WELL_KNOWN_PORTS = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    445: 'SMB',
    3306: 'MySQL',
    3389: 'RDP',
    5432: 'PostgreSQL',
    5984: 'CouchDB',
    6379: 'Redis',
    8080: 'HTTP-Alt',
    27017: 'MongoDB',
}

class PortScanner:
    """Concurrent TCP port scanner with advanced features"""
    
    def __init__(self, targets: List[str], start_port: int = 1, end_port: int = 1024,
                 threads: int = 100, timeout: float = 2.0, rate_limit: float = 0.0,
                 whitelist: Set[int] = None, blacklist: Set[int] = None,
                 enable_dns: bool = False, enable_fingerprint: bool = False):
        """
        Initialize scanner
        
        Args:
            targets: List of target IPs/hostnames
            start_port: Start port number
            end_port: End port number
            threads: Number of worker threads
            timeout: Connection timeout in seconds
            rate_limit: Delay between probes (seconds)
            whitelist: Set of ports to scan (if set, ONLY these ports scanned)
            blacklist: Set of ports to skip
            enable_dns: Enable reverse DNS lookup
            enable_fingerprint: Enable service fingerprinting
        """
        self.targets = targets
        self.start_port = max(1, start_port)
        self.end_port = min(65535, end_port)
        self.threads = max(1, min(threads, 256))
        self.timeout = max(0.1, timeout)
        self.rate_limit = rate_limit
        self.whitelist = whitelist
        self.blacklist = blacklist or set()
        self.enable_dns = enable_dns
        self.enable_fingerprint = enable_fingerprint
        self.port_queue = Queue()
        self.results = {}  # {target: {'open': [], 'closed': [], 'filtered': []}}
        self.lock = threading.Lock()
        self.scanned_count = 0
        self.total_count = 0
        self.start_time = None
        
        # Initialize results dict for each target
        for target in targets:
            self.results[target] = {'open': [], 'closed': [], 'filtered': []}
    
    def get_service_name(self, port: int) -> str:
        """Get service name for a port"""
        return WELL_KNOWN_PORTS.get(port, 'Unknown')
    
    def get_reverse_dns(self, ip: str) -> str:
        """Perform reverse DNS lookup"""
        if not self.enable_dns:
            return ip
        
        try:
            hostname, _, _ = socket_lib.gethostbyaddr(ip)
            return hostname
        except (socket_lib.herror, socket_lib.gaierror):
            return ip
    
    def fingerprint_service(self, ip: str, port: int, banner: str) -> str:
        """Attempt to fingerprint service version"""
        if not self.enable_fingerprint or not banner:
            return banner
        
        # SSH detection
        if banner.startswith('SSH'):
            return banner  # SSH already provides version
        
        # HTTP detection
        if port in [80, 8080, 8000, 3000]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                sock.connect((ip, port))
                sock.send(b'GET / HTTP/1.0\r\nHost: scanner\r\nConnection: close\r\n\r\n')
                response = sock.recv(512).decode('utf-8', errors='ignore')
                sock.close()
                
                # Extract Server header
                for line in response.split('\r\n'):
                    if line.startswith('Server:'):
                        return line.split(':', 1)[1].strip()
            except:
                pass
        
        # SMTP detection
        if port in [25, 587, 465]:
            if 'SMTP' in banner or 'smtp' in banner.lower():
                return banner
        
        # FTP detection
        if port == 21:
            if 'ProFTPD' in banner or 'vsftpd' in banner or 'FileZilla' in banner:
                return banner
        
        return banner
    
    def scan_port(self, target: str, port: int) -> Tuple[int, str, str]:
        """
        Scan a single port
        Returns: (port, state, banner)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            try:
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    # Port is OPEN, try to grab banner
                    banner = ""
                    try:
                        banner = sock.recv(256).decode('utf-8', errors='ignore')
                    except (socket.timeout, socket.error):
                        pass
                    
                    # Fingerprint if enabled
                    banner = self.fingerprint_service(target, port, banner[:100])
                    
                    return port, 'OPEN', banner
                else:
                    # Port is CLOSED
                    return port, 'CLOSED', ''
            except socket.timeout:
                # Port is FILTERED (timeout)
                return port, 'FILTERED', ''
            finally:
                sock.close()
        except socket.gaierror:
            raise Exception(f"Hostname could not be resolved: {target}")
        except socket.error as e:
            raise Exception(f"Connection error: {str(e)}")
    
    def worker(self, target: str):
        """Worker thread that processes ports from queue"""
        while True:
            try:
                port = self.port_queue.get(timeout=1)
            except Empty:
                break
            
            # Apply rate limiting
            if self.rate_limit > 0:
                time.sleep(self.rate_limit)
            
            try:
                port, state, banner = self.scan_port(target, port)
                
                # Perform reverse DNS if needed
                hostname = self.get_reverse_dns(target) if self.enable_dns else target
                
                with self.lock:
                    self.results[target][state.lower()].append({
                        'port': port,
                        'state': state,
                        'service': self.get_service_name(port),
                        'banner': banner,
                        'hostname': hostname
                    })
                    self.scanned_count += 1
            except Exception as e:
                print(f"\nError scanning port {port}: {e}", file=sys.stderr)
            finally:
                self.port_queue.task_done()
    
    def print_progress(self):
        """Print progress indicator"""
        if self.total_count > 0:
            percent = (self.scanned_count / self.total_count) * 100
            filled = int(percent / 5)
            bar = '█' * filled + '░' * (20 - filled)
            elapsed = time.time() - self.start_time
            rate = self.scanned_count / elapsed if elapsed > 0 else 0
            eta = (self.total_count - self.scanned_count) / rate if rate > 0 else 0
            
            sys.stdout.write(f'\rProgress: [{bar}] {percent:.1f}% ({self.scanned_count}/{self.total_count}) ETA: {int(eta)}s')
            sys.stdout.flush()
    
    def start_scan(self):
        """Start the port scanning process"""
        self.start_time = time.time()
        
        # Build port list with filtering
        if self.whitelist:
            # Only scan whitelisted ports
            ports_to_scan = [p for p in self.whitelist if self.start_port <= p <= self.end_port]
        else:
            # Scan range minus blacklist
            ports_to_scan = [p for p in range(self.start_port, self.end_port + 1) if p not in self.blacklist]
        
        self.total_count = len(ports_to_scan) * len(self.targets)
        
        # Fill queue with ports for each target
        for target in self.targets:
            for port in ports_to_scan:
                self.port_queue.put(port)
        
        # Create and start worker threads (for each target)
        threads = []
        for target in self.targets:
            for _ in range(min(self.threads, max(1, len(ports_to_scan) // 10))):
                t = threading.Thread(target=self.worker, args=(target,), daemon=True)
                t.start()
                threads.append(t)
        
        # Wait for all ports to be scanned
        while not self.port_queue.empty():
            self.print_progress()
            time.sleep(0.1)
        
        self.port_queue.join()
        
        # Wait for all threads to complete
        for t in threads:
            t.join(timeout=5)
        
        print()  # New line after progress bar

def print_banner():
    """Print application banner"""
    banner = f"""
    {CYAN}╔════════════════════════════════════════════════════════╗
    ║      Simple Port Scanner v2.0 (Python Edition)         ║
    ║      Asynchronous TCP Reconnaissance Tool              ║
    ╚════════════════════════════════════════════════════════╝{RESET}
    """
    print(banner)

def print_results_table(scanner: PortScanner):
    """Print results in table format for all targets"""
    for target in scanner.targets:
        print(f"\n{CYAN}═══ Results for {target} ═══{RESET}")
        print(f"{CYAN}PORT\tSTATE\t\tSERVICE\t\tBANNER{RESET}")
        print("─" * 100)
        
        # Sort results
        all_results = scanner.results[target]['open'] + scanner.results[target]['closed'] + scanner.results[target]['filtered']
        all_results.sort(key=lambda x: x['port'])
        
        for result in all_results:
            port = result['port']
            state = result['state']
            service = result['service']
            banner = result['banner'][:30] if result['banner'] else ''
            
            if state == 'OPEN':
                color = GREEN
            elif state == 'CLOSED':
                color = RED
            else:
                color = YELLOW
            
            print(f"{port}\t{color}{state}{RESET}\t\t{service}\t\t{banner}")

def print_results_csv(scanner: PortScanner, output_file: str):
    """Save results in CSV format for all targets"""
    all_results = []
    
    for target in scanner.targets:
        for result in (scanner.results[target]['open'] + scanner.results[target]['closed'] + scanner.results[target]['filtered']):
            result['target'] = target
            all_results.append(result)
    
    all_results.sort(key=lambda x: (x['target'], x['port']))
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['target', 'port', 'state', 'service', 'banner', 'hostname'])
        writer.writeheader()
        writer.writerows(all_results)
    
    print(f"✓ Results saved to {output_file}")

def print_results_json(scanner: PortScanner, output_file: str):
    """Save results in JSON format for all targets"""
    output = {
        'metadata': {
            'targets': scanner.targets,
            'start_port': scanner.start_port,
            'end_port': scanner.end_port,
            'timestamp': datetime.now().isoformat()
        },
        'results': {}
    }
    
    for target in scanner.targets:
        all_results = scanner.results[target]['open'] + scanner.results[target]['closed'] + scanner.results[target]['filtered']
        all_results.sort(key=lambda x: x['port'])
        
        output['results'][target] = {
            'open': len(scanner.results[target]['open']),
            'closed': len(scanner.results[target]['closed']),
            'filtered': len(scanner.results[target]['filtered']),
            'ports': all_results
        }
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✓ Results saved to {output_file}")

def print_results_html(scanner: PortScanner, output_file: str):
    """Save results in HTML format for all targets"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Port Scan Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        h2 {
            color: #764ba2;
            margin-top: 30px;
        }
        .metadata {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .metadata p {
            margin: 5px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background: #f9f9f9;
        }
        .open { color: #27ae60; font-weight: bold; }
        .closed { color: #e74c3c; font-weight: bold; }
        .filtered { color: #f39c12; font-weight: bold; }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-box {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
        }
        .stat-box h3 {
            margin: 0;
            color: #667eea;
        }
        .stat-box .number {
            font-size: 28px;
            font-weight: bold;
            margin: 10px 0 0 0;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Port Scan Report</h1>
        
        <div class="metadata">
            <p><strong>Scan Timestamp:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            <p><strong>Targets:</strong> """ + ', '.join(scanner.targets) + """</p>
            <p><strong>Port Range:</strong> """ + str(scanner.start_port) + """ - """ + str(scanner.end_port) + """</p>
        </div>
"""
    
    # Add results for each target
    for target in scanner.targets:
        open_ports = len(scanner.results[target]['open'])
        closed_ports = len(scanner.results[target]['closed'])
        filtered_ports = len(scanner.results[target]['filtered'])
        total = open_ports + closed_ports + filtered_ports
        
        html_content += f"""
        <h2>Target: {html.escape(target)}</h2>
        
        <div class="summary">
            <div class="stat-box">
                <h3>Open Ports</h3>
                <div class="number open">{open_ports}</div>
            </div>
            <div class="stat-box">
                <h3>Closed Ports</h3>
                <div class="number closed">{closed_ports}</div>
            </div>
            <div class="stat-box">
                <h3>Filtered Ports</h3>
                <div class="number filtered">{filtered_ports}</div>
            </div>
            <div class="stat-box">
                <h3>Total Scanned</h3>
                <div class="number">{total}</div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Port</th>
                    <th>State</th>
                    <th>Service</th>
                    <th>Banner</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add open ports
        all_results = scanner.results[target]['open'] + scanner.results[target]['closed'] + scanner.results[target]['filtered']
        all_results.sort(key=lambda x: x['port'])
        
        for result in all_results:
            state_class = result['state'].lower()
            html_content += f"""                <tr>
                    <td>{result['port']}</td>
                    <td><span class="{state_class}">{result['state']}</span></td>
                    <td>{html.escape(result['service'])}</td>
                    <td>{html.escape(result['banner'][:50])}</td>
                </tr>
"""
        
        html_content += """            </tbody>
        </table>
"""
    
    html_content += """
        <div class="footer">
            <p>Generated by Simple Port Scanner v3.0 | Educational & Authorized Testing Only</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Results saved to {output_file}")

def print_statistics(scanner: PortScanner, elapsed_time: float):
    """Print scan statistics"""
    total_ports_per_target = scanner.end_port - scanner.start_port + 1
    
    print(f"\n{'─' * 100}")
    print(f"SCAN STATISTICS:")
    print(f"{'─' * 100}")
    
    total_open = 0
    total_closed = 0
    total_filtered = 0
    
    for target in scanner.targets:
        open_ports = len(scanner.results[target]['open'])
        closed_ports = len(scanner.results[target]['closed'])
        filtered_ports = len(scanner.results[target]['filtered'])
        
        total_open += open_ports
        total_closed += closed_ports
        total_filtered += filtered_ports
        
        print(f"\nTarget: {target}")
        print(f"  Ports Scanned: {total_ports_per_target}")
        print(f"  Open Ports:    {GREEN}{open_ports}{RESET}")
        print(f"  Closed Ports:  {RED}{closed_ports}{RESET}")
        print(f"  Filtered Ports: {YELLOW}{filtered_ports}{RESET}")
    
    print(f"\n{'─' * 100}")
    print(f"TOTALS (All Targets):")
    print(f"  Open Ports:    {GREEN}{total_open}{RESET}")
    print(f"  Closed Ports:  {RED}{total_closed}{RESET}")
    print(f"  Filtered Ports: {YELLOW}{total_filtered}{RESET}")
    print(f"  Scan Time:     {elapsed_time:.2f} seconds")
    print(f"  Rate:          {scanner.scanned_count / elapsed_time:.1f} ports/sec")
    print(f"{'─' * 100}\n")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='TCP port scanner for network reconnaissance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  Scan common ports on localhost:
    python port_scanner.py -t 127.0.0.1 -p 1-1024
  
  Scan multiple targets:
    python port_scanner.py -t 192.168.1.1,192.168.1.2 -p 22,80,443,3306
  
  Quick scan profile:
    python port_scanner.py -t example.com --profile quick
  
  Scan with DNS and service fingerprinting:
    python port_scanner.py -t example.com -p 1-1024 --dns --fingerprint
  
  Full TCP port scan with HTML report:
    python port_scanner.py -t example.com -p 1-65535 -f report.html -F html
  
  Blacklist noisy ports, enable rate limiting (IDS evasion):
    python port_scanner.py -t target.com -p 1-1024 --blacklist 137,138,139 --rate 0.1
  
  Paranoid slow scan for stealth:
    python port_scanner.py -t target.com --profile paranoid

DISCLAIMER:
  Scan only systems you own or have explicit permission to test.
  Unauthorized port scanning may be illegal in your jurisdiction.
        '''
    )
    
    parser.add_argument('-t', '--target', required=True, 
                        help='Target IP address, hostname, or comma-separated list of targets')
    parser.add_argument('-p', '--ports', default='1-1024', 
                        help='Port range (e.g., "1-1024") or specific ports (e.g., "22,80,443")')
    parser.add_argument('-P', '--profile', choices=list(SCAN_PROFILES.keys()), 
                        help='Scan profile (quick/normal/thorough/paranoid)')
    parser.add_argument('-T', '--threads', type=int, default=100,
                        help='Number of concurrent threads (default: 100)')
    parser.add_argument('-o', '--timeout', type=float, default=2.0,
                        help='Connection timeout in seconds (default: 2.0)')
    parser.add_argument('--rate', type=float, default=0.0,
                        help='Rate limiting: delay between probes in seconds (default: 0.0)')
    parser.add_argument('-f', '--output-file', help='Output file for results')
    parser.add_argument('-F', '--format', choices=['table', 'csv', 'json', 'html'], default='table',
                        help='Output format (default: table)')
    parser.add_argument('-W', '--whitelist', help='Whitelist: comma-separated specific ports to scan ONLY')
    parser.add_argument('-B', '--blacklist', help='Blacklist: comma-separated ports to skip')
    parser.add_argument('--dns', action='store_true', help='Enable reverse DNS lookup')
    parser.add_argument('--fingerprint', action='store_true', help='Enable service fingerprinting')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Parse targets (comma-separated)
    targets = [t.strip() for t in args.target.split(',')]
    
    # Handle profile
    if args.profile:
        profile = SCAN_PROFILES[args.profile]
        threads = profile['threads']
        timeout = profile['timeout']
        rate_limit = profile['rate_limit']
        start_port = 1
        end_port = min(profile['port_count'], 65535)
        print(f"Using profile: {args.profile} ({profile['description']})")
    else:
        threads = args.threads
        timeout = args.timeout
        rate_limit = args.rate
        
        # Parse port specification
        if '-' in args.ports:
            try:
                start, end = args.ports.split('-')
                start_port = int(start)
                end_port = int(end)
            except ValueError:
                print(f"{RED}Error: Invalid port specification{RESET}")
                sys.exit(1)
        else:
            # For specific ports
            try:
                ports = list(map(int, args.ports.split(',')))
                start_port = min(ports)
                end_port = max(ports)
            except ValueError:
                print(f"{RED}Error: Invalid port specification{RESET}")
                sys.exit(1)
    
    # Parse whitelist and blacklist
    whitelist = None
    blacklist = set()
    
    if args.whitelist:
        try:
            whitelist = set(map(int, args.whitelist.split(',')))
        except ValueError:
            print(f"{RED}Error: Invalid whitelist specification{RESET}")
            sys.exit(1)
    
    if args.blacklist:
        try:
            blacklist = set(map(int, args.blacklist.split(',')))
        except ValueError:
            print(f"{RED}Error: Invalid blacklist specification{RESET}")
            sys.exit(1)
    
    print(f"Targets:   {', '.join(targets)}")
    print(f"Ports:     {start_port}-{end_port}")
    print(f"Threads:   {threads}")
    print(f"Timeout:   {timeout}s")
    if rate_limit > 0:
        print(f"Rate Limit: {rate_limit}s/probe")
    print(f"Format:    {args.format}")
    if args.whitelist:
        print(f"Whitelist: {args.whitelist}")
    if args.blacklist:
        print(f"Blacklist: {args.blacklist}")
    if args.dns:
        print(f"DNS:       Enabled")
    if args.fingerprint:
        print(f"Fingerprint: Enabled")
    if args.output_file:
        print(f"Output:    {args.output_file}")
    print("─" * 100)
    
    try:
        # Resolve hostnames
        resolved_targets = []
        for target in targets:
            try:
                ip = socket.gethostbyname(target)
                resolved_targets.append(ip)
                if target != ip and args.verbose:
                    print(f"✓ Resolved {target} to {ip}")
            except socket.gaierror:
                print(f"{RED}Error: Could not resolve hostname '{target}'{RESET}", file=sys.stderr)
                sys.exit(1)
        
        # Create scanner and start scan
        scanner = PortScanner(
            resolved_targets, 
            start_port, 
            end_port, 
            threads, 
            timeout, 
            rate_limit,
            whitelist,
            blacklist,
            args.dns,
            args.fingerprint
        )
        
        print(f"\n{CYAN}Starting scan...{RESET}\n")
        
        start_time = time.time()
        scanner.start_scan()
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Print results based on format
        if args.format == 'table':
            print_results_table(scanner)
        elif args.format == 'csv' and args.output_file:
            print_results_csv(scanner, args.output_file)
        elif args.format == 'json' and args.output_file:
            print_results_json(scanner, args.output_file)
        elif args.format == 'html' and args.output_file:
            print_results_html(scanner, args.output_file)
        elif args.output_file and args.format != 'table':
            print(f"{RED}Error: Output file requires -F/--format option with -f flag{RESET}")
            sys.exit(1)
        
        print_statistics(scanner, elapsed)
        
    except socket.gaierror as e:
        print(f"{RED}Error: {str(e)}{RESET}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Scan interrupted by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
