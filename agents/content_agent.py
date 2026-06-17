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
- Post format: {post_format}
- Goal / CTA type: {post_goal}

Rules:
- Make it specific, not generic
- Use the creator's tone
- Start with a strong hook
- Connect the post to the audience pain/desire
- Use audience language and proof points to make the post concrete and credible
- Use market context for currency, local examples, nearby alternatives, and whether the CTA should feel local or online
- Weave in the creator's personal touch only when it strengthens trust, relatability, or story
- Follow the selected idea's post format. Do not change a personal story into a list or a mistakes post into a generic how-to.
- End with a CTA matching the post goal
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
        }
    )


    chain_input = {
        **data,
        "content_frameworks": frameworks
    }
    chain = prompt | structured_model
    result = chain.invoke(chain_input)
    return result.model_dump()
