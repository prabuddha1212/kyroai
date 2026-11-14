-- ==============================================================================
-- StoreLab Supabase Database Migration & RLS Security Fix
-- Run this in your Supabase Dashboard: SQL Editor -> New Query -> Run
-- ==============================================================================

-- 1. Ensure 'products' table exists with is_active column
CREATE TABLE IF NOT EXISTS public.products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tagline TEXT,
    price INTEGER NOT NULL,
    original_price INTEGER,
    category TEXT,
    badge TEXT,
    image_url TEXT,
    description TEXT NOT NULL,
    features TEXT[] DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Ensure is_active column exists if table was previously created without it
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'products' AND column_name = 'is_active'
    ) THEN
        ALTER TABLE public.products ADD COLUMN is_active BOOLEAN DEFAULT true;
    END IF;
END $$;

-- 2. Ensure 'waitlist' table exists with 'name' and 'consent_given'
CREATE TABLE IF NOT EXISTS public.waitlist (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id TEXT NOT NULL,
    email TEXT NOT NULL,
    name TEXT DEFAULT '',
    consent_given BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Add 'name' column if missing
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'waitlist' AND column_name = 'name'
    ) THEN
        ALTER TABLE public.waitlist ADD COLUMN name TEXT DEFAULT '';
    END IF;
END $$;

-- Add 'consent_given' column if missing
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'waitlist' AND column_name = 'consent_given'
    ) THEN
        ALTER TABLE public.waitlist ADD COLUMN consent_given BOOLEAN DEFAULT true;
    END IF;
END $$;

-- Ensure UNIQUE constraint on (product_id, email) to prevent duplicate signups
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'waitlist_product_email_unique'
    ) THEN
        ALTER TABLE public.waitlist ADD CONSTRAINT waitlist_product_email_unique UNIQUE (product_id, email);
    END IF;
END $$;

-- 3. Ensure 'analytics_events' table exists
CREATE TABLE IF NOT EXISTS public.analytics_events (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_name TEXT NOT NULL,
    product_id TEXT,
    meta JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Enable Row Level Security (RLS) on all tables (NEVER DISABLED)
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.waitlist ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.analytics_events ENABLE ROW LEVEL SECURITY;

-- 5. Safe, Secure RLS Policies
-- Products: Anyone can read active products
DROP POLICY IF EXISTS "Allow public read access to active products" ON public.products;
CREATE POLICY "Allow public read access to active products"
    ON public.products FOR SELECT USING (is_active = true OR is_active IS NULL);

-- Waitlist: Anyone (anon key) can insert a new reservation
DROP POLICY IF EXISTS "Allow public insert into waitlist" ON public.waitlist;
CREATE POLICY "Allow public insert into waitlist"
    ON public.waitlist FOR INSERT WITH CHECK (true);

-- Waitlist: Anyone can read waitlist for aggregation (or backend service)
DROP POLICY IF EXISTS "Allow public read access to waitlist" ON public.waitlist;
CREATE POLICY "Allow public read access to waitlist"
    ON public.waitlist FOR SELECT USING (true);

-- Waitlist: Allow deletion (privacy requests)
DROP POLICY IF EXISTS "Allow public delete from waitlist" ON public.waitlist;
CREATE POLICY "Allow public delete from waitlist"
    ON public.waitlist FOR DELETE USING (true);

-- Analytics: Anyone can insert analytics events
DROP POLICY IF EXISTS "Allow public insert into analytics" ON public.analytics_events;
CREATE POLICY "Allow public insert into analytics"
    ON public.analytics_events FOR INSERT WITH CHECK (true);

-- Analytics: Allow reading for Owner Dashboard
DROP POLICY IF EXISTS "Allow public read access to analytics" ON public.analytics_events;
CREATE POLICY "Allow public read access to analytics"
    ON public.analytics_events FOR SELECT USING (true);

-- 6. Seed / Upsert the 4 concept products
INSERT INTO public.products (id, name, tagline, price, original_price, category, badge, image_url, description, features, is_active)
VALUES
(
    'desk-mat',
    'Pure Black Desk Mat (XXL)',
    'Spacious water-resistant surface with anti-fray stitching',
    799,
    999,
    'Surface',
    'Early Bird',
    'https://images.unsplash.com/photo-1616440347437-b1c73416efc2?auto=format&fit=crop&w=800&q=80',
    'Engineered for precision tracking and desk protection. Premium micro-textured cloth with high-density stitched borders and non-slip rubber backing.',
    ARRAY['900mm x 400mm x 4mm', 'Water-resistant coating', 'Non-slip rubber base'],
    true
),
(
    'headphone-stand',
    'Solid Aluminum Headphone Stand',
    'Minimalist weighted cradle for premium audio gear',
    599,
    799,
    'Organizer',
    'Popular',
    'https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=800&q=80',
    'Keep your desk clutter-free while protecting your headband. CNC-milled aluminum with curved silicone rest and anti-slip silicone feet.',
    ARRAY['Weighted steel base', 'Curved protective silicone', 'Matte anodized black finish'],
    true
),
(
    'cable-kit',
    'Zen Magnetic Cable Management Pack',
    'Magnetic clips & routing channels to tame loose wires',
    399,
    599,
    'Cables',
    'Essential',
    'https://images.unsplash.com/photo-1588508065123-287b28e013da?auto=format&fit=crop&w=800&q=80',
    'Eliminate charging cable drop-offs and messy desktop wires. Magnetic snap collars attach to desk edge mount strips for single-handed docking.',
    ARRAY['5x Magnetic clips', '3x Under-desk channels', 'Damage-free 3M adhesive'],
    true
),
(
    'keyboard',
    'Custom 75% Mechanical Keyboard',
    'Hot-swappable linear switches with acoustic dampening',
    2999,
    3999,
    'Hardware',
    'Flagship',
    'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80',
    'Pre-lubed smooth linear switches, sound-dampening silicone gaskets, and per-key RGB in a compact 75% desk-saving layout.',
    ARRAY['Hot-swappable 5-pin sockets', 'Gasket-mounted acoustic dampening', 'Detachable braided Type-C'],
    true
)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    tagline = EXCLUDED.tagline,
    price = EXCLUDED.price,
    original_price = EXCLUDED.original_price,
    category = EXCLUDED.category,
    badge = EXCLUDED.badge,
    image_url = EXCLUDED.image_url,
    description = EXCLUDED.description,
    features = EXCLUDED.features,
    is_active = true;
