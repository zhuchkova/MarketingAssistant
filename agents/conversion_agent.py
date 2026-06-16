from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from rag.conversion_retriever import retrieve_conversion_knowledge

load_dotenv()


class ManyChatFlowResult(BaseModel):
    trigger_keyword: str = Field(description="Short keyword users should comment or DM")
    first_message: str = Field(description="First ManyChat DM message")
    qualification_question: str = Field(description="One question to qualify the lead")
    follow_up: str = Field(description="Follow-up message after qualification")


model = init_chat_model(
    model="openai:gpt-4o-mini",
    temperature=0.7,
)

structured_model = model.with_structured_output(ManyChatFlowResult)

prompt = ChatPromptTemplate.from_template("""
You are a conversion strategist for Instagram and LinkedIn.

Create a simple ManyChat-style conversion flow for this generated post.

Creator profile:
- Niche: {niche}
- Offer: {offer}
- Target audience: {target_audience}
- Expertise: {expertise}
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
- Positioning: {positioning}
- Known for: {known_for}

Generated post:
- Platform: {platform}
- Post goal: {post_goal}
- Hook: {hook}
- Body: {body}
- CTA: {cta}
- Final text: {final_text}

Relevant CTA knowledge:
{cta_knowledge}

Relevant ManyChat funnel templates:
{manychat_knowledge}

Rules:
- Use a short trigger keyword
- First message should deliver or promise the resource immediately
- Qualification question should be easy to answer
- Follow-up should gently move the user toward the creator's offer
- Keep messages short and natural
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
