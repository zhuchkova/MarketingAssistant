from fastapi import HTTPException


def check_profile_owner(conn, profile_id: str, user_id: str):
    with conn.cursor() as cur:
        cur.execute("SELECT user_id FROM user_profiles WHERE id = %s", (profile_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Profile not found")
    if str(row[0]) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")


def check_post_owner(conn, post_id: str, user_id: str):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT up.user_id
            FROM posts p
            JOIN user_profiles up ON p.user_profile_id = up.id
            WHERE p.id = %s
        """, (post_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Post not found")
    if str(row[0]) != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
