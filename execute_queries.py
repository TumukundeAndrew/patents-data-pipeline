import sqlite3
import pandas as pd
import json
import os

def execute_and_export_queries(db_path, sql_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # Read the SQL file
    with open(sql_file, 'r') as file:
        sql_script = file.read()
    
    # Split the script into separate queries based on the double semicolon or custom parsing
    # Since our queries are separated by semicolons and have comments, let's extract them manually or using pandas read_sql
    # A robust way is to split by ';' and filter out empty strings, but for complex queries with CTEs we must be careful.
    
    queries = {
        "top_inventors": """
            SELECT 
                inventor_id, 
                disambig_inventor_name_first, 
                COUNT(DISTINCT patent_id) as total_patents
            FROM 
                inventors
            WHERE
                inventor_id IS NOT NULL AND inventor_id != ''
            GROUP BY 
                inventor_id, 
                disambig_inventor_name_first
            ORDER BY 
                total_patents DESC
            LIMIT 10;
        """,
        "top_companies": """
            SELECT 
                assignee_id, 
                disambig_assignee_organization, 
                COUNT(DISTINCT patent_id) as total_patents
            FROM 
                companies
            WHERE
                assignee_id IS NOT NULL AND assignee_id != ''
            GROUP BY 
                assignee_id, 
                disambig_assignee_organization
            ORDER BY 
                total_patents DESC
            LIMIT 10;
        """,
        "top_countries": """
            SELECT 
                l.disambig_country, 
                COUNT(DISTINCT i.patent_id) as total_patents
            FROM 
                inventors i
            JOIN 
                locations l ON i.location_id = l.location_id
            WHERE
                l.disambig_country IS NOT NULL AND l.disambig_country != ''
            GROUP BY 
                l.disambig_country
            ORDER BY 
                total_patents DESC
            LIMIT 10;
        """,
        "trends_over_time": """
            SELECT 
                strftime('%Y', patent_date) as patent_year,
                COUNT(DISTINCT patent_id) as total_patents
            FROM 
                patents
            WHERE 
                patent_date IS NOT NULL
            GROUP BY 
                patent_year
            ORDER BY 
                patent_year DESC;
        """,
        "inventors_ranking": """
            SELECT 
                inventor_id, 
                disambig_inventor_name_first, 
                total_patents,
                RANK() OVER(ORDER BY total_patents DESC) as inventor_rank,
                DENSE_RANK() OVER(ORDER BY total_patents DESC) as inventor_dense_rank
            FROM (
                SELECT 
                    inventor_id, 
                    disambig_inventor_name_first, 
                    COUNT(DISTINCT patent_id) as total_patents
                FROM 
                    inventors
                WHERE
                    inventor_id IS NOT NULL AND inventor_id != ''
                GROUP BY 
                    inventor_id, 
                    disambig_inventor_name_first
            )
            ORDER BY 
                inventor_rank
            LIMIT 20;
        """,
        "complex_cte_query": """
            WITH CountryPatentCounts AS (
                SELECT 
                    l.disambig_country,
                    COUNT(DISTINCT i.patent_id) as country_total_patents
                FROM 
                    inventors i
                JOIN 
                    locations l ON i.location_id = l.location_id
                WHERE
                    l.disambig_country IS NOT NULL AND l.disambig_country != ''
                GROUP BY 
                    l.disambig_country
            ),
            TopCountries AS (
                SELECT 
                    disambig_country
                FROM 
                    CountryPatentCounts
                ORDER BY 
                    country_total_patents DESC
                LIMIT 3
            ),
            CompanyPatentsByCountry AS (
                SELECT 
                    l.disambig_country,
                    c.disambig_assignee_organization,
                    COUNT(DISTINCT c.patent_id) as company_patents
                FROM 
                    companies c
                JOIN 
                    inventors i ON c.patent_id = i.patent_id
                JOIN 
                    locations l ON i.location_id = l.location_id
                WHERE
                    c.disambig_assignee_organization IS NOT NULL AND c.disambig_assignee_organization != ''
                GROUP BY 
                    l.disambig_country,
                    c.disambig_assignee_organization
            ),
            RankedCompaniesByCountry AS (
                SELECT 
                    cpbc.disambig_country,
                    cpbc.disambig_assignee_organization,
                    cpbc.company_patents,
                    ROW_NUMBER() OVER(PARTITION BY cpbc.disambig_country ORDER BY cpbc.company_patents DESC) as company_rank
                FROM 
                    CompanyPatentsByCountry cpbc
                JOIN 
                    TopCountries tc ON cpbc.disambig_country = tc.disambig_country
            )
            SELECT 
                disambig_country,
                disambig_assignee_organization as top_company,
                company_patents
            FROM 
                RankedCompaniesByCountry
            WHERE 
                company_rank = 1
            ORDER BY 
                company_patents DESC;
        """,
        "patent_table": """
            SELECT 
                p.patent_id,
                p.patent_title,
                p.patent_date,
                a.filing_date,
                pa.abstract
            FROM 
                patents p
            LEFT JOIN 
                applications a ON p.patent_id = a.patent_id
            LEFT JOIN 
                patent_abstracts pa ON p.patent_id = pa.patent_id
            LIMIT 20;
        """,
        "inventor_table": """
            SELECT 
                i.patent_id,
                i.inventor_id,
                i.disambig_inventor_name_first,
                i.location_id,
                l.disambig_country
            FROM 
                inventors i
            LEFT JOIN 
                locations l ON i.location_id = l.location_id
            LIMIT 20;
        """
    }

    output_dir = 'reports'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Executing queries on {db_path} and generating reports...\n")

    for query_name, query_sql in queries.items():
        print(f"--- Running {query_name} ---")
        try:
            # Execute query and load into pandas DataFrame
            df = pd.read_sql_query(query_sql, conn)
            
            # Export to CSV
            csv_path = os.path.join(output_dir, f"{query_name}.csv")
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            # Export to JSON
            json_path = os.path.join(output_dir, f"{query_name}.json")
            df.to_json(json_path, orient='records', indent=4)
            
            # Print to console safely
            try:
                print(df.to_string(index=False))
            except UnicodeEncodeError:
                print(df.to_string(index=False).encode('cp1252', errors='replace').decode('cp1252'))
            print("\n")
            
        except Exception as e:
            print(f"Error executing {query_name}: {e}")
            
    print(f"All reports have been successfully exported to the '{output_dir}' directory.")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    db_file = "patents_data.db"
    sql_file = "queries.sql"
    execute_and_export_queries(db_file, sql_file)
