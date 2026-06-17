import unittest

from fastapi import HTTPException

from authorization import check_post_owner, check_profile_owner


class FakeCursor:
    def __init__(self, row):
        self.row = row
        self.query = None
        self.params = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query, params):
        self.query = query
        self.params = params

    def fetchone(self):
        return self.row


class FakeConnection:
    def __init__(self, row):
        self.cursor_obj = FakeCursor(row)

    def cursor(self):
        return self.cursor_obj


class AuthorizationTests(unittest.TestCase):
    def test_profile_owner_allows_matching_user(self):
        check_profile_owner(FakeConnection(("user-1",)), "profile-1", "user-1")

    def test_profile_owner_rejects_missing_profile(self):
        with self.assertRaises(HTTPException) as ctx:
            check_profile_owner(FakeConnection(None), "profile-1", "user-1")

        self.assertEqual(ctx.exception.status_code, 404)

    def test_profile_owner_rejects_different_user(self):
        with self.assertRaises(HTTPException) as ctx:
            check_profile_owner(FakeConnection(("user-2",)), "profile-1", "user-1")

        self.assertEqual(ctx.exception.status_code, 403)

    def test_post_owner_allows_matching_user(self):
        check_post_owner(FakeConnection(("user-1",)), "post-1", "user-1")

    def test_post_owner_rejects_missing_post(self):
        with self.assertRaises(HTTPException) as ctx:
            check_post_owner(FakeConnection(None), "post-1", "user-1")

        self.assertEqual(ctx.exception.status_code, 404)

    def test_post_owner_rejects_different_user(self):
        with self.assertRaises(HTTPException) as ctx:
            check_post_owner(FakeConnection(("user-2",)), "post-1", "user-1")

        self.assertEqual(ctx.exception.status_code, 403)


if __name__ == "__main__":
    unittest.main()
