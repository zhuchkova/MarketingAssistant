ALTER TABLE audience_analyses
ALTER COLUMN pains TYPE JSONB
USING (
    CASE
        WHEN pains IS NULL THEN NULL
        WHEN pains LIKE '[%' THEN pains::jsonb
        ELSE to_jsonb(string_to_array(pains, ';'))
    END
),

ALTER COLUMN desires TYPE JSONB
USING (
    CASE
        WHEN desires IS NULL THEN NULL
        WHEN desires LIKE '[%' THEN desires::jsonb
        ELSE to_jsonb(string_to_array(desires, ';'))
    END
),

ALTER COLUMN objections TYPE JSONB
USING (
    CASE
        WHEN objections IS NULL THEN NULL
        WHEN objections LIKE '[%' THEN objections::jsonb
        ELSE to_jsonb(string_to_array(objections, ';'))
    END
),

ALTER COLUMN content_angles TYPE JSONB
USING (
    CASE
        WHEN content_angles IS NULL THEN NULL
        WHEN content_angles LIKE '[%' THEN content_angles::jsonb
        ELSE to_jsonb(string_to_array(content_angles, ';'))
    END
);