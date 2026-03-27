cmake_minimum_required(VERSION 3.16)
project(simplePortScanner
        VERSION 2.0
        DESCRIPTION "Asynchronous TCP Port Scanner with Boost.Asio"
        LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -Wall -Wextra -Wpedantic")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall")

# Find required packages
find_package(Boost 1.70 REQUIRED COMPONENTS system program_options)

# Include directories
include_directories(${Boost_INCLUDE_DIRS})

# Create executable
add_executable(simplePortScanner
    main.cpp
    src/PortScanner.hpp
    src/PortScanner.cpp
)

# Link libraries
target_link_libraries(simplePortScanner
    ${Boost_LIBRARIES}
)

# Additional compiler flags for better diagnostics
if(MSVC)
    target_compile_options(simplePortScanner PRIVATE /W4)
else()
    target_compile_options(simplePortScanner PRIVATE -Wall -Wextra -Wpedantic)
endif()

# Installation
install(TARGETS simplePortScanner DESTINATION bin)
install(FILES README.md LICENSE DESTINATION share/doc/simplePortScanner)

# Print configuration info
message(STATUS "=== Simple Port Scanner v2.0 ===")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Boost Version: ${Boost_VERSION}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")

