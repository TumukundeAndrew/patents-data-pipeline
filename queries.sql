-- queries.sql
-- Contains various SQL queries to analyze the Patents Database

-- 1. Top inventors (who has the most patents)
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

-- 2. Top companies (which companies own the most patents)
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

-- 3. Countries producing the most patents
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

-- 4. Trends over time (how many patents are created each year)
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

-- 5. Ranking query which ranks inventors using window functions
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

-- 6. CTE query (WITH statement) breaking a complex query into steps
-- Complex Query: Find the top 3 countries with the most patents, 
-- and for each of those countries, find their top company and the number of patents that company has.
WITH CountryPatentCounts AS (
    -- Step 1: Find total patents per country
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
    -- Step 2: Get the top 3 countries
    SELECT 
        disambig_country
    FROM 
        CountryPatentCounts
    ORDER BY 
        country_total_patents DESC
    LIMIT 3
),
CompanyPatentsByCountry AS (
    -- Step 3: Count patents per company per country
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
    -- Step 4: Rank companies within those countries
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
-- Step 5: Final selection of the top company in each of the top 3 countries
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

-- 7. Join patents, applications, and patent_abstracts to form "Patent" table
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

-- 8. Join inventors and locations to form "Inventor" table
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
