from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from agents.model_config import AUDIENCE_AGENT_MODEL
from rag.positioning_retriever import retrieve_positioning_knowledge

load_dotenv()


class AudienceAnalysis(BaseModel):
    audience_profile: str = Field(description="Detailed description of the target audience")
    pains: List[str] = Field(description="Main pains and frustrations of the audience")
    desires: List[str] = Field(description="Main goals and desires of the audience")
    objections: List[str] = Field(description="Reasons why the audience may hesitate to buy or engage")
    trigger_moments: List[str] = Field(description="Situations or moments when the audience starts actively looking for help")
    proof_points: List[str] = Field(description="Types of proof, examples, or evidence that would make the audience trust the creator")
    audience_language: List[str] = Field(description="Plain-language phrases the audience might use to describe their problems or desired outcomes")
    market_context: List[str] = Field(description="Market-specific context such as geography, currency, local alternatives, local buying expectations, and cultural reference notes")
    content_angles: List[str] = Field(description="Strategic content angles for this audience")
    tone: str = Field(description="Recommended tone of voice")
    positioning: str = Field(description="Clear expert positioning statement")
    known_for: str = Field(description="What the creator should become known for")


model = init_chat_model(
    model=AUDIENCE_AGENT_MODEL,
    temperature=0.7,
)

structured_model = model.with_structured_output(AudienceAnalysis)

prompt = ChatPromptTemplate.from_template("""
You are a marketing strategist.

Analyze the creator profile using the relevant positioning knowledge.

Profile:
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

Relevant positioning knowledge from RAG:
{positioning_knowledge}

Return trigger moments, proof points, audience language, and market context as concrete, audience-specific lists.
Use the personal touch as a source of relatability and differentiation when it is relevant.
Use market context to choose relevant currency, local/global references, buying expectations, and nearby alternatives. Keep output language English.
""")


def run_audience_agent(profile: dict) -> dict:
    positioning_knowledge = retrieve_positioning_knowledge(profile)

    chain_input = {
        **profile,
        "positioning_knowledge": positioning_knowledge
    }

    chain = prompt | structured_model
    result = chain.invoke(chain_input)

    return result.model_dump()
