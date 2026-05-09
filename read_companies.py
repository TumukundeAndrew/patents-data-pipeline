import pandas as pd
import os

def process_companies_data():
    print("Reading the first 100,000 rows from g_assignee_disambiguated.tsv.zip...")
    
    # Define file paths
    input_file = r"d:\cloud assignment\companies(assignees)\g_assignee_disambiguated.tsv.zip"
    output_file = r"d:\cloud assignment\companies(assignees)\g_assignee_disambiguated_100k.tsv"
    
    # Read the first 100,000 rows from the zipped TSV file
    try:
        # We use compression='zip' to read directly from the zip file
        df = pd.read_csv(input_file, sep='\t', nrows=100000, compression='zip', low_memory=False)
        
        # Save the extracted data to a new smaller TSV file
        df.to_csv(output_file, sep='\t', index=False)
        
        print(f"Successfully read and saved {len(df)} rows to {output_file}")
        
        # Display the first few rows as a preview
        print("\nPreview of the data:")
        print(df.head())
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_companies_data()
