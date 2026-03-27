# Changelog

All notable changes to Simple Port Scanner are documented in this file.

## [2.0] - 2026-03-27

### 🎉 Major Release - Complete Overhaul

A comprehensive redesign and significant feature expansion of the port scanner.

### ✨ Added

#### C++ Version
- **Multiple Output Formats**: Table (colorized), CSV, and JSON output options
- **Enhanced CLI**: Improved help text, usage examples, better error handling
- **Verbose Logging**: Optional verbose output for debugging and understanding scan process
- **Better Statistics**: Detailed summary with colored output for different port states
- **Service Database**: Expanded well-known ports reference (30+ common services)
- **Input Validation**: Comprehensive validation of command-line arguments
- **Error Handling**: Try-catch blocks for robust error management
- **Code Documentation**: Detailed comments explaining async operations
- **Progress Tracking**: Internal tracking of scanned ports for potential progress reporting

#### Python Version
- **Complete Rewrite**: Modern, Pythonic implementation using threading
- **Class-Based Design**: `PortScanner` class for better code organization
- **Multiple Output Formats**: Table, CSV, and JSON support
- **Argument Parsing**: Full `argparse` integration with help text
- **Color Output**: ANSI color codes for terminal output
- **Banner Grabbing**: Service identification through banner grabbing
- **Concurrent Scanning**: Thread-based concurrent port scanning
- **Error Recovery**: Graceful error handling and recovery
- **Statistics Tracking**: Comprehensive statistics collection

#### Project Files
- **BUILD.md**: Comprehensive build and installation guide for all platforms
- **justfile**: Command runner for common tasks (build, test, clean, etc.)
- **Improved README.md**: Much more detailed documentation with usage examples
- **Enhanced CMakeLists.txt**: Better configuration, version info, and compiler flags

### 🔧 Changed

#### C++ Code Improvements
- **Variable Naming**: More descriptive names (`port_queue` vs `q`, `active_threads` vs `cnt`)
- **Member Variables**: Better organization and initialization of class members
- **Method Signatures**: Consistent parameter naming and const correctness
- **Error Messages**: More informative error messages for troubleshooting
- **Output Formatting**: Professional, colored, easy-to-read results
- **Memory Management**: Continued use of `std::shared_ptr` for safe async operations
- **Port Parsing**: Enhanced parser supporting ranges, single ports, and comma-separated lists

#### Python Code Improvements
- **Socket Timeout Handling**: Proper distinction between closed and filtered ports
- **Thread Safety**: Lock-based synchronization for result collection
- **Code Structure**: Clear separation of concerns with dedicated methods
- **Type Hints**: Added type hints for better code clarity
- **Docstrings**: Comprehensive docstrings for all classes and methods
- **Exception Handling**: Specific exception handling for different error scenarios

#### Build System
- **CMake Version**: Increased minimum from 3.31 to 3.16 (more compatible)
- **Compiler Flags**: Added optimization flags and warning levels
- **Package Configuration**: Better Boost package discovery
- **Installation Support**: Added install targets for binaries and documentation

### 🎨 Improved

- **CLI User Experience**: Better help text, usage examples, and error messages
- **Output Formatting**: Professional, color-coded table output
- **Code Readability**: Better variable names, comments, and structure
- **Documentation**: Comprehensive README with examples and use cases
- **Build Process**: Simplified and clearer build instructions
- **Error Messages**: More descriptive and actionable error texts
- **Performance**: Better async operation scheduling in C++ version

### 🐛 Fixed

- **Port Range Validation**: Fixed boundary checking for port ranges
- **Buffer Overflow**: Increased banner buffer size and added bounds checking
- **Resource Leaks**: Proper cleanup of sockets and timers in async operations
- **Thread Safety**: Fixed potential race conditions in result collection
- **CSV Escaping**: Proper quoting and escaping of special characters in CSV output
- **JSON Escaping**: Proper escaping of quotes, backslashes, and control characters
- **Signal Handling**: Better handling of Ctrl+C interruption in Python version

### 📚 Documentation

- **Expanded README.md**: Feature list, installation instructions, usage examples
- **Added BUILD.md**: Platform-specific build instructions and troubleshooting
- **Added justfile**: Common development tasks automation
- **Code Comments**: Better inline documentation explaining async patterns
- **Usage Examples**: Multiple real-world examples in help text

### ⚙️ Technical Details

#### C++20 Features Used
- `std::make_shared<>` for smart pointers
- Lambda functions with captures
- Structured bindings (in std::find operations)
- `std::chrono` for timeout management

#### Boost Libraries
- **Asio**: Asynchronous I/O for concurrent socket operations
- **Program Options**: Command-line argument parsing

#### Python Libraries Used
- `socket`: TCP socket operations
- `threading`: Concurrent port scanning
- `queue`: Thread-safe result collection
- `json`: JSON output format
- `csv`: CSV output format
- `argparse`: Command-line interface

### 🔐 Security Improvements

- **Input Validation**: Ranges checked against port number boundaries
- **Error Boundaries**: Better exception handling prevents crashes
- **Buffer Management**: Controlled buffer sizes prevent overflows
- **Race Condition Prevention**: Proper locking in Python version

### 🚀 Performance

- **Concurrent Operations**: Maintains 200+ concurrent threads in C++ version
- **Thread Efficiency**: Python version uses efficient thread pooling
- **Memory Usage**: Optimized socket handling in both versions
- **Timeout Handling**: Efficient timeout detection without resource waste

### 📋 Breaking Changes

None - This is the initial v2.0 release with backward compatibility maintained.

### ⚠️ Known Issues

- JSONOutput first-item tracking uses static variable (one scan per process)
- Rapid consecutive scans on same target may benefit from process restart
- Banner grabbing timeout is tied to connection timeout

### 🔜 Future Enhancements

- UDP port scanning
- Service version detection
- IPv6 support
- SOCKS/proxy support
- Rate limiting and IDS evasion techniques
- Web UI dashboard
- Docker containerization
- Database integration for result storage
- Nmap output format compatibility

### Contributors

- **Original Author**: [@deniskhud](https://github.com/deniskhud)
- **v2.0 Enhancement**: Community improvements for v2.0

### Archive

Previous version (1.0) included basic sequential scanning and simple output formatting.

---

## Installation

See BUILD.md for detailed platform-specific installation instructions.

## Support

- **Documentation**: See README.md and learn/ directory
- **Issues**: Report bugs with detailed environment information
- **Contributions**: Welcome! See contributing guidelines

---

**Built with ❤️ for the cybersecurity community**
