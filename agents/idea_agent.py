from typing import List, Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from agents.model_config import IDEA_AGENT_MODEL
from rag.idea_retriever import retrieve_idea_knowledge

load_dotenv()


PostFormat = Literal[
    "personal_story",
    "mistakes",
    "day_in_life",
    "contrarian",
    "how_to",
    "checklist",
    "myth_busting",
    "client_example",
    "behind_scenes",
    "objection_handling",
]

FORMAT_LABELS = {
    "personal_story": "personal story",
    "mistakes": "mistakes",
    "day_in_life": "day in life",
    "contrarian": "contrarian",
    "how_to": "how-to",
    "checklist": "checklist",
    "myth_busting": "myth busting",
    "client_example": "client example",
    "behind_scenes": "behind the scenes",
    "objection_handling": "objection handling",
}


class ContentIdea(BaseModel):
    title: str = Field(description="Core message or strongest promise for the content idea")
    hook: str = Field(description="Possible first sentence or opening line for the post")
    post_format: PostFormat = Field(description="One exact post format slug from the allowed list")
    angle: str = Field(description="The strategic point of view or audience-specific framing, not a format label")
    topic: str = Field(description="Main subject of the post")
    trend_context: str = Field(default="", description="Specific trend or timely context used for this idea, or empty string")


class ContentIdeasResult(BaseModel):
    ideas: List[ContentIdea] = Field(description="List of generated content ideas")


model = init_chat_model(
    model=IDEA_AGENT_MODEL,
    temperature=0.8,
)

structured_model = model.with_structured_output(ContentIdeasResult)

prompt = ChatPromptTemplate.from_template("""
You are a social media strategy agent.

Generate specific content ideas for this creator.

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

Relevant hook and idea knowledge from RAG:
{idea_knowledge}

Trend context for new ideas:
{trend_context}

Generate {number_of_ideas} content ideas.

Rules:
- Make ideas specific to this audience
- Avoid generic marketing advice
- Each idea needs a strong core message and a possible opening line
- Prefer psychology hook patterns from RAG when choosing opening lines, especially expectation breaks, real-talk observations, immediate value, myth breaking, pragmatic framing, insider insight, and number-based proof
- Do not reuse the same opening-line structure across the set; psychology patterns should make openings sharper, not repetitive
- Each idea should connect to one clear audience pain, desire, or objection
- Use these fields clearly:
  - title = the core message, strongest promise, or sharpest belief the post should express
  - hook = one possible first sentence that can open the post; keep it usable, but do not make it carry the whole idea
  - post_format = the structure of the post. Use exactly one of: personal_story, mistakes, day_in_life, contrarian, how_to, checklist, myth_busting, client_example, behind_scenes, objection_handling
  - angle = the specific idea framing or point of view, e.g. "why cheap bouquets disappoint," "the hidden cost of skipping prep," "what changed after I learned this myself"
  - topic = the subject, e.g. "wedding flowers," "weekly meal planning," "beginner strength training"
- angle must not repeat the post_format label. For example, if post_format is objection_handling, angle should explain which objection and why, not say "objection handling"
- Do not invent post_format labels such as artisanal focus, community engagement, audience interaction, educational, or storytime
- Smartly mix post formats so the set includes personal, practical, trust-building, and objection-handling ideas
- Use trigger moments and audience language to make hooks feel timely and specific
- Use market context for relevant local/global references, price/currency examples, and nearby alternatives
- Use the creator's personal touch when it makes the idea more human, but do not force it into every idea
- If trend context is provided, TREND MODE is active:
  - Use the trend as context for timing, audience behavior, objections, desires, examples, or urgency.
  - Do not paste the trend phrase into every title, hook, angle, and topic.
  - Mention the trend explicitly only where it sounds natural; otherwise let it shape the premise.
  - Make the ideas varied. Hooks must not all start with the same phrase or structure.
  - Mix opening-line patterns: question, observation, contrast, story setup, myth, practical problem, or surprising detail.
  - Keep the idea useful even after the trend moment; avoid shallow "this trend is trending" framing.
  - Set trend_context to the exact relevant trend text used by the idea.
- If trend context is empty, keep trend_context empty and generate evergreen ideas.
""")


def run_idea_agent(
    profile: dict,
    audience_analysis: dict,
    number_of_ideas: int = 20,
    trend_context: str = ""
) -> list:
    idea_knowledge = retrieve_idea_knowledge(
        profile,
        audience_analysis,
        trend_context=trend_context or "",
    )

    chain_input = {
        **profile,
        **audience_analysis,
        "idea_knowledge": idea_knowledge,
        "number_of_ideas": number_of_ideas,
        "trend_context": trend_context or "",
    }

    chain = prompt | structured_model
    result = chain.invoke(chain_input)

    return [
        normalize_idea(idea.model_dump(), trend_context=trend_context or "")
        for idea in result.ideas
    ]


def normalize_idea(idea: dict, trend_context: str = "") -> dict:
    post_format = idea.get("post_format") or "how_to"
    angle = (idea.get("angle") or "").strip()
    format_label = FORMAT_LABELS.get(post_format, post_format).lower()
    compact_angle = angle.lower().replace("_", " ").replace("-", " ")

    if compact_angle == format_label or compact_angle == post_format.replace("_", " "):
        topic = (idea.get("topic") or "this topic").strip()
        title = (idea.get("title") or topic).strip()
        idea["angle"] = f"Why {topic} matters: {title}"
    else:
        idea["angle"] = angle

    for field in ("title", "hook", "angle", "topic"):
        idea[field] = capitalize_first(idea.get(field) or "")
    idea["trend_context"] = capitalize_first(trend_context or idea.get("trend_context") or "")

    return idea


def capitalize_first(value: str) -> str:
    value = value.strip()
    return value[:1].upper() + value[1:] if value else value
