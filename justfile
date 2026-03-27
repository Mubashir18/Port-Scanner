# Justfile for Simple Port Scanner
# Usage: just [command]

set shell := ["powershell", "-Command"]

# Default target
default:
    @just --list

# Build the C++ port scanner
build:
    @echo "Building Simple Port Scanner..."
    @if (-not (Test-Path "build")) { mkdir build }
    @cd build
    @cmake .. -DCMAKE_BUILD_TYPE=Release
    @cmake --build . --config Release
    @echo "✓ Build successful"

# Clean build artifacts
clean:
    @echo "Cleaning build artifacts..."
    @if (Test-Path "build") { rm -Recurse -Force build }
    @echo "✓ Clean complete"

# Rebuild from scratch
rebuild: clean build

# Run tests/examples
test:
    @echo "Running port scanner on localhost..."
    @.\build\Release\simplePortScanner -t 127.0.0.1 -p 1-100

# Scan example target (scanme.nmap.org)
demo:
    @echo "Running demo scan on scanme.nmap.org..."
    @.\build\Release\simplePortScanner -t scanme.nmap.org -p 1-10000

# Run Python version
python-test:
    @echo "Testing Python version..."
    @python port_scanner.py -t 127.0.0.1 -p 1-100

# Run with CSV output
csv-test:
    @echo "Testing CSV output..."
    @.\build\Release\simplePortScanner -t localhost -p 1-1024 -f results.csv -F csv
    @if (Test-Path "results.csv") { 
        echo "✓ CSV output saved to results.csv"
        type results.csv | head -10
    }

# Run with JSON output
json-test:
    @echo "Testing JSON output..."
    @.\build\Release\simplePortScanner -t localhost -p 1-1024 -f results.json -F json
    @if (Test-Path "results.json") { 
        echo "✓ JSON output saved to results.json"
    }

# Show help
help:
    @echo "Simple Port Scanner - Just Commands"
    @echo "===================================="
    @echo "build       - Build the C++ port scanner"
    @echo "clean       - Clean build artifacts"
    @echo "rebuild     - Clean and rebuild"
    @echo "test        - Run local scan test"
    @echo "demo        - Run demo scan (scanme.nmap.org)"
    @echo "python-test - Test Python version"
    @echo "csv-test    - Test CSV output format"
    @echo "json-test   - Test JSON output format"
    @echo "help        - Show this help message"

# Format code with clang-format
format:
    @echo "Formatting code..."
    @echo "Note: clang-format must be installed"
    @clang-format -i main.cpp src/*.cpp src/*.hpp 2>$null || echo "clang-format not found"

# Run linter
lint:
    @echo "Note: Run with Clang/GCC with -Wall -Wextra -Wpedantic flags"
    @echo "See CMakeLists.txt for compiler flags"

# Verbose test (with verbose output)
verbose-test:
    @echo "Running verbose scan..."
    @.\build\Release\simplePortScanner -t 127.0.0.1 -p 1-100 -v
