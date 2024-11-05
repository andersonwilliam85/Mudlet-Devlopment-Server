#!/bin/bash

# Usage: ./monitor_and_extract.sh <path_to_mpackage> <output_directory>

# Check if exactly two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path_to_mpackage> <output_directory>"
    exit 1
fi

# Assign variables to input arguments
MPACKAGE_FILE="$1"
OUTPUT_DIR="$2"

# Define paths for the Python script and temporary extraction directory
SCRIPT_DIR="$(dirname "$0")"
PYTHON_SCRIPT="$SCRIPT_DIR/mudlet_extractor.py"
TEMP_DIR="$(mktemp -d)"

# Check if the mpackage file exists
if [ ! -f "$MPACKAGE_FILE" ]; then
    echo "Error: mpackage file '$MPACKAGE_FILE' not found."
    exit 1
fi

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python extractor script '$PYTHON_SCRIPT' not found."
    exit 1
fi

# Function to extract the mpackage and process the XML file inside
process_mpackage() {
    echo "[INFO] Extracting contents of $MPACKAGE_FILE to $TEMP_DIR"
    unzip -o "$MPACKAGE_FILE" -d "$TEMP_DIR" > /dev/null

    # Locate the XML file within the extracted contents
    XML_FILE=$(find "$TEMP_DIR" -name "*.xml" | head -n 1)
    if [ -z "$XML_FILE" ]; then
        echo "Error: No XML file found in the mpackage."
        return 1
    fi

    # Ensure the output directory exists
    mkdir -p "$OUTPUT_DIR"

    echo "[INFO] Found XML file: $XML_FILE"
    echo "[INFO] Running extraction on XML file to $OUTPUT_DIR"
    python3 "$PYTHON_SCRIPT" --input "$XML_FILE" --output "$OUTPUT_DIR"
}

# Function to calculate hash of the mpackage file
get_file_hash() {
    sha256sum "$MPACKAGE_FILE" | awk '{print $1}'
}

# Initial file hash
LAST_HASH=$(get_file_hash)

# Initial extraction
process_mpackage

# Monitor the mpackage file for changes and re-run processing on change
echo "[INFO] Monitoring $MPACKAGE_FILE for changes..."

while true; do
    sleep 2  # Small delay to reduce frequency of checks
    CURRENT_HASH=$(get_file_hash)

    # Compare current file hash with the last hash
    if [ "$CURRENT_HASH" != "$LAST_HASH" ]; then
        echo "[INFO] Detected change in $MPACKAGE_FILE. Re-extracting and processing XML..."
        process_mpackage
        LAST_HASH=$CURRENT_HASH  # Update hash to the latest
    fi
done