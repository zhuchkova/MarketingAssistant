import unittest

from pydantic import ValidationError

from schemas.auth import LoginRequest, RegisterRequest
from schemas.post_generation import GeneratePostRequest
from schemas.user_profile import CreateUserProfileRequest


class ValidationTests(unittest.TestCase):
    def test_register_normalizes_email(self):
        request = RegisterRequest(
            email=" Creator@Example.COM ",
            password="secure-password",
            name=" Creator ",
        )

        self.assertEqual(request.email, "creator@example.com")
        self.assertEqual(request.name, "Creator")

    def test_register_rejects_short_password(self):
        with self.assertRaises(ValidationError):
            RegisterRequest(email="creator@example.com", password="short", name="Creator")

    def test_login_rejects_invalid_email(self):
        with self.assertRaises(ValidationError):
            LoginRequest(email="not-an-email", password="secure-password")

    def test_profile_id_is_optional(self):
        request = CreateUserProfileRequest(
            profile_name="AI Founder",
            niche="AI automation",
            offer="AI workflows",
            target_audience="Founders",
            expertise="ML engineering",
            tone="Practical",
            goal="Generate leads",
        )

        self.assertIsNone(request.id)

    def test_profile_rejects_invalid_id(self):
        with self.assertRaises(ValidationError):
            CreateUserProfileRequest(
                id="not-a-uuid",
                profile_name="AI Founder",
                niche="AI automation",
                offer="AI workflows",
                target_audience="Founders",
                expertise="ML engineering",
                tone="Practical",
                goal="Generate leads",
            )

    def test_generate_post_rejects_unknown_options(self):
        with self.assertRaises(ValidationError):
            GeneratePostRequest(
                content_idea_id="22222222-2222-2222-2222-222222222444",
                platform="threads",
                post_format="contrarian",
                post_goal="comment",
            )


if __name__ == "__main__":
    unittest.main()