# Mudlet-Devlopment-Server
 The Mudlet dev server monitors .mpackage changes, extracting triggers, aliases, and scripts into organized .lua files. A Python script parses XML data, while a Bash script continuously watches for updates, enabling efficient, structured development and documentation of Mudlet packages.
=======
# Mudlet-Development-Server

The **Mudlet-Development-Server** is a tool designed to streamline development for Mudlet packages. It monitors `.mpackage` files for changes and extracts essential components (triggers, aliases, scripts) into individual, organized `.lua` files, making them easier to work with in version control.

This repository includes:
- A **Bash script (`monitor_and_extract.sh`)** to watch `.mpackage` files for changes and trigger extractions automatically.
- A **Python script (`mudlet_extractor.py`)** to handle the parsing and extraction of the XML data inside `.mpackage` files.

## Features

- **Automated Extraction**: Continuously monitors for changes in a specified `.mpackage` file, extracting and updating Lua files on modification.
- **Organized Output**: Extracts triggers, aliases, and scripts into organized folders within the specified output directory.
- **Simplified Mudlet Package Development**: Helps maintain a well-structured Mudlet package development workflow, making it easy to track changes in source control.

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/Mudlet-Development-Server.git
   cd Mudlet-Development-Server
   ```

2. **Install dependencies**:
   - Ensure **Python 3** is installed:
     ```bash
     # Debian/Ubuntu
     sudo apt-get install python3
     # macOS (with Homebrew)
     brew install python3
     ```

3. **Set permissions** for `monitor_and_extract.sh`:
   ```bash
   chmod +x monitor_and_extract.sh
   ```

## Usage

1. **Prepare your `.mpackage` file**:
   - Place your `.mpackage` file in a directory accessible to the script.

2. **Run the monitoring script**:
   - Start the `monitor_and_extract.sh` script, providing paths to the `.mpackage` file and the output directory:
     ```bash
     ./monitor_and_extract.sh <path_to_mpackage> <output_directory>
     ```

   This command:
   - **Monitors** the specified `.mpackage` file for changes.
   - **Extracts** triggers, aliases, and scripts from the `.mpackage` file on each detected modification.
   - **Outputs** the extracted files to the specified directory.

### Example

```bash
./monitor_and_extract.sh ./packages/MyMudletPackage.mpackage ./output
```

3. **Extracted Output**:
   - Files are extracted into subdirectories (`triggers`, `aliases`, `scripts`) within the output directory you specify.

4. **Monitor for Changes**:
   - Once started, `monitor_and_extract.sh` continuously checks the `.mpackage` file for any changes (e.g., updates, modifications).
   - The script uses a hash comparison to detect changes in the `.mpackage` file.

### Script Details

#### `monitor_and_extract.sh`

The Bash script `monitor_and_extract.sh` provides continuous monitoring and triggers re-extraction upon changes to the `.mpackage` file. Here are the key steps in its process:

1. **Initial Extraction**: On startup, it extracts content from the specified `.mpackage` file.
2. **Hash-based Monitoring**: It calculates and monitors the hash of the `.mpackage` file to detect changes.
3. **Re-extraction on Change**: When a change is detected, the script triggers the `mudlet_extractor.py` script to process the updated `.mpackage` file and extract its contents.

**Usage**:
```bash
./monitor_and_extract.sh <path_to_mpackage> <output_directory>
```

#### `mudlet_extractor.py`

The Python script `mudlet_extractor.py` handles the actual extraction from the `.mpackage` file:
- **XML Parsing**: Reads and parses the XML content inside the `.mpackage`.
- **Component Extraction**: Extracts triggers, aliases, and scripts, saving them into organized subdirectories.

## Requirements

- Python 3.x
- Linux or macOS environment for Bash compatibility
- Mudlet-compatible `.mpackage` files

## Troubleshooting

- **File Not Found Errors**: Ensure the `.mpackage` file path and Python script path are correct.
- **Permissions**: If you encounter permissions issues, make sure `monitor_and_extract.sh` is executable (`chmod +x monitor_and_extract.sh`).
- **Extraction Issues**: If no files are extracted, verify that the `.mpackage` file includes the expected XML structure.

## License

This project is open-source and available under the MIT License.

---
