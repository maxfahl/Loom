#!/bin/bash

# analyze-websocket-traffic.sh
#
# Description:
#   Captures network traffic for a specified port using tcpdump, saving it to a .pcap file.
#   This script is useful for debugging low-level WebSocket connectivity issues and
#   analyzing the WebSocket handshake and subsequent data frames using external tools like Wireshark.
#
# Usage:
#   sudo ./analyze-websocket-traffic.sh --port 8080 --output ws_traffic.pcap --duration 60
#   ./analyze-websocket-traffic.sh --help
#
# Arguments:
#   --port, -p      : Required. The port number on which the WebSocket server is running.
#   --output, -o    : Optional. The output .pcap file name. Defaults to 'websocket_capture_PORT.pcap'.
#   --duration, -d  : Optional. Duration in seconds to capture traffic. Defaults to 30 seconds.
#   --interface, -i : Optional. Network interface to listen on (e.g., eth0, en0). Defaults to any.
#
# Prerequisites:
#   - tcpdump: Must be installed and accessible. Requires root privileges (sudo).
#
# Example:
#   # Capture traffic on port 8080 for 60 seconds, save to my_ws_capture.pcap
#   sudo ./analyze-websocket-traffic.sh -p 8080 -o my_ws_capture.pcap -d 60
#
#   # After capture, open the .pcap file with Wireshark for detailed analysis:
#   # wireshark -r my_ws_capture.pcap

set -euo pipefail

# --- Configuration Defaults ---
PORT=""
OUTPUT_FILE=""
DURATION=30
INTERFACE="any"

# --- Helper Functions ---

print_help() {
    echo "Usage: sudo $0 --port <PORT> [--output <FILE>] [--duration <SECONDS>] [--interface <INTERFACE>]"
    echo "       $0 --help"
    echo ""
    echo "Arguments:"
    echo "  --port, -p      : Required. The port number on which the WebSocket server is running."
    echo "  --output, -o    : Optional. The output .pcap file name. Defaults to 'websocket_capture_PORT.pcap'."
    echo "  --duration, -d  : Optional. Duration in seconds to capture traffic. Defaults to 30 seconds."
    echo "  --interface, -i : Optional. Network interface to listen on (e.g., eth0, en0). Defaults to any."
    echo ""
    echo "Description:"
    echo "  Captures network traffic for a specified port using tcpdump, saving it to a .pcap file."
    echo "  This script is useful for debugging low-level WebSocket connectivity issues and"
    echo "  analyzing the WebSocket handshake and subsequent data frames using external tools like Wireshark."
    echo ""
    echo "Prerequisites:"
    echo "  - tcpdump: Must be installed and accessible. Requires root privileges (sudo)."
    echo ""
    echo "Example:"
    echo "  sudo $0 -p 8080 -o my_ws_capture.pcap -d 60"
    echo "  wireshark -r my_ws_capture.pcap"
}

log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

# --- Argument Parsing ---

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -p|--port)
        PORT="$2"
        shift # past argument
        shift # past value
        ;;
        -o|--output)
        OUTPUT_FILE="$2"
        shift # past argument
        shift # past value
        ;;
        -d|--duration)
        DURATION="$2"
        shift # past argument
        shift # past value
        ;;
        -i|--interface)
        INTERFACE="$2"
        shift # past argument
        shift # past value
        ;;
        --help)
        print_help
        exit 0
        ;;
        *)
        log_error "Unknown option: $1"
        print_help
        exit 1
        ;;
    esac
done

# --- Validation ---

if [[ -z "$PORT" ]]; then
    log_error "Error: --port is required."
    print_help
    exit 1
fi

if ! command -v tcpdump &> /dev/null; then
    log_error "Error: tcpdump is not installed. Please install it (e.g., sudo apt-get install tcpdump or brew install tcpdump)."
    exit 1
fi

if [[ "$(id -u)" -ne 0 ]]; then
    log_error "Error: This script requires root privileges. Please run with sudo."
    exit 1
fi

if [[ -z "$OUTPUT_FILE" ]]; then
    OUTPUT_FILE="websocket_capture_${PORT}.pcap"
fi

# --- Main Logic ---

log_info "Starting WebSocket traffic capture on port ${PORT} for ${DURATION} seconds..."
log_info "Output will be saved to: ${OUTPUT_FILE}"
log_info "Listening on interface: ${INTERFACE}"
log_info "Press Ctrl+C to stop capture early."

# tcpdump command
# -i ${INTERFACE} : listen on specified interface
# -w ${OUTPUT_FILE} : write raw packets to file
# -s 0 : snaplen 0, capture entire packet
# port ${PORT} : filter by port
# timeout ${DURATION} : stop after duration

timeout ${DURATION} tcpdump -i "${INTERFACE}" -w "${OUTPUT_FILE}" -s 0 "port ${PORT}" || true # `|| true` to prevent script from exiting if timeout kills tcpdump

if [[ -f "${OUTPUT_FILE}" ]]; then
    log_success "Traffic capture complete. Data saved to ${OUTPUT_FILE}"
    log_info "For detailed WebSocket frame analysis, open the .pcap file with Wireshark:"
    log_info "  wireshark -r ${OUTPUT_FILE}"
    log_info "In Wireshark, you can apply a display filter like 'websocket' to see WebSocket frames."
else
    log_error "Traffic capture failed or no data was captured."
fi
