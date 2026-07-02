import unittest

from pydantic import ValidationError

from schemas.auth import LoginRequest, RegisterRequest
from schemas.content_idea import ContentIdeaRequest, GenerateIdeasRequest
from schemas.automation_resource import AutomationResourceRequest
from schemas.post_generation import GeneratePostRequest, UpdatePostRequest
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

    def test_generate_ideas_normalizes_trend_context(self):
        request = GenerateIdeasRequest(count=10, trend_context=" chocolate week ")

        self.assertEqual(request.trend_context, "Chocolate week")

    def test_generate_post_accepts_share_goal(self):
        request = GeneratePostRequest(
            content_idea_id="22222222-2222-2222-2222-222222222444",
            platform="instagram",
            instagram_content_type="carousel",
            post_goal="share",
            post_length="long",
            automation_resource_id="55555555-5555-5555-5555-555555555555",
        )

        self.assertEqual(request.post_goal, "share")
        self.assertEqual(request.instagram_content_type, "carousel")
        self.assertEqual(request.post_length, "long")
        self.assertEqual(request.automation_resource_id, "55555555-5555-5555-5555-555555555555")

    def test_generate_post_rejects_invalid_automation_resource_id(self):
        with self.assertRaises(ValidationError):
            GeneratePostRequest(
                content_idea_id="22222222-2222-2222-2222-222222222444",
                platform="instagram",
                instagram_content_type="carousel",
                post_goal="comment",
                automation_resource_id="not-a-uuid",
            )

    def test_generate_post_rejects_unknown_instagram_type(self):
        with self.assertRaises(ValidationError):
            GeneratePostRequest(
                content_idea_id="22222222-2222-2222-2222-222222222444",
                platform="instagram",
                instagram_content_type="grid",
                post_goal="share",
            )

    def test_generate_post_rejects_unknown_length(self):
        with self.assertRaises(ValidationError):
            GeneratePostRequest(
                content_idea_id="22222222-2222-2222-2222-222222222444",
                platform="linkedin",
                post_goal="comment",
                post_length="extra_long",
            )

    def test_update_post_trims_text(self):
        request = UpdatePostRequest(
            hook=" Useful hook ",
            body=" Useful body ",
            cta=" Comment YES ",
            final_text=" Useful hook\n\nUseful body\n\nComment YES ",
        )

        self.assertEqual(request.hook, "Useful hook")
        self.assertEqual(request.final_text, "Useful hook\n\nUseful body\n\nComment YES")

    def test_update_post_requires_final_text(self):
        with self.assertRaises(ValidationError):
            UpdatePostRequest(
                hook="Useful hook",
                body="Useful body",
                cta="Comment YES",
                final_text="   ",
            )

    def test_automation_resource_accepts_reusable_flow_fields(self):
        request = AutomationResourceRequest(
            title=" Bouquet Guide ",
            url=" https://example.com/guide ",
            suggested_keyword=" GUIDE ",
            trigger_type=" SPECIFIC_WORD ",
            public_comment_reply=" Sent it to you now. ",
            delivery_message=" Here is the guide. ",
            opening_dm_button_label=" Send me the link ",
            link_button_label=" Open ",
            qualification_question=" What are you trying to solve? ",
            follow_up_cta=" Book a bouquet consult. ",
            preferred_post_goal=" DOWNLOAD ",
        )

        self.assertEqual(request.title, "Bouquet Guide")
        self.assertEqual(request.suggested_keyword, "GUIDE")
        self.assertEqual(request.trigger_type, "specific_word")
        self.assertEqual(request.opening_dm_button_label, "Send me the link")
        self.assertEqual(request.link_button_label, "Open")
        self.assertEqual(request.preferred_post_goal, "download")

    def test_automation_resource_rejects_unknown_trigger_type(self):
        with self.assertRaises(ValidationError):
            AutomationResourceRequest(
                title="Guide",
                trigger_type="everyone",
            )

    def test_automation_resource_rejects_unknown_preferred_goal(self):
        with self.assertRaises(ValidationError):
            AutomationResourceRequest(
                title="Guide",
                preferred_post_goal="subscribe",
            )

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
