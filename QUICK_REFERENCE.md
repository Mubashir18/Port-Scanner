# Port Scanner v3.0 - Quick Reference

## Installation & Setup
```bash
# No additional dependencies required (Python 3.6+)
python port_scanner.py -h  # Show help
```

## Most Common Commands

### 1. Quick Scan (< 5 seconds)
```bash
python port_scanner.py -t target --profile quick
```

### 2. Standard Audit (30 seconds)
```bash
python port_scanner.py -t target --profile normal
```

### 3. Complete Audit (5-15 minutes)
```bash
python port_scanner.py -t target --profile thorough
```

### 4. Stealth Scan (IDS Evasion)
```bash
python port_scanner.py -t target --profile paranoid --rate 0.5
```

### 5. Professional HTML Report
```bash
python port_scanner.py -t target -p 1-1024 -f report.html -F html
```

### 6. Multiple Targets
```bash
python port_scanner.py -t 192.168.1.1,192.168.1.2,192.168.1.3 -p 1-1024
```

### 7. With Service Detection
```bash
python port_scanner.py -t target --profile normal --fingerprint --dns
```

### 8. Database Integration (CSV)
```bash
python port_scanner.py -t target -p 1-1024 -f results.csv -F csv
```

### 9. Tool Integration (JSON)
```bash
python port_scanner.py -t target -p 1-1024 -f results.json -F json
```

### 10. Smart Filtering
```bash
# Only scan web ports
python port_scanner.py -t target -p 1-65535 -W 80,443,8080,8443,3000

# All ports except noisy ones
python port_scanner.py -t target -p 1-65535 -B 137,138,139,445
```

## Option Quick Reference

| Option | Purpose | Example |
|--------|---------|---------|
| `-t` | Target(s) | `-t 192.168.1.1` or `-t 192.168.1.1,192.168.1.2` |
| `-p` | Ports | `-p 1-1024` or `-p 22,80,443` |
| `-P` | Profile | `-P quick/normal/thorough/paranoid` |
| `--rate` | Slow scan (IDS evasion) | `--rate 0.5` (500ms delay) |
| `-f` | Output file | `-f results.csv` |
| `-F` | Output format | `-F table/csv/json/html` |
| `-W` | Whitelist ports | `-W 80,443,22` (ONLY these) |
| `-B` | Blacklist ports | `-B 137,138,139` (skip these) |
| `--dns` | Reverse DNS | `--dns` (hostname lookup) |
| `--fingerprint` | Service detection | `--fingerprint` (version info) |
| `-T` | Thread count | `-T 50` (default: 100) |
| `-o` | Timeout | `-o 1.0` (seconds, default: 2.0) |
| `-v` | Verbose | `-v` (more details) |

## Output Formats

### Table (Terminal)
```
PORT    STATE           SERVICE         BANNER
80      OPEN            HTTP            Apache 2.4.41
443     CLOSED          HTTPS
22      CLOSED          SSH
```

### CSV (Spreadsheet)
```
target,port,state,service,banner,hostname
192.168.1.1,80,OPEN,HTTP,Apache 2.4,webserver.local
192.168.1.1,443,CLOSED,HTTPS,,webserver.local
```

### JSON (API/Automation)
```json
{
  "metadata": {
    "targets": ["192.168.1.1"],
    "timestamp": "2024-01-30T15:45:23"
  },
  "results": {
    "192.168.1.1": {
      "open": 2,
      "closed": 998,
      "ports": [...]
    }
  }
}
```

### HTML (Reports)
Professional HTML with styling, charts, color-coded ports

## Scan Profile Comparison

| Profile | Speed | Stealth | Accuracy | Best For |
|---------|-------|---------|----------|----------|
| quick | ⚡⚡⚡ | Low | Medium | Initial recon |
| normal | ⚡⚡ | Medium | High | Security audits |
| thorough | ⚡ | Medium | Very High | Complete audits |
| paranoid | 🐢 | Very High | Medium | Avoiding detection |

## Performance Tips

1. **Faster scans**: `-P quick`, reduce timeout, increase threads
2. **Quieter scans**: `--profile paranoid`, `--rate 0.5`, reduce threads
3. **Avoid noise**: `-B 137,138,139,445` (NetBIOS and SMB)
4. **Target specific**: `-W 22,80,443` (only web/SSH)
5. **Batch results**: Use CSV/JSON for processing 1000+ targets

## Troubleshooting

### Scan too slow?
- Use `-P quick` profile
- Reduce timeout: `-o 0.5`
- Increase threads: `-T 200`

### Getting too many timeouts?
- Increase timeout: `-o 3.0`
- Use normal profile instead of quick
- Reduce thread count: `-T 50`

### IDS/Firewall blocking scans?
- Use paranoid profile: `-P paranoid`
- Add rate limiting: `--rate 0.5`
- Increase timeout: `-o 5.0`

### Need port 80 open for test?
- Start a simple server: `python -m http.server 80` (needs admin)
- Or: `python -m http.server 8080` (scan with `-W 8080`)

## Examples Cheat Sheet

```bash
# Scan localhost quickly
python port_scanner.py -t 127.0.0.1 -P quick

# Scan network, save HTML report
python port_scanner.py -t 192.168.1.1 -p 1-1024 -f report.html -F html

# Scan 3 servers, export CSV for analysis
python port_scanner.py -t web.local,db.local,app.local -p 1-1024 -f results.csv -F csv

# Stealthy scan avoiding IDS
python port_scanner.py -t target -P paranoid --rate 1.0 --dns --fingerprint

# Only check web servers
python port_scanner.py -t target -p 1-65535 -W 80,443,8080,8443,3000 -f web_ports.csv -F csv
```

---

**Getting more help?** Run `python port_scanner.py -h` for full documentation
