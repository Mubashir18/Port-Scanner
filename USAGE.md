# Usage Guide - Simple Port Scanner v2.0

Complete guide to using the Simple Port Scanner in both C++ and Python implementations.

## Table of Contents
1. [C++ Version](#c-version)
2. [Python Version](#python-version)
3. [Output Formats](#output-formats)
4. [Common Use Cases](#common-use-cases)
5. [Tips & Tricks](#tips--tricks)
6. [Troubleshooting](#troubleshooting)

---

## C++ Version

### Command Syntax

```bash
./simplePortScanner [OPTIONS]
```

### Required Arguments

- `-t, --target HOST`: Target IP address or hostname (required)

### Optional Arguments

```
-h, --help              Show help message and exit
-p, --ports RANGE       Ports to scan (default: 1-1024)
                        Format examples:
                        - Single port: "80"
                        - Range: "1-1024"
                        - List: "22,80,443,3306"
                        - Mixed: "1-100,443,8080-8090"

-T, --threads NUM       Number of concurrent threads (default: 200)
                        Range: 1-1000
                        Higher values = faster scan but more load
                        Tip: Use 300-500 for full TCP scans

-o, --timeout SEC       Connection timeout in seconds (default: 3)
                        Range: 1-255
                        Lower = faster but may miss slow services
                        Higher = slower but catches filtered ports

-f, --output FILE       Output file path for results
                        Works with -F flag for format selection

-F, --format FORMAT     Output format (default: table)
                        Options: table, csv, json

-v, --verbose           Enable verbose output for debugging
```

### Examples

#### Basic Scanning

```bash
# Scan most common ports on localhost
./simplePortScanner -t 127.0.0.1

# Scan specific host's common ports
./simplePortScanner -t example.com -p 1-1024

# Quick scan of web ports
./simplePortScanner -t 192.168.1.1 -p 80,443,8080,8443
```

#### Performance Tuning

```bash
# Fast scan with many threads (may generate traffic alarms)
./simplePortScanner -t target.com -p 1-10000 -T 500 -o 2

# Stealthy scan with few threads (slower but less obvious)
./simplePortScanner -t target.com -p 1-65535 -T 50 -o 5

# Balanced scan
./simplePortScanner -t target.com -p 1-65535 -T 250 -o 3
```

#### Output Formats

```bash
# Default table format (colorized terminal output)
./simplePortScanner -t localhost -p 1-1024

# Save to CSV file
./simplePortScanner -t example.com -p 1-1024 -f results.csv -F csv

# Save to JSON file (for tool integration)
./simplePortScanner -t example.com -p 1-1024 -f results.json -F json

# Verbose output for debugging
./simplePortScanner -t localhost -p 22-25 -v
```

#### Advanced Scenarios

```bash
# Full TCP scan with custom settings
./simplePortScanner \
  -t example.com \
  -p 1-65535 \
  -T 400 \
  -o 4 \
  -f full_scan.json \
  -F json \
  -v

# Specific port list with detailed output
./simplePortScanner \
  -t target.local \
  -p 21,22,23,25,53,80,110,143,443,445,3306,5432 \
  -T 100 \
  -f common_ports.csv \
  -F csv
```

### Output Examples

#### Table Format
```
PORT    STATE           SERVICE         BANNER
────────────────────────────────────────────────────────
22      OPEN            SSH             SSH-2.0-OpenSSH_7.4
80      OPEN            HTTP            
443     OPEN            HTTPS           
3306    CLOSED          MySQL           
5432    FILTERED        PostgreSQL      
```

#### CSV Format
```
port,state,service,banner
22,OPEN,SSH,"SSH-2.0-OpenSSH_7.4"
80,OPEN,HTTP,""
443,OPEN,HTTPS,""
3306,CLOSED,MySQL,""
```

#### JSON Format
```json
{
  "metadata": {
    "target": "example.com",
    "start_port": 22,
    "end_port": 443,
    "timestamp": "2026-03-27T14:30:00.000000"
  },
  "results": [
    {
      "port": 22,
      "state": "OPEN",
      "service": "SSH",
      "banner": "SSH-2.0-OpenSSH_7.4"
    }
  ],
  "summary": {
    "open": 2,
    "closed": 420,
    "filtered": 1
  }
}
```

---

## Python Version

### Command Syntax

```bash
python port_scanner.py [OPTIONS]
```

### Required Arguments

- `-t, --target HOST`: Target IP address or hostname (required)

### Optional Arguments

```
-h, --help              Show help message and exit
-p, --ports RANGE       Port range to scan (default: 1-1024)
                        Format: "1-1024" or "22,80,443"
                        Note: Python version works best with ranges

-T, --threads NUM       Number of concurrent threads (default: 100)
                        Python has GIL implications, use 50-150

-o, --timeout SEC       Connection timeout in seconds (default: 2.0)

-f, --output-file FILE  Output file for results

-F, --format FORMAT     Output format (default: table)
                        Options: table, csv, json

-v, --verbose           Enable verbose output
```

### Examples

#### Basic Usage

```bash
# Simple scan of localhost
python port_scanner.py -t 127.0.0.1

# Scan with specific range
python port_scanner.py -t example.com -p 1-10000

# Scan with custom thread count
python port_scanner.py -t target.com -p 1-1024 -T 50
```

#### Output Options

```bash
# Save to CSV
python port_scanner.py -t example.com -p 1-1024 -f results.csv -F csv

# Save to JSON
python port_scanner.py -t example.com -p 1-1024 -f results.json -F json

# Verbose output
python port_scanner.py -t localhost -p 22-80 -v
```

#### Running Directly

```bash
# Make executable (Unix-like systems)
chmod +x port_scanner.py

# Run directly
./port_scanner.py -t target.com -p 1-1024

# Use python3 explicitly
python3 port_scanner.py -t target.com -p 1-1024
```

---

## Output Formats

### Choosing the Right Format

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| **Table** | Interactive use, quick viewing | Easy to read, colored output | Hard to parse, not machine-readable |
| **CSV** | Data analysis, spreadsheets | Excel/Google Sheets compatible | Needs proper escaping, no hierarchical data |
| **JSON** | Tool integration, automation | Machine-readable, structured | Larger file size, needs JSON parser |

### Format Examples

#### Table (Terminal Display)
```
PORT    STATE           SERVICE         BANNER
22      OPEN            SSH             SSH-2.0-OpenSSH_7.4
3306    CLOSED          MySQL           
8080    FILTERED        HTTP-Alt        
```

#### CSV (Data Analysis)
```csv
port,state,service,banner
22,OPEN,SSH,"SSH-2.0-OpenSSH_7.4"
3306,CLOSED,MySQL,""
8080,FILTERED,HTTP-Alt,""
```

#### JSON (Tool Integration)
```json
{
  "summary": {
    "open": 1,
    "closed": 1,
    "filtered": 1
  },
  "results": [
    {"port": 22, "state": "OPEN", "service": "SSH", "banner": "SSH-2.0-OpenSSH_7.4"}
  ]
}
```

---

## Common Use Cases

### 1. Initial Network Reconnaissance

```bash
# Quick scan of common ports on target
./simplePortScanner -t target.com -p 1-1024
```

### 2. Penetration Testing - Full TCP Scan

```bash
# Complete port scan with aggressive threading
./simplePortScanner \
  -t target.com \
  -p 1-65535 \
  -T 400 \
  -o 3 \
  -f full_scan.json \
  -F json
```

### 3. Compliance Audit - Web Servers

```bash
# Check for unwanted web services
./simplePortScanner -t audit-target.local -p 80,443,8080,8443,8888 -f web_audit.csv -F csv
```

### 4. Incident Response - Backdoor Detection

```bash
# Scan for non-standard services that might indicate compromise
./simplePortScanner -t suspect-host.local -p 1-65535 -T 300 -v
```

### 5. Development - Service Verification

```bash
# Verify newly deployed services are accessible
./simplePortScanner -t localhost -p 3000,5000,8000,9000
```

### 6. Network Inventory - Multiple Hosts

```bash
# Scan multiple hosts and save results
for host in 192.168.1.{1..10}; do
  ./simplePortScanner -t $host -p 22,80,443 -f host_$host.csv -F csv
done
```

---

## Tips & Tricks

### Performance Optimization

1. **Adjust Thread Count**
   - Start with 200-300 threads
   - Increase to 400-500 for full scans
   - Decrease to 50-100 for stealth

2. **Timeout Settings**
   - Use 2-3 seconds for WAN targets
   - Use 1-2 seconds for LAN targets
   - Increase to 5+ for unreliable networks

3. **Port Range Strategy**
   - Scan 1-1024 first (well-known ports)
   - Then 1024-10000 (registered ports)
   - Finally 10000-65535 (dynamic ports)

### Output Processing

```bash
# Count open ports from table output
./simplePortScanner -t target.com -p 1-10000 | grep OPEN | wc -l

# Extract open ports from CSV
python3 -c "import csv; print([row['port'] for row in csv.DictReader(open('results.csv')) if row['state'] == 'OPEN'])"

# Parse JSON results
python3 -m json.tool results.json | grep '"port"'
```

### Batch Scanning

```bash
# Scan a subnet
for ip in {1..254}; do
  ./simplePortScanner -t 192.168.1.$ip -p 22,80,443 -f results_$ip.csv -F csv &
done
wait
```

### Combining with Other Tools

```bash
# Export to Nmap for further analysis (requires conversion)
./simplePortScanner -t target.com -p 1-1024 -f results.json -F json

# Feed to vulnerability scanner
cat results.json | jq '.results[] | select(.state == "OPEN") | .service'
```

---

## Understanding Port States

### OPEN
- Service is actively listening on the port
- Connection was accepted by the target
- Indicates potential attack surface
- **Example**: HTTP server on port 80

### CLOSED
- Port is not open, but the host is reachable
- Connection attempt was rejected (RST received)
- Indicates the host is up but service is disabled
- **Example**: Port 445 without SMB service

### FILTERED
- Connection attempt timed out
- A firewall or packet filter appears to be blocking access
- Cannot determine if service is present
- **Example**: Port behind a stateful firewall

---

## Troubleshooting

### Common Issues

#### "Connection refused" errors
```bash
# Check if target is reachable first
ping example.com

# Try with longer timeout
./simplePortScanner -t example.com -p 1-1024 -o 5
```

#### Target resolution fails
```bash
# Verify hostname resolves
nslookup example.com
# or
dig example.com

# Use IP address directly if DNS fails
./simplePortScanner -t 93.184.216.34 -p 1-1024
```

#### Scan takes too long
```bash
# Increase thread count
./simplePortScanner -t target.com -p 1-65535 -T 500

# Reduce timeout (may miss some ports)
./simplePortScanner -t target.com -p 1-65535 -o 1

# Scan in smaller ranges
./simplePortScanner -t target.com -p 1-10000
./simplePortScanner -t target.com -p 10001-20000
```

#### No results or all ports filtered
```bash
# Target may be blocking your IP
# Try with very high timeout
./simplePortScanner -t target.com -p 80 -o 10

# Check if you have network access
ping target.com
```

#### Incomplete output or missing results
```bash
# Use verbose mode for more information
./simplePortScanner -t target.com -p 1-1024 -v

# Save to file instead of viewing in terminal
./simplePortScanner -t target.com -p 1-1024 -f results.txt -F csv
```

---

## Performance Expectations

### Scan Times (Approximate)

| Range | Threads | Time |
|-------|---------|------|
| 1-1024 | 200 | ~5 sec |
| 1-10000 | 300 | ~15 sec |
| 1-65535 | 400-500 | ~120 sec |

*Times vary based on network latency and target responsiveness*

### Network Load

- **Low**: 50 threads, 5+ sec timeout
- **Medium**: 200 threads, 3 sec timeout (default)
- **High**: 500+ threads, <2 sec timeout

---

## Legal and Ethical Considerations

⚠️ **Always remember:**

1. **Only scan systems you own or have explicit permission to test**
2. **Unauthorized port scanning may be illegal in your jurisdiction**
3. **Aggressive scanning can disrupt services or trigger security alerts**
4. **Use appropriate timeout and threading values for your environment**
5. **Log and document all scanning activities for audit purposes**

---

## Getting Help

- **Command Help**: `./simplePortScanner -h` or `python port_scanner.py -h`
- **Documentation**: See README.md and BUILD.md
- **Learning Materials**: See `learn/` directory for detailed explanations
- **Issues**: Report problems with environment details and command used

---

**Happy scanning! 🔍**
