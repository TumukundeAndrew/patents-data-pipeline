import sqlite3
import json

def generate_report(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Total Patents
    cursor.execute("SELECT COUNT(DISTINCT patent_id) FROM patents;")
    total_patents = cursor.fetchone()[0]

    # 2. Top Inventors
    cursor.execute("""
        SELECT 
            disambig_inventor_name_first, 
            COUNT(DISTINCT patent_id) as total
        FROM inventors
        WHERE disambig_inventor_name_first IS NOT NULL AND disambig_inventor_name_first != ''
        GROUP BY inventor_id, disambig_inventor_name_first
        ORDER BY total DESC
        LIMIT 5;
    """)
    top_inventors = cursor.fetchall()

    # 3. Top Companies
    cursor.execute("""
        SELECT 
            disambig_assignee_organization, 
            COUNT(DISTINCT patent_id) as total
        FROM companies
        WHERE disambig_assignee_organization IS NOT NULL AND disambig_assignee_organization != ''
        GROUP BY assignee_id, disambig_assignee_organization
        ORDER BY total DESC
        LIMIT 5;
    """)
    top_companies = cursor.fetchall()

    # 4. Top Countries
    cursor.execute("""
        SELECT 
            l.disambig_country, 
            COUNT(DISTINCT i.patent_id) as total
        FROM inventors i
        JOIN locations l ON i.location_id = l.location_id
        WHERE l.disambig_country IS NOT NULL AND l.disambig_country != ''
        GROUP BY l.disambig_country
        ORDER BY total DESC
        LIMIT 5;
    """)
    top_countries = cursor.fetchall()
    
    # Calculate share for top countries
    cursor.execute("""
        SELECT COUNT(DISTINCT i.patent_id)
        FROM inventors i
        JOIN locations l ON i.location_id = l.location_id
        WHERE l.disambig_country IS NOT NULL AND l.disambig_country != ''
    """)
    total_country_patents = cursor.fetchone()[0]

    # --- Generate Console Report ---
    print("================== PATENT REPORT ===================")
    print(f"Total Patents: {total_patents:,}")
    
    print("\nTop Inventors:")
    for i, (name, count) in enumerate(top_inventors, 1):
        print(f"{i}. {name} - {count}")
        
    print("\nTop Companies:")
    for i, (name, count) in enumerate(top_companies, 1):
        print(f"{i}. {name} - {count:,}")
        
    print("\nTop Countries:")
    for i, (country, _) in enumerate(top_countries, 1):
        print(f"{i}. {country}")
    
    # --- Generate JSON Report ---
    json_data = {
        "total_patents": total_patents,
        "top_inventors": [{"name": name, "patents": count} for name, count in top_inventors],
        "top_companies": [{"name": name, "patents": count} for name, count in top_companies],
        "top_countries": [{"country": country, "share": round(count / total_country_patents, 4)} for country, count in top_countries]
    }

    with open("summary_report.json", "w") as f:
        json.dump(json_data, f, indent=4)
        
    print("\nReport successfully saved to 'summary_report.json'")

    conn.close()

if __name__ == "__main__":
    generate_report("patents_data.db")
