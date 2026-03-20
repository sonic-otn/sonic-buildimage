#!/bin/bash

PLATFORM_PROFILE="/usr/share/sonic/platform/default.json"
JSON_FILE="/etc/evprofile/default.json"

# Copy platform-specific event profile if present
if [ -f "$PLATFORM_PROFILE" ]; then
    cp "$PLATFORM_PROFILE" "$JSON_FILE"
fi

# Check if file exists and is not empty
if [ -s "$JSON_FILE" ]; then
    # Check if "events" is defined and has at least one entry
    if jq -e '.events and (.events | length > 0)' "$JSON_FILE" > /dev/null; then
        echo "Valid events found. Starting eventdb."
        exec /usr/bin/eventdb
    else
        echo "'events' list is missing or empty. Skipping eventdb start."
        exit 0
    fi
else
    echo "JSON file missing or empty. Skipping eventdb start."
    exit 0
fi
