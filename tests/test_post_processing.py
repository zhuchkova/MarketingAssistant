import unittest

from post_processing import (
    enforce_automation_cta,
    enforce_reel_caption_only,
    extract_reel_caption,
    remove_duplicate_comment_keyword_ctas,
)


class PostProcessingTests(unittest.TestCase):
    def test_removes_duplicate_comment_keyword_sentence_from_body(self):
        body = (
            "Most founders do not need more content ideas. "
            "They need one repeatable system. "
            "Comment GUIDE and I will send you the checklist."
        )

        cleaned = remove_duplicate_comment_keyword_ctas(body, "GUIDE")

        self.assertEqual(
            cleaned,
            "Most founders do not need more content ideas. They need one repeatable system.",
        )

    def test_keeps_non_cta_keyword_mentions(self):
        body = "Use the guide as a weekly planning reference. Save it before Friday."

        cleaned = remove_duplicate_comment_keyword_ctas(body, "GUIDE")

        self.assertEqual(cleaned, body)

    def test_enforce_automation_cta_keeps_keyword_only_in_cta(self):
        post = {
            "hook": "Your content system is too heavy.",
            "body": "Use one simple planning loop.\n\nComment GUIDE and I will send the template.",
            "cta": "Comment GUIDE and I'll send you the content planner.",
            "final_text": "old generated text with duplicate CTA",
        }
        resource = {
            "title": "content planner",
            "suggested_keyword": "GUIDE",
        }

        result = enforce_automation_cta(post, resource)

        self.assertEqual(result["body"], "Use one simple planning loop.")
        self.assertEqual(result["cta"], "Comment GUIDE and I'll send you the content planner.")
        self.assertEqual(result["final_text"], "")

    def test_enforce_automation_cta_adds_missing_keyword_cta(self):
        post = {
            "hook": "A useful hook",
            "body": "A useful body",
            "cta": "Want the checklist?",
            "final_text": "old generated text",
        }
        resource = {
            "title": "the checklist",
            "suggested_keyword": "CHECKLIST",
        }

        result = enforce_automation_cta(post, resource)

        self.assertEqual(result["cta"], "Comment CHECKLIST and I'll send you the checklist.")
        self.assertEqual(result["final_text"], "")

    def test_extract_reel_caption_prefers_labeled_caption_section(self):
        body = """Reel script:
Hook: Stop writing posts from scratch.
Voiceover: Build one repeatable idea loop.
On-screen text: One loop beats ten random posts.

Caption:
Most founders do not need more content ideas.

They need one simple system they can repeat every week."""

        self.assertEqual(
            extract_reel_caption(body),
            (
                "Most founders do not need more content ideas.\n\n"
                "They need one simple system they can repeat every week."
            ),
        )

    def test_enforce_reel_caption_only_updates_body_and_resets_final_text(self):
        post = {
            "hook": "Stop making content harder.",
            "body": "Script: Say this to camera.\n\nCaption: Build one simple content loop.",
            "cta": "Save this for planning day.",
            "final_text": "old full text",
        }

        result = enforce_reel_caption_only(post, "reel")

        self.assertEqual(result["body"], "Build one simple content loop.")
        self.assertEqual(result["final_text"], "")

    def test_enforce_reel_caption_only_ignores_carousel(self):
        post = {
            "hook": "Useful hook",
            "body": "Script: This should stay because it is not a reel.",
            "cta": "Useful CTA",
            "final_text": "Useful final text",
        }

        result = enforce_reel_caption_only(post, "carousel")

        self.assertEqual(result["body"], "Script: This should stay because it is not a reel.")
        self.assertEqual(result["final_text"], "Useful final text")


if __name__ == "__main__":
    unittest.main()
