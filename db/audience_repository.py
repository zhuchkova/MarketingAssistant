import uuid
from psycopg.types.json import Json

def save_audience_analysis(conn, profile_id, data):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO audience_analyses (id,
                                                   user_profile_id,
                                                   audience_profile,
                                                   pains,
                                                   desires,
                                                   objections,
                                                   trigger_moments,
                                                   proof_points,
                                                   audience_language,
                                                   content_angles,
                                                   tone,
                                                   positioning,
                                                   known_for)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        str(uuid.uuid4()),
                        profile_id,
                        data["audience_profile"],
                        Json(data["pains"]),
                        Json(data["desires"]),
                        Json(data["objections"]),
                        Json(data.get("trigger_moments", [])),
                        Json(data.get("proof_points", [])),
                        Json(data.get("audience_language", [])),
                        Json(data["content_angles"]),
                        data["tone"],
                        data["positioning"],
                        data["known_for"],
                    ))
