import csv
import re
import pandas as pd
import os

# Directories for input and output
input_dir = './input'
output_dir = './Linux_if_nameindex'
os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

# Define keywords for system information discovery (containment check with *)
keywords = [
    # "*systeminfo*"
    # "*ipconfig*"
    # "*ComputerInfo*"
    # "*ifconfig*"
    # "*uname.exe*"
    # "*release*"
    # "*wmic*"
    # "*LocalUser*"
    # "*passwd*"
    # "*group*"
    # "*domainname*"
    # "*hostname*"
    # "*tasklist /v*"
    # "*ScheduledTask*"
    # "*aux*"
    # "*crontab*"
    # "*dpkg*"
    # "*rpm*"
    # "*HotFix*"
    # "*env*"
    # "*ver >> %temp%\download systeminfo >> %temp%\download*"
    # "GetSystemInfo"
    # "GetUserNameA"
    # "netstat -ano"
    # "*reg query hklm\software*"
    # "*system_profiler*"
    # "*systemsetup -gettimezone*"
    # "*-getcomputername*"
    # "*-listallnetworkservices*"
    # "*statvfs*"
    "*if_nameindex*"
    # "*instances get*"
    # "*SPHardwareDataType*"
    # "*system_profiler SPHardwareDataType SPSoftwareDataType*"
    # "*management.azure.com/subscriptions/*"
    # "*Sysinfo.exe*"
]

# Compile regex pattern to search for keywords as part of any string (ignores leading/trailing characters)
pattern = re.compile(r'(' + '|'.join(re.escape(keyword.strip('*')) for keyword in keywords) + r')', re.IGNORECASE)

# Process each TSV file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.tsv'):
        tsv_file_path = os.path.join(input_dir, filename)
        output_tsv_file_path = os.path.join(output_dir, f"output-{filename}")

        # Initialize a list to store rows that contain keywords
        flagged_rows = []
        
        print(f"[INFO] Processing file: {filename}")

        # Read the TSV file and check for keywords in the command line column (tab-separated)
        with open(tsv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')  # Specify tab delimiter
            
            row_count = 0
            matched_count = 0

            for row in reader:
                row_count += 1
                command_line = row.get("action_process_image_command_line", "")

                # Ensure command_line is a string before applying regex
                if command_line and isinstance(command_line, str) and pattern.search(command_line):
                    matched_count += 1
                    print(f"[DEBUG] Match found in file {filename}, row {row_count}: {command_line}")
                    flagged_rows.append(row)  # Add entire row to flagged_rows

            print(f"[INFO] Total rows processed in {filename}: {row_count}")
            print(f"[INFO] Total rows with matched keywords in {filename}: {matched_count}")

        # Check if any matches were found and save to output TSV if any
        if flagged_rows:
            # Convert flagged rows to DataFrame and save to new TSV
            df = pd.DataFrame(flagged_rows)
            df.to_csv(output_tsv_file_path, index=False, sep='\t')  # Save as tab-separated file
            print(f"[INFO] Filtered output saved to {output_tsv_file_path}")
        else:
            print(f"[INFO] No rows with system discovery keywords found in {filename}.")
