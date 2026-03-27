```
██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
```

# Simple Port Scanner v2.0

> **Asynchronous TCP port scanner** built with C++ and Boost.Asio for high-concurrency network reconnaissance.

High-performance port scanner for security audits, penetration testing, and network reconnaissance. Available in both C++ (high-performance) and Python (ease of use).

## 🎯 Features

- ✅ **Asynchronous I/O**: Uses Boost.Asio for high-concurrency scanning
- ✅ **Configurable Scanning**: Flexible port ranges and concurrency control
- ✅ **Service Detection**: Banner grabbing for service fingerprinting
- ✅ **Multiple Output Formats**: Table, CSV, and JSON output
- ✅ **Detailed Statistics**: Results categorized by port state (open/closed/filtered)
- ✅ **Cross-Platform**: Works on Linux, macOS, and Windows
- ✅ **Dual Implementation**: C++ (performance) and Python (accessibility)
- ✅ **Well-Documented**: Comprehensive learning materials included

## 🚀 Quick Start

### C++ Version (Recommended)

```bash
# Prerequisites: C++20 compiler, Boost libraries, CMake 3.16+
mkdir build && cd build
cmake ..
cmake --build . --config Release

# Run the scanner
./simplePortScanner -t 192.168.1.1 -p 1-1024

# With custom options
./simplePortScanner -t example.com -p 80,443,8080 -T 300 -o 5
```

### Python Version

```bash
# No dependencies required beyond Python 3.8+
python port_scanner.py -t 192.168.1.1 -p 1-1024

# With output file
python port_scanner.py -t example.com -p 1-65535 -f results.csv -F csv
```

## 📖 Usage Guide

### C++ Version

```bash
./simplePortScanner [OPTIONS]

OPTIONS:
  -h, --help              Show help message
  -t, --target HOST       Target IP address or hostname (required)
  -p, --ports RANGE       Ports to scan (default: 1-1024)
                          Format: "1-1024" or "22,80,443,3306"
  -T, --threads NUM       Concurrent threads (default: 200, max: 1000)
  -o, --timeout SEC       Connection timeout in seconds (default: 3)
  -f, --output FILE       Output file (CSV or JSON)
  -F, --format FORMAT     Output format: table, csv, json (default: table)
  -v, --verbose           Enable verbose output

EXAMPLES:
  # Scan common ports on localhost
  ./simplePortScanner -t 127.0.0.1 -p 1-1024

  # Scan with high concurrency
  ./simplePortScanner -t 192.168.1.1 -p 1-65535 -T 500

  # Save results to CSV
  ./simplePortScanner -t example.com -p 1-10000 -f results.csv -F csv

  # JSON output for tool integration
  ./simplePortScanner -t scanme.nmap.org -p 1-1024 -f results.json -F json

  # Full TCP scan with custom timeout
  ./simplePortScanner -t target.local -p 1-65535 -o 5 -v
```

### Python Version

```bash
python port_scanner.py [OPTIONS]

OPTIONS:
  -t, --target HOST       Target IP address or hostname (required)
  -p, --ports RANGE       Port range (default: 1-1024)
  -T, --threads NUM       Number of concurrent threads (default: 100)
  -o, --timeout SEC       Connection timeout in seconds (default: 2.0)
  -f, --output-file FILE  Output file
  -F, --format FORMAT     Output format: table, csv, json (default: table)
  -v, --verbose           Enable verbose output

EXAMPLES:
  # Basic scan
  python port_scanner.py -t 127.0.0.1

  # Scan with threading
  python port_scanner.py -t example.com -p 1-10000 -T 50

  # Save to file
  python port_scanner.py -t example.com -p 1-1024 -f results.json -F json
```

## 🏗️ Output Formats

### Table Format (Default)
```
PORT    STATE           SERVICE         BANNER
────────────────────────────────────────────────────────
22      OPEN            SSH             SSH-2.0-OpenSSH_7.4
80      OPEN            HTTP            
443     OPEN            HTTPS           
3306    CLOSED          MySQL           
5432    FILTERED        PostgreSQL      
```

