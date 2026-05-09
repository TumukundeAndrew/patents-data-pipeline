import pandas as pd
import os

def process_inventors_data():
    base_dir = r"d:\cloud assignment\inventors"
    
    files_to_process = [
        "g_inventor_disambiguated.tsv.zip",
        "g_location_disambiguated.tsv.zip"
    ]
    
    for filename in files_to_process:
        input_file = os.path.join(base_dir, filename)
        
        # Determine output file name by removing .zip and adding _100k
        output_filename = filename.replace(".zip", "")
        output_filename = output_filename.replace(".tsv", "_100k.tsv")
        output_file = os.path.join(base_dir, output_filename)
        
        print(f"Reading the first 100,000 rows from {filename}...")
        
        try:
            # We use compression='zip' to read directly from the zip file
            df = pd.read_csv(input_file, sep='\t', nrows=100000, compression='zip', low_memory=False)
            
            # Save the extracted data to a new smaller TSV file
            df.to_csv(output_file, sep='\t', index=False)
            
            print(f"Successfully read and saved {len(df)} rows to {output_file}")
            
            # Display the first few rows as a preview
            print(f"\nPreview of the data in {filename}:")
            print(df.head())
            print("-" * 50)
            
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")
            print("-" * 50)

if __name__ == "__main__":
    process_inventors_data()
