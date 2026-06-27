from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from rag.content_framework_retriever import retrieve_content_frameworks

load_dotenv()

class GeneratedPost(BaseModel):
    hook: str = Field(description="Opening hook")
    body: str = Field(description="Main post body")
    cta: str = Field(description="Call to action")
    final_text: str = Field(description="Full final post text")


model = init_chat_model(
    model="openai:gpt-4o-mini",
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
- Title: {idea_title}
- Hook idea: {idea_hook}
- Post format: {idea_post_format}
- Idea framing: {idea_angle}
- Topic: {idea_topic}

Relevant content frameworks from RAG:
{content_frameworks}

Post requirements:
- Platform: {platform}
- Instagram content type: {instagram_content_type}
- Post format: {post_format}
- Goal / CTA type: {post_goal}
- Length: {post_length}

Selected reusable Instagram DM resource:
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
- Start with a strong hook
- Respect the requested length:
  - short = one compact idea, no extra sections
  - medium = default useful depth, 2-3 main points
  - long = deeper story/proof/teaching with more nuance
- If platform is Instagram, follow the requested content type:
  - carousel = write as slide-by-slide copy
  - story = write as a sequence of story frames
  - reel = write a short spoken/overlay script plus caption CTA
- Connect the post to the audience pain/desire
- Use audience language and proof points to make the post concrete and credible
- Use market context for currency, local examples, nearby alternatives, and whether the CTA should feel local or online
- Weave in the creator's personal touch only when it strengthens trust, relatability, or story
- Follow the selected idea's post format. Do not change a personal story into a list or a mistakes post into a generic how-to.
- End with a CTA matching the post goal
- If platform is Instagram and a DM resource title or trigger keyword exists, the post CTA must clearly use that DM resource.
- If a trigger keyword exists, use it exactly in the CTA, for example: "Comment GUIDE and I'll send you the checklist."
- If a DM resource URL exists, do not put the URL directly in the public post unless the format naturally needs it; tell the reader to comment or DM the keyword so the resource can be sent privately.
- If no DM resource is selected, use a normal CTA matching the post goal and do not pretend that a download or automation exists.
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
        "content_frameworks": frameworks
    }
    chain = prompt | structured_model
    result = chain.invoke(chain_input)
    return result.model_dump()
