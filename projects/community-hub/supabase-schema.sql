-- Community Tips Database Schema
-- For 愉城社區 / 愉景新城 WhatsApp chat extraction

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Main table: community tips
CREATE TABLE IF NOT EXISTS community_tips (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    msg_date        DATE NOT NULL,
    msg_time        TIME NOT NULL,
    datetime        TIMESTAMPTZ NOT NULL,
    sender          TEXT NOT NULL,
    raw_text        TEXT NOT NULL,
    category        TEXT NOT NULL,
    useful          BOOLEAN DEFAULT true,
    summary_en      TEXT,
    summary_zh      TEXT,  -- Optional Chinese summary
    entities        JSONB DEFAULT '[]'::jsonb,
    language        TEXT CHECK (language IN ('zh', 'en', 'mixed')),
    source          TEXT DEFAULT 'whatsapp_export',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_tips_category ON community_tips(category);
CREATE INDEX IF NOT EXISTS idx_tips_date ON community_tips(msg_date);
CREATE INDEX IF NOT EXISTS idx_tips_datetime ON community_tips(datetime);
CREATE INDEX IF NOT EXISTS idx_tips_useful ON community_tips(useful) WHERE useful = true;
CREATE INDEX IF NOT EXISTS idx_tips_entities ON community_tips USING GIN(entities);
CREATE INDEX IF NOT EXISTS idx_tips_search ON community_tips USING GIN(to_tsvector('simple', raw_text));

-- Categories enum (for reference)
-- traffic, restaurant, doctor, tech_tip, shopping, service, community, event, news, repair, education, childcare

-- View: Latest useful tips by category
CREATE OR REPLACE VIEW latest_tips_by_category AS
SELECT DISTINCT ON (category)
    category,
    id,
    msg_date,
    sender,
    summary_en,
    entities,
    raw_text
FROM community_tips
WHERE useful = true
ORDER BY category, msg_date DESC, datetime DESC;

-- View: Recent tips (last 7 days)
CREATE OR REPLACE VIEW recent_tips AS
SELECT *
FROM community_tips
WHERE useful = true
  AND datetime >= NOW() - INTERVAL '7 days'
ORDER BY datetime DESC;

-- Function: Search tips by keyword
CREATE OR REPLACE FUNCTION search_tips(query_text TEXT, category_filter TEXT DEFAULT NULL)
RETURNS TABLE(
    id UUID,
    msg_date DATE,
    sender TEXT,
    summary_en TEXT,
    raw_text TEXT,
    category TEXT,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id,
        t.msg_date,
        t.sender,
        t.summary_en,
        t.raw_text,
        t.category,
        ts_rank(to_tsvector('simple', t.raw_text), plainto_tsquery('simple', query_text)) AS rank
    FROM community_tips t
    WHERE t.useful = true
      AND (category_filter IS NULL OR t.category = category_filter)
      AND to_tsvector('simple', t.raw_text) @@ plainto_tsquery('simple', query_text)
    ORDER BY rank DESC
    LIMIT 50;
END;
$$ LANGUAGE plpgsql;

-- Function: Get tips by category with pagination
CREATE OR REPLACE FUNCTION get_tips_by_category(
    cat TEXT,
    page_num INTEGER DEFAULT 1,
    page_size INTEGER DEFAULT 20
)
RETURNS TABLE(
    id UUID,
    msg_date DATE,
    msg_time TIME,
    sender TEXT,
    summary_en TEXT,
    entities JSONB,
    raw_text TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id,
        t.msg_date,
        t.msg_time,
        t.sender,
        t.summary_en,
        t.entities,
        t.raw_text
    FROM community_tips t
    WHERE t.useful = true
      AND t.category = cat
    ORDER BY t.datetime DESC
    LIMIT page_size
    OFFSET (page_num - 1) * page_size;
END;
$$ LANGUAGE plpgsql;

-- Statistics view
CREATE OR REPLACE VIEW tips_stats AS
SELECT
    category,
    COUNT(*) AS total_count,
    COUNT(*) FILTER (WHERE datetime >= NOW() - INTERVAL '30 days') AS last_30_days,
    COUNT(*) FILTER (WHERE datetime >= NOW() - INTERVAL '7 days') AS last_7_days,
    MAX(datetime) AS latest_tip,
    MIN(datetime) AS earliest_tip
FROM community_tips
WHERE useful = true
GROUP BY category
ORDER BY total_count DESC;

-- Row Level Security (if you want multi-user support)
ALTER TABLE community_tips ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public read (for now, can restrict later)
CREATE POLICY "Allow public read access" ON community_tips
    FOR SELECT USING (true);

-- Policy: Allow authenticated users to insert
CREATE POLICY "Allow authenticated insert" ON community_tips
    FOR INSERT WITH CHECK (true);

-- Grant permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO PUBLIC;
GRANT SELECT ON ALL VIEWS IN SCHEMA public TO PUBLIC;
