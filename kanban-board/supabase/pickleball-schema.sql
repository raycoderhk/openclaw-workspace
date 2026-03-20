-- Pickleball Court Tracker Schema
-- Run this in Supabase SQL Editor

-- ============================================
-- 1. Courts Table (球場主表)
-- ============================================
CREATE TABLE IF NOT EXISTS pickleball_courts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    address TEXT,
    district TEXT,
    court_type TEXT CHECK (court_type IN ('indoor', 'outdoor')),
    surface_type TEXT,
    lighting TEXT,
    price_range TEXT CHECK (price_range IN ('$', '$$', '$$$')),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    noise_level TEXT CHECK (noise_level IN ('quiet', 'moderate', 'loud')),
    facilities TEXT[],
    phone TEXT,
    website TEXT,
    google_maps_url TEXT,
    notes TEXT,
    is_wishlist BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 2. Court Photos Table (球場照片)
-- ============================================
CREATE TABLE IF NOT EXISTS pickleball_court_photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    court_id UUID REFERENCES pickleball_courts(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    photo_url TEXT NOT NULL,
    caption TEXT,
    photo_type TEXT CHECK (photo_type IN ('court_view', 'facility', 'action_shot', 'other')),
    is_from_friend BOOLEAN DEFAULT false,
    friend_name TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 3. Visits Table (打波記錄)
-- ============================================
CREATE TABLE IF NOT EXISTS pickleball_visits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    court_id UUID REFERENCES pickleball_courts(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    visit_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    duration_minutes INTEGER,
    players TEXT[],
    session_type TEXT CHECK (session_type IN ('social', 'training', 'coaching', 'tournament')),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- 4. Comments Table (評論/心得)
-- ============================================
CREATE TABLE IF NOT EXISTS pickleball_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    court_id UUID REFERENCES pickleball_courts(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    comment_text TEXT NOT NULL,
    comment_type TEXT CHECK (comment_type IN ('review', 'tip', 'warning', 'update')),
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================
-- Row Level Security (RLS)
-- ============================================
ALTER TABLE pickleball_courts ENABLE ROW LEVEL SECURITY;
ALTER TABLE pickleball_court_photos ENABLE ROW LEVEL SECURITY;
ALTER TABLE pickleball_visits ENABLE ROW LEVEL SECURITY;
ALTER TABLE pickleball_comments ENABLE ROW LEVEL SECURITY;

-- Courts Policies
CREATE POLICY "Users can view own courts" ON pickleball_courts
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own courts" ON pickleball_courts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own courts" ON pickleball_courts
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own courts" ON pickleball_courts
    FOR DELETE USING (auth.uid() = user_id);

-- Photos Policies
CREATE POLICY "Users can view own photos" ON pickleball_court_photos
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own photos" ON pickleball_court_photos
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own photos" ON pickleball_court_photos
    FOR DELETE USING (auth.uid() = user_id);

-- Visits Policies
CREATE POLICY "Users can view own visits" ON pickleball_visits
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own visits" ON pickleball_visits
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own visits" ON pickleball_visits
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own visits" ON pickleball_visits
    FOR DELETE USING (auth.uid() = user_id);

-- Comments Policies
CREATE POLICY "Users can view own comments" ON pickleball_comments
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own comments" ON pickleball_comments
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own comments" ON pickleball_comments
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own comments" ON pickleball_comments
    FOR DELETE USING (auth.uid() = user_id);

-- ============================================
-- Indexes (for performance)
-- ============================================
CREATE INDEX IF NOT EXISTS idx_courts_user_id ON pickleball_courts(user_id);
CREATE INDEX IF NOT EXISTS idx_courts_district ON pickleball_courts(district);
CREATE INDEX IF NOT EXISTS idx_courts_wishlist ON pickleball_courts(is_wishlist);
CREATE INDEX IF NOT EXISTS idx_photos_court_id ON pickleball_court_photos(court_id);
CREATE INDEX IF NOT EXISTS idx_visits_court_id ON pickleball_visits(court_id);
CREATE INDEX IF NOT EXISTS idx_visits_date ON pickleball_visits(visit_date);
CREATE INDEX IF NOT EXISTS idx_comments_court_id ON pickleball_comments(court_id);

-- ============================================
-- Storage Bucket (run in Supabase Dashboard UI)
-- ============================================
-- Go to Storage → Create Bucket
-- Bucket name: pickleball-photos
-- Public: false
-- File size limit: 5242880 (5MB)

-- ============================================
-- Storage Policies (run after creating bucket)
-- ============================================
-- Policy 1: Users can upload to their own folder
CREATE POLICY "Users can upload own photos"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'pickleball-photos'
    AND auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy 2: Users can view their own photos
CREATE POLICY "Users can view own photos"
ON storage.objects FOR SELECT
USING (
    bucket_id = 'pickleball-photos'
    AND auth.uid()::text = (storage.foldername(name))[1]
);

-- Policy 3: Users can delete their own photos
CREATE POLICY "Users can delete own photos"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'pickleball-photos'
    AND auth.uid()::text = (storage.foldername(name))[1]
);
