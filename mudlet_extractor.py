import xml.etree.ElementTree as ET
import os
import argparse

def save_script(name, content, folder_path, regex_list=None):
    """Save the Lua script content to a .lua file in the specified folder, including regex triggers as comments."""
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{name}.lua")
    with open(file_path, 'w') as file:
        # Write regex patterns as comments at the top of the file
        if regex_list:
            file.write("-- Regex Triggers:\n")
            for regex in regex_list:
                file.write(f"-- {regex}\n")
            file.write("\n")  # Add a blank line after regex comments

        # Write the script content
        file.write(content)
    print(f"Saved script: {file_path}")

def parse_group(group_element, current_path):
    """Recursively create folder structure and save scripts based on XML group hierarchy."""
    for child in group_element:
        # Handle nested groups to create folders
        if 'Group' in child.tag:  # TriggerGroup, AliasGroup, ScriptGroup
            group_name = child.find('name').text or 'UnnamedGroup'
            new_path = os.path.join(current_path, group_name)
            os.makedirs(new_path, exist_ok=True)
            print(f"Created folder: {new_path}")
            parse_group(child, new_path)
        
        # Handle individual scripts within groups
        elif child.tag in ['Trigger', 'Alias', 'Script']:
            script_name = child.find('name').text or 'UnnamedScript'
            script_content = child.find('script').text or '-- No content'

            # Gather regex patterns if available
            regex_list = []
            if child.tag == 'Trigger':
                regex_code_list = child.find('regexCodeList')
                if regex_code_list is not None:
                    regex_list = [regex.text for regex in regex_code_list.findall('string')]
            elif child.tag == 'Alias':
                regex = child.find('regex')
                if regex is not None:
                    regex_list = [regex.text]

            # Save the script with regex patterns as comments
            save_script(script_name, script_content, current_path, regex_list=regex_list)

def main(input_file, output_dir):
    """Main function to parse the XML file and generate the folder structure with scripts."""
    try:
        tree = ET.parse(input_file)
        print("XML tree successfully parsed.")
    except ET.ParseError as e:
        print(f"Failed to parse XML file: {e}")
        return

    root = tree.getroot()
    if root is not None:
        # Define base folders for each type of package, ignoring VariablePackage
        base_dirs = {
            'TriggerPackage': os.path.join(output_dir, 'Triggers'),
            'AliasPackage': os.path.join(output_dir, 'Aliases'),
            'ScriptPackage': os.path.join(output_dir, 'Scripts')
        }
        
        for package_tag, base_dir in base_dirs.items():
            package_element = root.find(package_tag)
            if package_element is not None:
                os.makedirs(base_dir, exist_ok=True)
                print(f"Created base folder for {package_tag}: {base_dir}")
                parse_group(package_element, base_dir)
    else:
        print("Root element is None. Cannot proceed with parsing.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Mudlet XML package and extract scripts to a folder structure.")
    parser.add_argument('--input', required=True, help="Path to the input XML file.")
    parser.add_argument('--output', required=True, help="Path to the output directory.")
    args = parser.parse_args()

    main(args.input, args.output)