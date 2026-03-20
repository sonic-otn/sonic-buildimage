#!/bin/bash
# yang_auto_cli.sh
# Automatically generate CLI commands from SONiC YANG models
# Safe for systemd + dpkg + SONiC runtime

set -euo pipefail

########################################
# Configuration
########################################
LOG_FILE="/var/log/sonic-yanggen.log"
YANG_BASE_DIR="/usr/share/sonic/device-yang"
YANG_DEST_DIR="/usr/local/yang-models"
DEVICE_BASE_DIR="/usr/share/sonic/device"

########################################
# Ensure logging works
########################################
mkdir -p "$(dirname "$LOG_FILE")"

log_message() {
    echo "[$(date '+%F %T')] $1" | tee -a "$LOG_FILE"
}

get_show_generate_opts() {
    local yang_basename="$1"
    local device_config="$2"
    local source_yang=""
    local annot_yang=""
    local layout_flag=""
    local generated_basename=""

    if [ ! -f "$device_config" ]; then
        return 0
    fi

    while read -r source_yang annot_yang layout_flag _; do
        [ -n "${source_yang:-}" ] || continue

        generated_basename="${source_yang%.yang}"
        generated_basename="${generated_basename/openconfig/sonic}"

        if [ "$generated_basename" = "$yang_basename" ]; then
            if [ "${layout_flag:-}" = "vertical" ]; then
                echo "--vertical"
            fi
            return 0
        fi
    done < <(grep -v '^#' "$device_config" | grep -v '^$')
}

########################################
# Must run as root (systemd)
########################################
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: yang_auto_cli.sh must be run as root" >&2
    exit 1
fi

########################################
# Detect ONIE platform (runtime only)
########################################
ONIE_PLATFORM=""

if [ -f /host/machine.conf ]; then
    # shellcheck disable=SC1091
    . /host/machine.conf
    ONIE_PLATFORM="${onie_platform:-}"
fi

if [ -z "$ONIE_PLATFORM" ]; then
    log_message "WARNING: ONIE platform not detected, skipping YANG auto CLI generation"
    exit 0
fi

mkdir -p "$YANG_DEST_DIR"
SOURCE_DIR="$YANG_BASE_DIR/$ONIE_PLATFORM"
DEVICE_CONFIG="$DEVICE_BASE_DIR/$ONIE_PLATFORM/yang_auto_cli"

########################################
# Start
########################################
log_message "=================================================="
log_message "Starting SONiC YANG Auto CLI Generation"
log_message "Source directory: $SOURCE_DIR"
log_message "Target directory: $YANG_DEST_DIR"
log_message "Device config: $DEVICE_CONFIG"
log_message "=================================================="

########################################
# Validate Source directory
########################################
if [ ! -d "$SOURCE_DIR" ]; then
    log_message "WARNING: Source YANG directory not found: $SOURCE_DIR"
    exit 0
fi

if [ ! -f "$DEVICE_CONFIG" ]; then
    log_message "WARNING: Device config not found: $DEVICE_CONFIG"
fi

########################################
# Check sonic-cli-gen
########################################
if ! command -v sonic-cli-gen >/dev/null 2>&1; then
    log_message "WARNING: sonic-cli-gen not found, skipping auto CLI generation"
    exit 0
fi

########################################
# Process YANG files
########################################
PROCESSED_COUNT=0
FAILED_COUNT=0

shopt -s nullglob

# load sonic default system sonic yang-models
sonic-cli-gen generate config sonic-syslog
sonic-cli-gen generate show sonic-syslog
# This should be done by system CLI generator. Temporary solution.
sonic-cli-gen generate show sonic-event
# onic-cli-gen generate show sonic-alarm

for src_file in "$SOURCE_DIR"/*.yang; do
    yang_basename="$(basename "$src_file" .yang)"
    dest_file="$YANG_DEST_DIR/$(basename "$src_file")"
    show_generate_opts="$(get_show_generate_opts "$yang_basename" "$DEVICE_CONFIG")"

    # Copy file to destination
    cp "$src_file" "$dest_file"

    log_message "Processing YANG: $yang_basename"
    if [ -n "$show_generate_opts" ]; then
        log_message "  Show CLI options: $show_generate_opts"
    fi

    if sonic-cli-gen generate show "$yang_basename" $show_generate_opts >>"$LOG_FILE" 2>&1 \
       && sonic-cli-gen generate config "$yang_basename" >>"$LOG_FILE" 2>&1; then
        log_message "  ✓ CLI generated successfully for $yang_basename"
        PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
    else
        log_message "  ✗ CLI generation failed for $yang_basename"
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
done
shopt -u nullglob

########################################
# Summary
########################################
log_message "=================================================="
log_message "YANG Auto CLI Generation Completed"
log_message "Processed: $PROCESSED_COUNT"
log_message "Failed:    $FAILED_COUNT"
log_message "=================================================="

########################################
# IMPORTANT:
# Never fail systemd / dpkg install
########################################
exit 0
