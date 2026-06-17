from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from rag.idea_retriever import retrieve_idea_knowledge

load_dotenv()


class ContentIdea(BaseModel):
    title: str = Field(description="Short internal title for the content idea")
    hook: str = Field(description="Strong opening line for the post")
    angle: str = Field(description="The framing of the topic, e.g. contrarian, how-to, mistake, story")
    topic: str = Field(description="Main topic of the post")


class ContentIdeasResult(BaseModel):
    ideas: List[ContentIdea] = Field(description="List of generated content ideas")


model = init_chat_model(
    model="openai:gpt-4o-mini",
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
- Content angles: {content_angles}
- Positioning: {positioning}
- Known for: {known_for}

Relevant hook and idea knowledge from RAG:
{idea_knowledge}

Generate {number_of_ideas} content ideas.

Rules:
- Make ideas specific to this audience
- Avoid generic marketing advice
- Each idea needs a strong hook
- Each idea should connect to one clear audience pain, desire, or objection
- Use trigger moments and audience language to make hooks feel timely and specific
- Use the creator's personal touch when it makes the idea more human, but do not force it into every idea
""")


def run_idea_agent(
    profile: dict,
    audience_analysis: dict,
    number_of_ideas: int = 10
) -> list[dict]:
    idea_knowledge = retrieve_idea_knowledge(profile, audience_analysis)

    chain_input = {
        **profile,
        **audience_analysis,
        "idea_knowledge": idea_knowledge,
        "number_of_ideas": number_of_ideas,
    }

    chain = prompt | structured_model
    result = chain.invoke(chain_input)

    return [idea.model_dump() for idea in result.ideas]
