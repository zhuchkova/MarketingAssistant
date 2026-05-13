# python scripts/migrate.py
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import psycopg

DB_URL = os.getenv("DATABASE_URL", "postgresql://app:app@localhost:5432/appdb")
MIGRATIONS_DIR = Path("migrations")

print("Migrating DB_URL =", DB_URL)


def split_sql(sql: str) -> list[str]:
    """
    Very small SQL splitter good enough for typical migration files.
    It respects single-quoted strings and dollar-quoted blocks ($$...$$ or $tag$...$tag$).
    """
    statements = []
    buf = []

    i = 0
    in_single = False
    dollar_tag = None  # e.g. "$$" or "$func$"

    while i < len(sql):
        ch = sql[i]

        # Handle single quotes
        if dollar_tag is None and ch == "'" and not in_single:
            in_single = True
            buf.append(ch)
            i += 1
            continue
        elif dollar_tag is None and ch == "'" and in_single:
            # Check escaped quote ''
            if i + 1 < len(sql) and sql[i + 1] == "'":
                buf.append("''")
                i += 2
                continue
            in_single = False
            buf.append(ch)
            i += 1
            continue

        # Handle dollar-quoted strings: $tag$ ... $tag$
        if not in_single and ch == "$":
            # Try to read tag
            j = i + 1
            while j < len(sql) and (sql[j].isalnum() or sql[j] == "_"):
                j += 1
            if j < len(sql) and sql[j] == "$":
                tag = sql[i : j + 1]  # includes both $ signs
                if dollar_tag is None:
                    dollar_tag = tag
                elif dollar_tag == tag:
                    dollar_tag = None
                buf.append(tag)
                i = j + 1
                continue

        # Split on semicolon only when not inside strings
        if ch == ";" and not in_single and dollar_tag is None:
            stmt = "".join(buf).strip()
            if stmt:
                statements.append(stmt)
            buf = []
            i += 1
            continue

        buf.append(ch)
        i += 1

    tail = "".join(buf).strip()
    if tail:
        statements.append(tail)

    return statements


def main() -> None:
    if not MIGRATIONS_DIR.exists():
        raise SystemExit(f"Missing migrations directory: {MIGRATIONS_DIR.resolve()}")

    with psycopg.connect(DB_URL) as conn:
        # Ensure migrations table exists
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version TEXT PRIMARY KEY,
                    applied_at TIMESTAMP NOT NULL DEFAULT now()
                );
                """
            )
            conn.commit()

        # Load applied versions
        with conn.cursor() as cur:
            cur.execute("SELECT version FROM schema_migrations")
            applied = {row[0] for row in cur.fetchall()}

        # Apply new migrations (each file = one transaction)
        for file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            version = file.name
            if version in applied:
                continue

            sql_text = file.read_text(encoding="utf-8")
            statements = split_sql(sql_text)

            if not statements:
                # Empty file; still mark applied
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO schema_migrations (version) VALUES (%s)",
                        (version,),
                    )
                    conn.commit()
                print(f"Applied (empty) {version}")
                continue

            print(f"Applying {version} ({len(statements)} statements)")

            try:
                with conn.cursor() as cur:
                    for stmt in statements:
                        cur.execute(stmt)
                    cur.execute(
                        "INSERT INTO schema_migrations (version) VALUES (%s)",
                        (version,),
                    )
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    print("Migrations complete")


if __name__ == "__main__":
    main()