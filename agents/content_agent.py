from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from agents.model_config import CONTENT_AGENT_MODEL
from rag.content_framework_retriever import retrieve_content_frameworks

load_dotenv()

class GeneratedPost(BaseModel):
    hook: str = Field(description="Opening hook")
    body: str = Field(description="Main post body")
    cta: str = Field(description="Call to action")
    final_text: str = Field(description="Full final post text")


model = init_chat_model(
    model=CONTENT_AGENT_MODEL,
    temperature=0.8,
)

structured_model = model.with_structured_output(GeneratedPost)

prompt = ChatPromptTemplate.from_template("""
You are a social media content writer.

Create one platform-specific post.

Creator profile:
- Niche: {niche}
- Offer: {offer}
- Target audience: {target_audience}
- Expertise: {expertise}
- Personal touch: {personal_touch}
- Market scope: {market_scope}
- Primary market: {primary_market}
- Currency: {currency}
- Locale notes: {locale_notes}
- Tone: {tone}
- Goal: {goal}

Audience analysis:
- Audience profile: {audience_profile}
- Pains: {pains}
- Desires: {desires}
- Objections: {objections}
- Trigger moments: {trigger_moments}
- Proof points: {proof_points}
- Audience language: {audience_language}
- Market context: {market_context}
- Content angles: {content_angles}
- Positioning: {positioning}
- Known for: {known_for}

Selected content idea:
- Core message: {idea_title}
- Opening line suggestion: {idea_hook}
- Post format: {idea_post_format}
- Idea framing: {idea_angle}
- Topic: {idea_topic}
- Trend context: {idea_trend_context}

Relevant content frameworks from RAG:
{content_frameworks}

Post requirements:
- Platform: {platform}
- Instagram content type: {instagram_content_type}
- Post format: {post_format}
- Goal / CTA type: {post_goal}
- Length: {post_length}
- Extra drafting context: {extra_context}

Selected reusable Instagram DM resource:
- Automation selected: {automation_resource_selected}
- DM resource title: {automation_resource_title}
- DM resource URL: {automation_resource_url}
- DM resource description: {automation_resource_description}
- Trigger keyword: {automation_resource_keyword}
- Public reply: {automation_resource_public_comment_reply}
- First DM / delivery message: {automation_resource_delivery_message}
- Follow-up CTA: {automation_resource_follow_up_cta}
- Preferred post goal: {automation_resource_preferred_post_goal}

Rules:
- Make it specific, not generic
- Use the creator's tone
- Use the core message as the primary creative premise for the post.
- Start with a strong hook that sharpens the core message. You may rewrite the opening line suggestion; do not copy it blindly if the core message is stronger.
- The opening line suggestion is supporting context, not the main instruction.
- Respect the requested length:
  - short = one compact idea, no extra sections
  - medium = default useful depth, 2-3 main points
  - long = deeper story/proof/teaching with more nuance
- If platform is Instagram, follow the requested content type:
  - carousel = write as slide-by-slide copy
  - story = write as a sequence of story frames
  - reel = write only the Instagram Reel caption for the body. Do not include a reel script, voiceover, on-screen text, overlay text, shot list, or scene directions.
- Connect the post to the audience pain/desire
- Use audience language and proof points to make the post concrete and credible
- Use market context for currency, local examples, nearby alternatives, and whether the CTA should feel local or online
- Weave in the creator's personal touch only when it strengthens trust, relatability, or story
- If the selected idea has trend context, TREND MODE is active:
  - Use it as context for the opening tension, timing, example, comparison, audience behavior, or reason to care.
  - Mention the trend explicitly only when it sounds natural.
  - Do not paste the trend phrase mechanically into the hook, body, and CTA.
  - Make the post feel timely without turning it into a generic trend explainer.
- Use the extra drafting context as a specific direction for this draft when it is provided.
- Follow the selected idea's post format. Do not change a personal story into a list or a mistakes post into a generic how-to.
- End with a CTA matching the post goal
- Keep the CTA only in the cta field. Do not repeat "comment [keyword]", "DM [keyword]", or the final action instruction inside the body.
- If Instagram content type is reel, keep the body as caption copy only. Do not add script, voiceover, overlay, shot list, or scene sections.
- If automation selected is true, the post CTA must clearly use that DM resource.
- If automation selected is true and a trigger keyword exists, use it exactly in the CTA, for example: "Comment GUIDE and I'll send you the checklist."
- If automation selected is true and a trigger keyword exists, the CTA is invalid unless it includes that exact keyword.
- If automation selected is true and a DM resource URL exists, do not put the URL directly in the public post unless the format naturally needs it; tell the reader to comment or DM the keyword so the resource can be sent privately.
- If automation selected is false, use a normal CTA matching the post goal and do not pretend that a download, DM automation, keyword, or private resource exists.
- If automation selected is false, never invent an uppercase comment keyword such as GUIDE, LINK, ARTBUDDY, or similar. A comment CTA may ask a natural question, for example: "What would you add?" or "Tell me your favorite gallery ritual."
""")

