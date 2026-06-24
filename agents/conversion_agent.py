from typing import List
from pydantic import BaseModel, ConfigDict, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from rag.conversion_retriever import retrieve_conversion_knowledge

load_dotenv()


class ManyChatSetup(BaseModel):
    manual_required: bool = Field(description="Always true until full ManyChat automation setup is supported")
    public_comment_reply: str = Field(description="Public reply to configure in the Instagram comments automation")
    trigger_keyword: str = Field(description="Keyword users should comment")
    flow_type: str = Field(description="Type of flow, for example instagram_comment_to_dm")
    lead_magnet_used: bool = Field(description="Whether a saved lead magnet or custom URL was used")
    lead_magnet_url: str = Field(description="Lead magnet or offer URL, or an empty string if none exists")
    setup_steps: List[str] = Field(description="Manual setup steps for ManyChat")
    api_supported_parts: List[str] = Field(description="ManyChat API pieces that may be automated later")

    model_config = ConfigDict(extra="forbid")


class ManyChatFlowResult(BaseModel):
    trigger_keyword: str = Field(description="Short keyword users should comment or DM")
    public_comment_reply: str = Field(description="Short public reply to the user's Instagram comment")
    first_message: str = Field(description="First ManyChat DM message")
    qualification_question: str = Field(description="One question to qualify the lead")
    follow_up: str = Field(description="Follow-up message after qualification")
    manychat_setup: ManyChatSetup = Field(
        description="ManyChat-ready setup JSON with manual steps and API-supported pieces"
    )

    model_config = ConfigDict(extra="forbid")


model = init_chat_model(
    model="openai:gpt-4o-mini",
    temperature=0.7,
)

structured_model = model.with_structured_output(ManyChatFlowResult)

prompt = ChatPromptTemplate.from_template("""
You are a conversion strategist for Instagram.

Create a simple ManyChat-style conversion flow for this generated Instagram post.

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

Generated post:
- Platform: {platform}
- Post goal: {post_goal}
- Hook: {hook}
- Body: {body}
- CTA: {cta}
- Final text: {final_text}

Selected lead magnet or offer:
- Lead magnet title: {lead_magnet_title}
- Lead magnet URL: {lead_magnet_url}
- Lead magnet description: {lead_magnet_description}
- Suggested keyword: {lead_magnet_keyword}
- Delivery message: {lead_magnet_delivery_message}
- Follow-up CTA: {lead_magnet_follow_up_cta}

Relevant CTA knowledge:
{cta_knowledge}

Relevant ManyChat funnel templates:
{manychat_knowledge}

Rules:
- Use a short uppercase trigger keyword
- Public comment reply should be short and acknowledge that the DM/resource is coming
- If a lead magnet URL exists, the first message must include that URL
- If no lead magnet URL exists, create a useful goal-based flow: booking details for book_visit, order details for buy_order, or a simple next-step conversation for comment/save/share/follow
- Qualification question should be easy to answer
- Follow-up should gently move the user toward the creator's offer
- Keep messages short and natural
- manychat_setup must be JSON-serializable and include:
  - manual_required: true
  - public_comment_reply
  - trigger_keyword
  - flow_type
  - lead_magnet_used
  - lead_magnet_url as a URL string or an empty string if no URL exists
  - setup_steps
  - api_supported_parts
- Do not add extra keys to manychat_setup.
""")


def run_conversion_agent(context: dict) -> dict:
    rag_knowledge = retrieve_conversion_knowledge(context)

    chain_input = {
        **context,
        **rag_knowledge,
    }

    chain = prompt | structured_model
    result = chain.invoke(chain_input)

    return result.model_dump()