### CSV Format
```
port,state,service,banner
22,"OPEN","SSH","SSH-2.0-OpenSSH_7.4"
80,"OPEN","HTTP",""
443,"OPEN","HTTPS",""
```

### JSON Format
```json
{
  "metadata": {
    "target": "example.com",
    "start_port": 1,
    "end_port": 1024,
    "timestamp": "2026-03-27T12:34:56.789123"
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
    "open": 3,
    "closed": 1000,
    "filtered": 21
  }
}
```

## 🔒 Port States

- **OPEN**: Service is actively listening on the port
- **CLOSED**: Host is reachable but no service is listening
- **FILTERED**: A firewall/filter is blocking access to the port

## 📚 Learning Materials

This project includes comprehensive educational documentation:

| Module | Topic |
|--------|-------|
| [00 - Overview](learn/00-OVERVIEW.md) | Prerequisites, use cases, and quick start |
| [01 - Concepts](learn/01-CONCEPTS.md) | TCP scanning, port states, real-world breach scenarios |
| [02 - Architecture](learn/02-ARCHITECTURE.md) | System design, data flow, async I/O patterns |
| [03 - Implementation](learn/03-IMPLEMENTATION.md) | Code walkthrough, async operations, banner grabbing |
| [04 - Challenges](learn/04-CHALLENGES.md) | Extension ideas and advanced features |

## 💡 Use Cases

1. **Penetration Testing**: Initial reconnaissance for vulnerability assessment
2. **Security Audits**: Verify exposed services match security policies
3. **Network Inventory**: Map active services on internal networks
4. **Incident Response**: Detect backdoors and unauthorized services
5. **Compliance Scanning**: PCI-DSS, SOC 2, and other audit requirements
6. **Development**: Testing service startup and availability

## 🛡️ Legal & Ethical

⚠️ **DISCLAIMER**: This tool is for authorized security testing only. 

- Only scan networks you own or have explicit written permission to test
- Unauthorized port scanning may violate computer fraud and abuse laws
- Always obtain proper authorization before penetration testing
- Log all scanning activities for audit trails
- Respect organizational policies and legal boundaries

## 🔧 Building from Source

### Requirements

**C++ Version:**
- C++20 compatible compiler (GCC 10+, Clang 12+, MSVC 2019+)
- Boost 1.70+ (Asio, Program_options)
- CMake 3.16+

**Python Version:**
- Python 3.8+
- No external dependencies

# Build C++ version
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release

# Verify build
./simplePortScanner --help
```

### Install Boost (if needed)

**Ubuntu/Debian:**
```bash
sudo apt-get install libboost-all-dev
```

**macOS:**
```bash
brew install boost
```

**Windows (vcpkg):**
```bash
vcpkg install boost:x64-windows
```

## 📊 Performance Metrics

| Scan Type | Time | Threads |
|-----------|------|---------|
| 1024 common ports | ~5 sec | 200 |
| 10,000 ports | ~15 sec | 300 |
| 65,535 (full) | ~120 sec | 500 |

*Times vary based on network latency and target responsiveness*

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

- UDP port scanning
- Service version detection improvements
- IPv6 support
- SOCKS/proxy support
- Rate limiting and IDS evasion
- Web UI dashboard
- Docker containerization

## 📄 License

AGPL 3.0 - See [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- **Boost.Asio**: Asynchronous I/O library
- **Nmap**: Inspiration for architecture and features
- **Wireshark**: Network analysis reference
- **Security Research Community**: Best practices and threat intelligence

## 📞 Support

- **Issues**: GitHub issue tracker
- **Discussions**: Community Q&A
- **Documentation**: See `learn/` directory
- **Examples**: See usage examples above

---

**Built with ❤️ for the cybersecurity community**

*Last Updated: 28 March 2026 | Version 2.0*

