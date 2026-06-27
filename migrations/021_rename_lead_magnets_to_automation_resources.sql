DO $$
BEGIN
    IF to_regclass('public.automation_resources') IS NULL
       AND to_regclass('public.lead_magnets') IS NOT NULL THEN
        ALTER TABLE lead_magnets RENAME TO automation_resources;
    END IF;
END $$;

DO $$
BEGIN
    IF to_regclass('public.automation_resources') IS NOT NULL THEN
        UPDATE automation_resources
        SET manychat_setup = manychat_setup
            - 'lead_magnet_url'
            - 'lead_magnet_used'
            || jsonb_build_object(
                'automation_resource_url',
                COALESCE(manychat_setup->>'automation_resource_url', manychat_setup->>'lead_magnet_url', ''),
                'resource_used',
                CASE
                    WHEN manychat_setup ? 'resource_used' THEN (manychat_setup->>'resource_used')::boolean
                    WHEN manychat_setup ? 'lead_magnet_used' THEN (manychat_setup->>'lead_magnet_used')::boolean
                    ELSE false
                END
            )
        WHERE manychat_setup ? 'lead_magnet_url'
           OR manychat_setup ? 'lead_magnet_used';
    END IF;
END $$;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'posts'
          AND column_name = 'lead_magnet_id'
    )
    AND NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'posts'
          AND column_name = 'automation_resource_id'
    ) THEN
        ALTER TABLE posts RENAME COLUMN lead_magnet_id TO automation_resource_id;
    ELSIF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'posts'
          AND column_name = 'lead_magnet_id'
    )
    AND EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'posts'
          AND column_name = 'automation_resource_id'
    ) THEN
        UPDATE posts
        SET automation_resource_id = COALESCE(automation_resource_id, lead_magnet_id);

        ALTER TABLE posts DROP COLUMN lead_magnet_id;
    END IF;
END $$;
