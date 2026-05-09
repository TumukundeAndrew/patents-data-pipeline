import pandas as pd
import os

def clean_inventors_data():
    base_dir = r"d:\cloud assignment\inventors"
    
    # 1. Clean g_inventor_disambiguated_100k.tsv
    print("--- Cleaning g_inventor_disambiguated_100k.tsv ---")
    inv_input = os.path.join(base_dir, "g_inventor_disambiguated_100k.tsv")
    inv_output = os.path.join(base_dir, "cleaned_inventor_disambiguated.csv")
    
    try:
        df_inv = pd.read_csv(inv_input, sep='\t', low_memory=False)
        inv_cols = ['patent_id', 'inventor_id', 'disambig_inventor_name_first', 'location_id']
        
        # Check and filter columns
        existing_inv_cols = [col for col in inv_cols if col in df_inv.columns]
        missing_inv_cols = [col for col in inv_cols if col not in df_inv.columns]
        if missing_inv_cols:
            print(f"Warning: Missing columns in inventor data: {missing_inv_cols}")
            
        df_inv_cleaned = df_inv[existing_inv_cols].copy()
        
        # Drop rows where essential identifiers are missing
        dropna_cols_inv = [col for col in ['patent_id', 'inventor_id'] if col in df_inv_cleaned.columns]
        if dropna_cols_inv:
            df_inv_cleaned.dropna(subset=dropna_cols_inv, inplace=True)
            
        # Fill missing values
        if 'disambig_inventor_name_first' in df_inv_cleaned.columns:
            df_inv_cleaned['disambig_inventor_name_first'] = df_inv_cleaned['disambig_inventor_name_first'].fillna('Unknown')
            
        # Optional: strip whitespace
        for col in df_inv_cleaned.select_dtypes(include=['object']).columns:
            df_inv_cleaned[col] = df_inv_cleaned[col].str.strip()
            
        df_inv_cleaned.drop_duplicates(inplace=True)
        df_inv_cleaned.to_csv(inv_output, sep=',', index=False)
        print(f"Saved {df_inv_cleaned.shape[0]} rows to {inv_output}\n")
        
    except Exception as e:
        print(f"Error processing inventor data: {e}\n")

    # 2. Clean g_location_disambiguated_100k.tsv
    print("--- Cleaning g_location_disambiguated_100k.tsv ---")
    loc_input = os.path.join(base_dir, "g_location_disambiguated_100k.tsv")
    loc_output = os.path.join(base_dir, "cleaned_location_disambiguated.csv")
    
    try:
        df_loc = pd.read_csv(loc_input, sep='\t', low_memory=False)
        loc_cols = ['location_id', 'patent_id', 'disambig_country']
        
        # Check and filter columns
        existing_loc_cols = [col for col in loc_cols if col in df_loc.columns]
        missing_loc_cols = [col for col in loc_cols if col not in df_loc.columns]
        if missing_loc_cols:
            print(f"Warning: Missing columns in location data: {missing_loc_cols}")
            
        df_loc_cleaned = df_loc[existing_loc_cols].copy()
        
        # Drop rows where essential identifiers are missing
        dropna_cols_loc = [col for col in ['location_id'] if col in df_loc_cleaned.columns]
        if dropna_cols_loc:
            df_loc_cleaned.dropna(subset=dropna_cols_loc, inplace=True)
            
        # Fill missing values
        if 'disambig_country' in df_loc_cleaned.columns:
            df_loc_cleaned['disambig_country'] = df_loc_cleaned['disambig_country'].fillna('Unknown')
            
        # Optional: strip whitespace
        for col in df_loc_cleaned.select_dtypes(include=['object']).columns:
            df_loc_cleaned[col] = df_loc_cleaned[col].str.strip()
            
        df_loc_cleaned.drop_duplicates(inplace=True)
        df_loc_cleaned.to_csv(loc_output, sep=',', index=False)
        print(f"Saved {df_loc_cleaned.shape[0]} rows to {loc_output}\n")
        
    except Exception as e:
        print(f"Error processing location data: {e}\n")

if __name__ == "__main__":
    clean_inventors_data()
