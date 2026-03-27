#include "src/PortScanner.hpp"
#include <boost/program_options.hpp>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cstring>

namespace po = boost::program_options;

void print_banner() {
    std::cout << "\n";
    std::cout << "  ██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ \n";
    std::cout << "  ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗\n";
    std::cout << "  ██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝\n";
    std::cout << "  ██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗\n";
    std::cout << "  ██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║\n";
    std::cout << "  ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝\n";
    std::cout << "  Asynchronous TCP Port Scanner v2.0\n";
    std::cout << "  ─────────────────────────────────────────────────────────\n\n";
}

int main(int argc, char* argv[]) {
    try {
        po::options_description desc("OPTIONS");
        desc.add_options()
            ("help,h", "Display this help message")
            ("target,t", po::value<std::string>()->required(), "Target IP address or hostname")
            ("ports,p", po::value<std::string>()->default_value("1-1024"), "Ports to scan (e.g., '80,443,8080' or '1-1024')")
            ("threads,T", po::value<int>()->default_value(200), "Number of concurrent threads (1-1000)")
            ("timeout,o", po::value<uint8_t>()->default_value(3)->value_name("sec"), "Connection timeout in seconds")
            ("output,f", po::value<std::string>(), "Output file (CSV or JSON format)")
            ("format,F", po::value<std::string>()->default_value("table"), "Output format: table, csv, or json")
            ("verbose,v", "Enable verbose output");

        po::variables_map vm;
        
        try {
            po::store(po::parse_command_line(argc, argv, desc), vm);
            
            if (vm.count("help")) {
                print_banner();
                std::cout << desc << "\n";
                std::cout << "EXAMPLES:\n";
                std::cout << "  Scan common ports on localhost:\n";
                std::cout << "    ./simplePortScanner -t 127.0.0.1 -p 1-1024\n\n";
                std::cout << "  Scan specific ports with 300 threads:\n";
                std::cout << "    ./simplePortScanner -t 192.168.1.1 -p 22,80,443,8080 -T 300\n\n";
                std::cout << "  Full TCP port scan with custom timeout:\n";
                std::cout << "    ./simplePortScanner -t example.com -p 1-65535 -o 5\n\n";
                std::cout << "  Save results to CSV file:\n";
                std::cout << "    ./simplePortScanner -t example.com -p 1-1024 -f results.csv -F csv\n\n";
                std::cout << "DISCLAIMER:\n";
                std::cout << "  Scan only systems you own or have explicit permission to test.\n";
                std::cout << "  Unauthorized port scanning may be illegal.\n\n";
                return 0;
            }
            
            po::notify(vm);
        } catch (const po::error& e) {
            std::cerr << "ERROR: " << e.what() << "\n";
            std::cerr << "Use '-h' or '--help' for usage information.\n";
            return 1;
        }

        // Validate inputs
        std::string target = vm["target"].as<std::string>();
        std::string port = vm["ports"].as<std::string>();
        int threads = vm["threads"].as<int>();
        uint8_t timeout = vm["timeout"].as<uint8_t>();
        std::string format = vm["format"].as<std::string>();

        if (threads < 1 || threads > 1000) {
            std::cerr << "ERROR: Thread count must be between 1 and 1000\n";
            return 1;
        }

        if (format != "table" && format != "csv" && format != "json") {
            std::cerr << "ERROR: Format must be 'table', 'csv', or 'json'\n";
            return 1;
        }

        if (timeout == 0) {
            std::cerr << "ERROR: Timeout must be at least 1 second\n";
            return 1;
        }

        print_banner();
        std::cout << "Target:  " << target << "\n";
        std::cout << "Ports:   " << port << "\n";
        std::cout << "Threads: " << threads << "\n";
        std::cout << "Timeout: " << (int)timeout << " second(s)\n";
        std::cout << "Format:  " << format << "\n";
        if (vm.count("output")) {
            std::cout << "Output:  " << vm["output"].as<std::string>() << "\n";
        }
        std::cout << "─────────────────────────────────────────────────────────\n\n";

        PortScanner scanner;
        scanner.set_options(target, port, threads, timeout);
        if (vm.count("output")) {
            scanner.set_output_file(vm["output"].as<std::string>());
        }
        scanner.set_output_format(format);
        if (vm.count("verbose")) {
            scanner.set_verbose(true);
        }
        
        scanner.start();
        scanner.run();

        return 0;
    } catch (const std::exception& e) {
        std::cerr << "FATAL ERROR: " << e.what() << "\n";
        return 1;
    }
}
