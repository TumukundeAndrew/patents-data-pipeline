import pandas as pd
import os

def clean_companies_data():
    input_file = r"d:\cloud assignment\companies(assignees)\g_assignee_disambiguated_100k.tsv"
    output_file = r"d:\cloud assignment\companies(assignees)\cleaned_companies.csv"
    
    print(f"Reading data from {input_file}...")
    
    try:
        # Read the 100k rows TSV file
        df = pd.read_csv(input_file, sep='\t', low_memory=False)
        
        # Define the columns we want to keep
        columns_to_keep = ['patent_id', 'assignee_id', 'disambig_assignee_organization']
        
        # Check if all required columns are present
        missing_cols = [col for col in columns_to_keep if col not in df.columns]
        if missing_cols:
            print(f"Warning: The following required columns are missing: {missing_cols}")
            # Keep only the columns that actually exist
            columns_to_keep = [col for col in columns_to_keep if col in df.columns]
        
        # Filter the dataframe to keep only the specified columns
        df_cleaned = df[columns_to_keep].copy()
        
        print(f"Original shape: {df.shape}")
        
        # Handle missing values
        # Drop rows where all the essential identifying columns are missing (if any)
        # or fill them based on a strategy. Let's drop rows where patent_id or assignee_id is missing
        if 'patent_id' in df_cleaned.columns and 'assignee_id' in df_cleaned.columns:
            df_cleaned.dropna(subset=['patent_id', 'assignee_id'], inplace=True)
            
        # Fill missing values in organization name with "Unknown"
        if 'disambig_assignee_organization' in df_cleaned.columns:
            df_cleaned['disambig_assignee_organization'] = df_cleaned['disambig_assignee_organization'].fillna('Unknown')
            
        # Optional: strip whitespace from string columns to clean messy data
        for col in df_cleaned.select_dtypes(include=['object']).columns:
            df_cleaned[col] = df_cleaned[col].str.strip()
            
        # Remove duplicates
        df_cleaned.drop_duplicates(inplace=True)
            
        print(f"Cleaned shape: {df_cleaned.shape}")
        
        # Save the cleaned data
        df_cleaned.to_csv(output_file, sep=',', index=False)
        
        print(f"Successfully saved cleaned data to {output_file}")
        
        # Display preview
        print("\nPreview of cleaned data:")
        print(df_cleaned.head())
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    clean_companies_data()
