import unittest

from pydantic import ValidationError

from schemas.auth import LoginRequest, RegisterRequest
from schemas.content_idea import ContentIdeaRequest
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

    def test_profile_personal_touch_is_optional(self):
        request = CreateUserProfileRequest(
            profile_name="AI Founder",
            niche="AI automation",
            offer="AI workflows",
            target_audience="Founders",
            expertise="ML engineering",
            personal_touch="   ",
            tone="Practical",
            goal="Generate leads",
        )

        self.assertIsNone(request.personal_touch)

    def test_profile_market_context_is_optional(self):
        request = CreateUserProfileRequest(
            profile_name="Local Cafe",
            niche="specialty coffee",
            offer="coffee and pastries",
            target_audience="Neighborhood regulars",
            expertise="Barista team",
            market_scope=" local ",
            primary_market=" Berlin, Germany ",
            currency=" EUR ",
            locale_notes=" Write in English, but use local European context. ",
            tone="Warm",
            goal="Increase visits",
        )

        self.assertEqual(request.market_scope, "local")
        self.assertEqual(request.primary_market, "Berlin, Germany")
        self.assertEqual(request.currency, "EUR")
        self.assertEqual(request.locale_notes, "Write in English, but use local European context.")

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
                post_goal="comment",
            )

    def test_generate_post_accepts_share_goal(self):
        request = GeneratePostRequest(
            content_idea_id="22222222-2222-2222-2222-222222222444",
            platform="instagram",
            post_goal="share",
        )

        self.assertEqual(request.post_goal, "share")

    def test_custom_idea_rejects_unknown_style(self):
        with self.assertRaises(ValidationError):
            ContentIdeaRequest(
                title="A useful idea",
                hook="A useful hook",
                angle="A useful angle",
                topic="A useful topic",
                post_format="unknown_style",
            )

    def test_custom_idea_rejects_format_as_framing(self):
        with self.assertRaises(ValidationError):
            ContentIdeaRequest(
                title="A useful idea",
                hook="A useful hook",
                angle="Objection Handling",
                topic="A useful topic",
                post_format="objection_handling",
            )


if __name__ == "__main__":
    unittest.main()
