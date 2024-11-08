import pandas as pd
import os

# Define the directory containing the .tsv files and the output file path
input_dir = './uname'  # Replace with your directory path
output_file = './Combine_uname.tsv'  # Save as a single combined .tsv file

# Initialize an empty DataFrame to hold all the data
combined_data = pd.DataFrame()

# Loop through each .tsv file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith('.tsv'):
        file_path = os.path.join(input_dir, filename)
        
        # Read each .tsv file into a DataFrame
        df = pd.read_csv(file_path, delimiter='\t', dtype=str)  # Read all data as strings
        
        # Add a column to identify the source file
        df['source_file'] = filename
        
        # Append to the combined DataFrame
        combined_data = pd.concat([combined_data, df], ignore_index=True)
        
        print(f"[INFO] Added '{filename}' to the combined DataFrame")

# Save the combined data to a single .tsv file
combined_data.to_csv(output_file, sep='\t', index=False)

print(f"[INFO] All .tsv files have been combined into '{output_file}'")
