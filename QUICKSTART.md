# Quick Start Guide - Simple Port Scanner

Simple step-by-step instructions to get the port scanner running.

## Option 1: Python Version (Easiest - No Installation Required)

### Step 1: Open Command Prompt/Terminal
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac**: Press `Cmd + Space`, type `terminal`, press Enter
- **Linux**: Open your terminal application

### Step 2: Navigate to the Project
```bash
cd "f:\g projects\port scanner"
```

### Step 3: Run the Scanner
```bash
python port_scanner.py -t 127.0.0.1 -p 1-100
```

**What this does:**
- Scans localhost (127.0.0.1)
- Checks ports 1-100
- Shows results in a table

### Step 4: View Results
You'll see output like:
```
PORT    STATE           SERVICE         BANNER
22      OPEN            SSH             
80      OPEN            HTTP            
```

## Option 2: C++ Version (Recommended for Performance)

### Prerequisites Check
First, verify you have the tools installed:

#### Step 1: Check C++ Compiler
```bash
g++ --version
```
or
```bash
clang --version
```

If you see a version number, you have a compiler! ✓

If not, install:
- **Windows**: Download from mingw-w64.org or use Visual Studio
- **Mac**: Run `xcode-select --install`
- **Linux**: Run `sudo apt-get install build-essential`

#### Step 2: Check CMake
```bash
cmake --version
```

If you see a version number, you have CMake! ✓

If not, install:
- **Windows**: Download from cmake.org
- **Mac**: Run `brew install cmake`
- **Linux**: Run `sudo apt-get install cmake`

#### Step 3: Check Boost
```bash
pkg-config --modversion boost
```

If you see a version, you have Boost! ✓

If not, install:
- **Windows**: Use vcpkg or download from boost.org
- **Mac**: Run `brew install boost`
- **Linux**: Run `sudo apt-get install libboost-all-dev`

### Building the C++ Version

#### Step 1: Create Build Directory
```bash
cd "f:\g projects\port scanner"
mkdir build
cd build
```

#### Step 2: Configure with CMake
```bash
cmake ..
```

#### Step 3: Build
```bash
cmake --build . --config Release
```

#### Step 4: Run the Scanner
**Windows:**
```bash
.\Release\simplePortScanner.exe -t 127.0.0.1 -p 1-100
```

**Mac/Linux:**
```bash
./simplePortScanner -t 127.0.0.1 -p 1-100
```

## Common Commands

### Python Version

```bash
# Scan localhost (common ports)
python port_scanner.py -t 127.0.0.1

# Scan specific host
python port_scanner.py -t example.com -p 1-1024

# Scan with custom threads (faster)
python port_scanner.py -t example.com -p 1-10000 -T 50

# Save results to file
python port_scanner.py -t example.com -p 1-1024 -f results.csv -F csv
```

### C++ Version

```bash
# Scan localhost
./simplePortScanner -t 127.0.0.1

# Fast scan with more threads
./simplePortScanner -t example.com -p 1-65535 -T 400

# Save as JSON
./simplePortScanner -t example.com -p 1-1024 -f results.json -F json

# Show help
./simplePortScanner -h
```

## Understanding the Output

### What do the port states mean?

- **OPEN** 🟢 - Service is running/listening on this port
- **CLOSED** 🔴 - Port exists but nothing is listening
- **FILTERED** 🟡 - A firewall is blocking access

### Example Results

```
PORT    STATE           SERVICE         
22      OPEN            SSH             <- Someone can connect via SSH
80      OPEN            HTTP            <- Web server is running
443     OPEN            HTTPS           <- Secure web server is running
3306    CLOSED          MySQL           <- MySQL is not running
8080    FILTERED        HTTP-Alt        <- Firewall is blocking it
```

## Troubleshooting

### Python Version Won't Run
**Problem**: `python: command not found`
**Solution**: Install Python from python.org or use `python3`

```bash
python3 port_scanner.py -t 127.0.0.1
```

### C++ Build Fails
**Problem**: `CMake not found` or `Boost not found`
**Solution**: 
1. Install missing tools (see Prerequisites)
2. Try these commands before building again:
   ```bash
   cmake --version  # Check CMake is installed
   ```

### "Permission denied" on Mac/Linux
**Solution**: Make file executable first
```bash
chmod +x simplePortScanner
./simplePortScanner -t 127.0.0.1
```

### "Connection refused" or no results
**This is normal!** The target might:
- Not have services running
- Be blocking the port
- Be unreachable

Try scanning localhost first (127.0.0.1) to test.

## Recommended First Scans

### Test 1: Scan Your Own Computer
```bash
# Python
python port_scanner.py -t 127.0.0.1 -p 1-100

# C++
./simplePortScanner -t 127.0.0.1 -p 1-100
```

### Test 2: Scan a Web Server (with permission)
```bash
# Python
python port_scanner.py -t scanme.nmap.org -p 1-1024

# C++
./simplePortScanner -t scanme.nmap.org -p 1-1024
```
Note: scanme.nmap.org is a public host for practicing port scans.

## Getting More Help

- **See all options**: Add `-h` flag
  ```bash
  ./simplePortScanner -h
  python port_scanner.py -h
  ```

- **Detailed guides**: Read these files:
  - `USAGE.md` - Complete usage guide
  - `BUILD.md` - Detailed build instructions
  - `README.md` - Full features and documentation

## Legal Reminder ⚠️

**Only scan computers you own or have permission to scan!**

Unauthorized port scanning is illegal in many places.

---

**You're ready to go! Start with the Python version for the easiest experience.** 🚀
