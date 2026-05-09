import json
import matplotlib.pyplot as plt
import os

def create_visualizations(json_path):
    output_dir = 'visualizations'
    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, 'r') as f:
        data = json.load(f)

    # 1. Top Inventors Bar Chart
    inventors = data.get('top_inventors', [])
    if inventors:
        names = [inv['name'] for inv in inventors]
        patents = [inv['patents'] for inv in inventors]
        
        plt.figure(figsize=(10, 6))
        plt.bar(names, patents, color='skyblue')
        plt.title('Top 5 Inventors by Patent Count')
        plt.xlabel('Inventor')
        plt.ylabel('Number of Patents')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'top_inventors.png'))
        plt.close()

    # 2. Top Companies Horizontal Bar Chart
    companies = data.get('top_companies', [])
    if companies:
        names = [comp['name'] for comp in companies]
        # Reverse to have the highest on top of the horizontal bar chart
        names.reverse()
        patents = [comp['patents'] for comp in companies]
        patents.reverse()
        
        plt.figure(figsize=(12, 6))
        plt.barh(names, patents, color='lightcoral')
        plt.title('Top 5 Companies by Patent Count')
        plt.xlabel('Number of Patents')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'top_companies.png'))
        plt.close()

    # 3. Top Countries Pie Chart
    countries = data.get('top_countries', [])
    if countries:
        labels = [c['country'] for c in countries]
        shares = [c['share'] for c in countries]
        
        # Calculate 'Other' if total share < 1.0
        total_share = sum(shares)
        if total_share < 1.0:
            labels.append('Other')
            shares.append(1.0 - total_share)
            
        plt.figure(figsize=(8, 8))
        plt.pie(shares, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title('Patent Share by Top Countries')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'top_countries_pie.png'))
        plt.close()
        
    print(f"Visualizations successfully generated in '{output_dir}' directory.")

if __name__ == "__main__":
    create_visualizations("summary_report.json")
