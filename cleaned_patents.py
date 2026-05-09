import pandas as pd
import os

def clean_patents_data():
    base_dir = r"d:\cloud assignment\patents"
    
    # 1. Clean g_application_100k.tsv
    print("--- Cleaning g_application_100k.tsv ---")
    app_input = os.path.join(base_dir, "g_application_100k.tsv")
    app_output = os.path.join(base_dir, "cleaned_application.csv")
    
    try:
        df_app = pd.read_csv(app_input, sep='\t', low_memory=False)
        app_cols = ['patent_id', 'filing_date']
        
        existing_app_cols = [col for col in app_cols if col in df_app.columns]
        missing_app_cols = [col for col in app_cols if col not in df_app.columns]
        if missing_app_cols:
            print(f"Warning: Missing columns in application data: {missing_app_cols}")
            
        df_app_cleaned = df_app[existing_app_cols].copy()
        
        # Drop rows missing essential identifiers
        if 'patent_id' in df_app_cleaned.columns:
            df_app_cleaned.dropna(subset=['patent_id'], inplace=True)
            
        # Optional: strip whitespace
        for col in df_app_cleaned.select_dtypes(include=['object']).columns:
            df_app_cleaned[col] = df_app_cleaned[col].str.strip()
            
        df_app_cleaned.drop_duplicates(inplace=True)
        df_app_cleaned.to_csv(app_output, sep=',', index=False)
        print(f"Saved {df_app_cleaned.shape[0]} rows to {app_output}\n")
        
    except Exception as e:
        print(f"Error processing application data: {e}\n")

    # 2. Clean g_patent_100k.tsv
    print("--- Cleaning g_patent_100k.tsv ---")
    pat_input = os.path.join(base_dir, "g_patent_100k.tsv")
    pat_output = os.path.join(base_dir, "cleaned_patent.csv")
    
    try:
        df_pat = pd.read_csv(pat_input, sep='\t', low_memory=False)
        pat_cols = ['patent_id', 'patent_title', 'patent_date']
        
        existing_pat_cols = [col for col in pat_cols if col in df_pat.columns]
        missing_pat_cols = [col for col in pat_cols if col not in df_pat.columns]
        if missing_pat_cols:
            print(f"Warning: Missing columns in patent data: {missing_pat_cols}")
            
        df_pat_cleaned = df_pat[existing_pat_cols].copy()
        
        if 'patent_id' in df_pat_cleaned.columns:
            df_pat_cleaned.dropna(subset=['patent_id'], inplace=True)
            
        if 'patent_title' in df_pat_cleaned.columns:
            df_pat_cleaned['patent_title'] = df_pat_cleaned['patent_title'].fillna('Unknown Title')
            
        # Optional: strip whitespace
        for col in df_pat_cleaned.select_dtypes(include=['object']).columns:
            df_pat_cleaned[col] = df_pat_cleaned[col].str.strip()
            
        df_pat_cleaned.drop_duplicates(inplace=True)
        df_pat_cleaned.to_csv(pat_output, sep=',', index=False)
        print(f"Saved {df_pat_cleaned.shape[0]} rows to {pat_output}\n")
        
    except Exception as e:
        print(f"Error processing patent data: {e}\n")

    # 3. Clean g_patent_abstract_100k.tsv
    print("--- Cleaning g_patent_abstract_100k.tsv ---")
    abs_input = os.path.join(base_dir, "g_patent_abstract_100k.tsv")
    abs_output = os.path.join(base_dir, "cleaned_patent_abstract.csv")
    
    try:
        df_abs = pd.read_csv(abs_input, sep='\t', low_memory=False)
        # Handle cases where the column might be named 'patent_abstract' instead of 'abstract'
        abs_cols = ['patent_id', 'abstract']
        if 'patent_abstract' in df_abs.columns and 'abstract' not in df_abs.columns:
            df_abs.rename(columns={'patent_abstract': 'abstract'}, inplace=True)
            
        existing_abs_cols = [col for col in abs_cols if col in df_abs.columns]
        missing_abs_cols = [col for col in abs_cols if col not in df_abs.columns]
        if missing_abs_cols:
            print(f"Warning: Missing columns in abstract data: {missing_abs_cols}")
            
        df_abs_cleaned = df_abs[existing_abs_cols].copy()
        
        if 'patent_id' in df_abs_cleaned.columns:
            df_abs_cleaned.dropna(subset=['patent_id'], inplace=True)
            
        if 'abstract' in df_abs_cleaned.columns:
            df_abs_cleaned['abstract'] = df_abs_cleaned['abstract'].fillna('No abstract available')
            
        # Optional: strip whitespace
        for col in df_abs_cleaned.select_dtypes(include=['object']).columns:
            df_abs_cleaned[col] = df_abs_cleaned[col].str.strip()
            
        df_abs_cleaned.drop_duplicates(inplace=True)
        df_abs_cleaned.to_csv(abs_output, sep=',', index=False)
        print(f"Saved {df_abs_cleaned.shape[0]} rows to {abs_output}\n")
        
    except Exception as e:
        print(f"Error processing patent abstract data: {e}\n")

if __name__ == "__main__":
    clean_patents_data()
