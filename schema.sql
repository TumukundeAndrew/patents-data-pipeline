-- schema.sql
-- Schema definition for the Patents Database

CREATE TABLE IF NOT EXISTS companies (
    patent_id TEXT,
    assignee_id TEXT,
    disambig_assignee_organization TEXT
);

CREATE TABLE IF NOT EXISTS inventors (
    patent_id TEXT,
    inventor_id TEXT,
    disambig_inventor_name_first TEXT,
    location_id TEXT
);

CREATE TABLE IF NOT EXISTS locations (
    location_id TEXT,
    disambig_country TEXT
);

CREATE TABLE IF NOT EXISTS applications (
    patent_id TEXT,
    filing_date DATE
);

CREATE TABLE IF NOT EXISTS patents (
    patent_id TEXT PRIMARY KEY,
    patent_title TEXT,
    patent_date DATE
);

CREATE TABLE IF NOT EXISTS patent_abstracts (
    patent_id TEXT,
    abstract TEXT
);

-- Basic indexing to improve join performance
CREATE INDEX IF NOT EXISTS idx_companies_patent_id ON companies(patent_id);
CREATE INDEX IF NOT EXISTS idx_inventors_patent_id ON inventors(patent_id);
CREATE INDEX IF NOT EXISTS idx_locations_location_id ON locations(location_id);
CREATE INDEX IF NOT EXISTS idx_applications_patent_id ON applications(patent_id);
CREATE INDEX IF NOT EXISTS idx_patent_abstracts_patent_id ON patent_abstracts(patent_id);

CREATE TABLE IF NOT EXISTS relationships (
    patent_id TEXT,
    inventor_id TEXT,
    assignee_id TEXT
);
CREATE INDEX IF NOT EXISTS idx_relationships_patent_id ON relationships(patent_id);
