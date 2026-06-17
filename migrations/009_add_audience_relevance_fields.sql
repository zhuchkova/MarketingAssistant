ALTER TABLE audience_analyses
    ADD COLUMN IF NOT EXISTS trigger_moments JSONB DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS proof_points JSONB DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS audience_language JSONB DEFAULT '[]'::jsonb;
