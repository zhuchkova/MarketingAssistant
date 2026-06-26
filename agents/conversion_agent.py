from typing import List
from pydantic import BaseModel, ConfigDict, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from rag.conversion_retriever import retrieve_conversion_knowledge

load_dotenv()


class ManyChatSetup(BaseModel):
    manual_required: bool = Field(description="Always true until full ManyChat automation setup is supported")
    comment_trigger_mode: str = Field(description="specific_word or any_word")
    public_comment_reply: str = Field(description="Public reply to configure in the Instagram comments automation")
    trigger_keyword: str = Field(description="Keyword users should comment")
    public_comment_reply_options: List[str] = Field(description="Alternative short public replies")
    opening_dm_text: str = Field(description="Opening DM text shown before the user clicks the button")
    second_dm_text: str = Field(description="Second DM text sent after the user clicks the opening button")
    opening_dm_button_label: str = Field(description="Button label in the opening DM, for example Send me the link")
    link_button_label: str = Field(description="Button label for the delivered link, for example Open")
    flow_type: str = Field(description="Type of flow, for example instagram_comment_to_dm")
    lead_magnet_used: bool = Field(description="Whether a saved lead magnet or custom URL was used")
    lead_magnet_url: str = Field(description="Lead magnet or offer URL, or an empty string if none exists")
    setup_steps: List[str] = Field(description="Manual setup steps for ManyChat")
    api_supported_parts: List[str] = Field(description="ManyChat API pieces that may be automated later")

    model_config = ConfigDict(extra="forbid")


class ManyChatFlowResult(BaseModel):
    trigger_keyword: str = Field(description="Short keyword users should comment or DM")
    public_comment_reply_options: List[str] = Field(description="Three short public comment reply options")
    public_comment_reply: str = Field(description="Short public reply to the user's Instagram comment")
    first_message: str = Field(description="First ManyChat DM message")
    second_message: str = Field(description="Second DM message after the user clicks the opening button")
    opening_dm_button_label: str = Field(description="Opening DM button label")
    link_button_label: str = Field(description="Link button label")
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

Create a reusable ManyChat-style Instagram comment-to-DM flow for this lead resource.

The flow may later be attached to many Instagram reels or carousels. If the post fields below are blank, ignore them and base the flow on the creator, audience, and selected lead magnet/resource.

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

Optional generated post context:
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
- Comment trigger mode: {lead_magnet_trigger_type}
- Public comment reply: {lead_magnet_public_comment_reply}
- Delivery message: {lead_magnet_delivery_message}
- Second DM message: {lead_magnet_second_dm_message}
- Opening DM button label: {lead_magnet_opening_dm_button_label}
- Link button label: {lead_magnet_link_button_label}
- Qualification question: {lead_magnet_qualification_question}
- Follow-up CTA: {lead_magnet_follow_up_cta}
- Preferred post goal: {lead_magnet_preferred_post_goal}

Relevant CTA knowledge:
{cta_knowledge}

Relevant ManyChat funnel templates:
{manychat_knowledge}

Rules:
- Use a short uppercase trigger keyword unless the selected trigger mode is any_word
- comment_trigger_mode must be specific_word unless the user explicitly wants any word or reaction
- Public comment reply should be short and acknowledge that the DM/resource is coming
- Return exactly 3 public_comment_reply_options. The selected public_comment_reply must be one of them unless a saved public reply exists.
- If a saved public comment reply exists, use it unless it is clearly unsafe or irrelevant
- first_message is the opening DM before the user clicks the button. It must not include the URL directly and should not say the link is already inside the message.
- Make first_message specific to this lead magnet/resource, creator, and audience. Use the resource title, description, outcome, niche, or local context when available.
- Do not reuse the same generic wording for every resource. Good pattern: “Hey there, I’m so happy you’re here. Thanks for your interest in [resource/outcome]. Click below and I’ll send [specific resource] in just a sec.”
- If a saved first DM/delivery message exists, use it as first_message only if it follows the opening-DM pattern and does not already send the link.
- second_message is sent after the user clicks the opening DM button. It should deliver the promised resource/details and may mention that the link/button is below, but should not be identical to first_message.
- If a saved second DM exists, use it unless it is clearly unsafe or irrelevant.
- If saved button labels exist, use them exactly unless they are too long or unclear
- If a saved qualification question or follow-up exists, use it unless it is clearly unsafe or irrelevant
- If a lead magnet URL exists, the first message must NOT include that URL; the URL belongs in the link step after the user clicks the opening button.
- If no lead magnet URL exists, create a useful goal-based flow: booking details for book_visit, order details for buy_order, or a simple next-step conversation for comment/save/share/follow. Do not pretend a link exists.
- opening_dm_button_label should be direct, for example “Send me the link”, “Show me”, “Start”, “Tell me more”, or “Send details”.
- link_button_label should be short, for example “Open”, “Book”, “View”, “Shop”, or “Read”. If no URL exists, return an empty string for link_button_label.
- Qualification question is optional in real setup, but output one useful easy-to-answer question for users who want it.
- Follow-up is optional in real setup, but output a gentle follow-up that moves the user toward the creator's offer.
- Keep messages short and natural
- manychat_setup must be JSON-serializable and include:
  - manual_required: true
  - comment_trigger_mode
  - public_comment_reply
  - public_comment_reply_options
  - trigger_keyword
  - opening_dm_text
  - second_dm_text
  - opening_dm_button_label
  - link_button_label
  - flow_type
  - lead_magnet_used
  - lead_magnet_url as a URL string or an empty string if no URL exists
  - setup_steps
  - api_supported_parts
- setup_steps must reflect the real choices made for this flow: keyword mode, selected keyword or any-word trigger, public reply, public reply alternatives, opening DM, button label, second DM, link button label only when a URL exists, optional qualification question, optional follow-up, preview, and go live.
- api_supported_parts should say the API can help with account metadata, tags, fields, and sending content/flows once a subscriber/contact exists, but Instagram comment automation setup itself is prepared as manual ManyChat setup notes for now.
- opening_dm_text must exactly match first_message.
- second_dm_text must exactly match second_message.
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