revision_prompt = ChatPromptTemplate.from_template("""
You are a social media content editor.

Revise the existing post according to the user's instruction.

Creator profile:
- Niche: {niche}
- Offer: {offer}
- Target audience: {target_audience}
- Expertise: {expertise}
- Personal touch: {personal_touch}
- Market scope: {market_scope}
- Primary market: {primary_market}
- Currency: {currency}
- Locale notes: {locale_notes}
- Tone: {tone}
- Goal: {goal}

Audience analysis:
- Audience profile: {audience_profile}
- Pains: {pains}
- Desires: {desires}
- Objections: {objections}
- Trigger moments: {trigger_moments}
- Proof points: {proof_points}
- Audience language: {audience_language}
- Market context: {market_context}
- Positioning: {positioning}
- Known for: {known_for}

Current post:
- Platform: {platform}
- Instagram content type: {instagram_content_type}
- Post goal: {post_goal}
- Hook: {hook}
- Body: {body}
- CTA: {cta}
- Full text: {final_text}

Selected reusable Instagram DM resource:
- Automation selected: {automation_resource_selected}
- DM resource title: {automation_resource_title}
- Trigger keyword: {automation_resource_keyword}
- Public reply: {automation_resource_public_comment_reply}
- First DM / delivery message: {automation_resource_delivery_message}
- Follow-up CTA: {automation_resource_follow_up_cta}

User revision instruction:
{revision_instruction}

Rules:
- Keep the same platform and post goal unless the instruction clearly asks otherwise.
- Preserve the automation keyword and automation CTA if automation is selected.
- Keep the CTA only in the cta field. Do not repeat "comment [keyword]", "DM [keyword]", or the final action instruction inside the body.
- If Instagram content type is reel, keep the body as caption copy only. Remove script, voiceover, overlay, shot list, or scene sections.
- If automation is not selected, do not invent a private resource, download, or uppercase comment keyword.
- Return a complete revised hook, body, CTA, and final_text.
""")


def run_content_agent(data: dict) -> dict:

    frameworks = retrieve_content_frameworks(
        profile=data,
        audience_analysis=data,
        content_idea={
            "topic": data.get("idea_topic"),
            "angle": data.get("idea_angle"),
            "hook": data.get("idea_hook"),
            "post_format": data.get("idea_post_format"),
            "trend_context": data.get("idea_trend_context"),
            "platform": data.get("platform"),
            "instagram_content_type": data.get("instagram_content_type"),
            "post_length": data.get("post_length"),
            "automation_resource_title": data.get("automation_resource_title"),
            "automation_resource_keyword": data.get("automation_resource_keyword"),
            "automation_resource_preferred_post_goal": data.get("automation_resource_preferred_post_goal"),
        }
    )


    chain_input = {
        **data,
        "idea_trend_context": data.get("idea_trend_context") or "",
        "extra_context": data.get("extra_context") or "",
        "automation_resource_selected": bool(data.get("automation_resource_id")),
        "content_frameworks": frameworks
    }
    chain = prompt | structured_model
    result = chain.invoke(chain_input)
    return result.model_dump()


def run_content_revision_agent(data: dict) -> dict:
    chain_input = {
        **data,
        "automation_resource_selected": bool(data.get("automation_resource_id")),
    }
    chain = revision_prompt | structured_model
    result = chain.invoke(chain_input)
    return result.model_dump()
