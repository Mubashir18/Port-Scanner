# Building Simple Port Scanner v2.0

This guide covers building and testing the port scanner C++ implementation.

## System Requirements

### Minimum Requirements
- **C++ Compiler**: C++20 support (GCC 10+, Clang 12+, MSVC 2019+)
- **CMake**: Version 3.16 or higher
- **Boost**: Version 1.70+ with Asio and Program_options libraries

### Recommended
- **Git**: For cloning the repository
- **Make/Ninja**: For faster builds
- **Clang-Format**: For code formatting

## Installation by Platform

### Ubuntu/Debian

```bash
# Install build tools
sudo apt-get update
sudo apt-get install -y build-essential cmake git

# Install Boost libraries
sudo apt-get install -y libboost-all-dev

# Alternatively, minimal Boost install
sudo apt-get install -y libboost-system-dev libboost-program-options-dev
```

### macOS

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install CMake and Boost
brew install cmake boost
```

### Windows (Visual Studio)

```powershell
# Using vcpkg (recommended)
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\vcpkg integrate install
.\vcpkg install boost:x64-windows

# Alternative: Download from boost.org and set BOOST_ROOT environment variable
```

### Windows (MinGW)

```bash
# Using pacman (MSYS2)
pacman -S mingw-w64-x86_64-cmake mingw-w64-x86_64-boost

# Or using Chocolatey
choco install cmake boost-msvc-14.0
```

## Building the Project

### Basic Build

```bash
# Navigate to project directory
cd simple-port-scanner

# Create build directory
mkdir build
cd build

# Configure with CMake
cmake ..

# Build the project
cmake --build . --config Release
# or on Unix: make
```

### Advanced Build Options

```bash
# Build with debug symbols
cmake .. -DCMAKE_BUILD_TYPE=Debug
cmake --build . --config Debug

# Build with verbose output
cmake --build . --config Release -- VERBOSE=1

# Specify generator
cmake .. -G "Unix Makefiles"           # on Linux/macOS
cmake .. -G "Ninja"                    # on Windows/Mac (faster)
cmake .. -G "Visual Studio 16 2019"    # on Windows with MSVC

# Specify Boost path (if not found automatically)
cmake .. -DBOOST_ROOT=/path/to/boost
```

### Using Just

```bash
# Install just (https://just.systems/install.sh)
just build       # Build project
just rebuild     # Clean and rebuild
just clean       # Remove build artifacts
```

## Verifying the Build

```bash
# Check if executable was created
ls -la build/simplePortScanner    # Linux/macOS
dir build\Release\simplePortScanner.exe  # Windows

# Run help command
./build/simplePortScanner -h      # Linux/macOS
.\build\Release\simplePortScanner.exe -h  # Windows
```

## Testing the Build

### Quick Test (localhost)

```bash
# Scan localhost ports
./simplePortScanner -t 127.0.0.1 -p 1-100
```

### CSV Output Test

```bash
./simplePortScanner -t localhost -p 1-1024 -f results.csv -F csv
cat results.csv
```

### JSON Output Test

```bash
./simplePortScanner -t localhost -p 1-1024 -f results.json -F json
# View JSON output
cat results.json
```

## Troubleshooting

### CMake not found
```bash
# Add CMake to PATH or use full path
export PATH="/usr/local/cmake/bin:$PATH"    # macOS
PATH "C:\Program Files\CMake\bin;%PATH%"    # Windows
```

### Boost not found
```bash
# Set BOOST_ROOT environment variable
export BOOST_ROOT=/usr/local/boost_1_76_0   # macOS
SET BOOST_ROOT=C:\local\boost_1_76_0        # Windows

# Then reconfigure CMake
cmake .. -DBOOST_ROOT=$BOOST_ROOT
```

### Compiler version mismatch
```bash
# Specify compiler explicitly
cmake .. -DCMAKE_CXX_COMPILER=g++-10
cmake .. -DCMAKE_CXX_COMPILER=clang++
```

### Permission denied (on Unix)
```bash
chmod +x build/simplePortScanner
./build/simplePortScanner -h
```

## Building on Different Platforms

### Building on Linux (GCC/Clang)

```bash
mkdir build && cd build
cmake .. -DCMAKE_CXX_COMPILER=g++-11 -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release -j$(nproc)
```

### Building on macOS (Clang)

```bash
mkdir build && cd build
cmake .. -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release -j$(sysctl -n hw.ncpu)
```

### Building on Windows (MSVC)

```bash
mkdir build
cd build
cmake .. -G "Visual Studio 16 2019" -A x64
cmake --build . --config Release
```

### Building on Windows (MinGW)

```bash
mkdir build
cd build
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release
```

## Optimization Flags

The CMakeLists.txt includes optimization flags:

- **Debug**: `-g -O0` (no optimization, full debugging)
- **Release**: `-O3 -Wall -Wextra` (full optimization, minimal warnings)

To customize:

```bash
cmake .. -DCMAKE_CXX_FLAGS="-march=native -O3"
```

## Installation

```bash
# Install to system (requires permissions)
cd build
cmake --install . --prefix /usr/local

# Or with custom prefix
cmake .. -DCMAKE_INSTALL_PREFIX=~/.local
cmake --install .

# Binary location: ~/.local/bin/simplePortScanner
```

## Performance Tuning

### Multi-threaded builds
```bash
cmake --build . --config Release -j4  # Use 4 threads
```

### Memory usage
The scanner uses shared pointers for async operations. For large port ranges:

```bash
# Scan in chunks to reduce memory
./simplePortScanner -t target.com -p 1-10000      # First 10k
./simplePortScanner -t target.com -p 10001-20000  # Next 10k
```

## Building Python Version

The Python version requires no compilation:

```bash
# Verify Python installation
python3 --version

# Run directly
python3 port_scanner.py -t example.com -p 1-1024

# Make executable on Unix
chmod +x port_scanner.py
./port_scanner.py -t example.com -p 1-1024
```

## Version Info

Check build and version information:

```bash
# From build directory
cmake --system-information

# Check compiler
gcc --version
clang --version
cmake --version
```

## Next Steps

After building:

1. **Run basic test**: `./build/simplePortScanner -t 127.0.0.1 -p 1-100`
2. **Read documentation**: See `README.md` and `learn/` directory
3. **Try different formats**: Test CSV and JSON output options
4. **Explore options**: Run with `-h` for full option list

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `boost not found` | Install Boost or set BOOST_ROOT environment variable |
| `C++20 features not supported` | Update compiler (GCC 10+, Clang 12+, MSVC 2019+) |
| `CMake version too old` | Update CMake to 3.16 or higher |
| `Permission denied` | Run `chmod +x simplePortScanner` on Unix |
| `Port already in use` | Change test ports or disable target services |

## Support & Documentation

- **Full Documentation**: See README.md
- **Learning Modules**: See `learn/` directory
- **Build Issues**: Check CMakeLists.txt for dependencies
- **Usage Examples**: Run binary with `-h` flag

---

**Happy scanning! 🔍**
