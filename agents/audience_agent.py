from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

prompt = ChatPromptTemplate.from_template("""
You are a marketing strategist.

Analyze the creator profile and return ONLY valid JSON.

Profile:
- Niche: {niche}
- Offer: {offer}
- Target audience: {target_audience}
- Expertise: {expertise}
- Tone: {tone}
- Goal: {goal}

Return JSON with this exact structure:

{{
  "audience_profile": "...",
  "pains": ["...", "..."],
  "desires": ["...", "..."],
  "objections": ["...", "..."],
  "content_angles": ["...", "..."],
  "tone": "...",
  "positioning": "...",
  "known_for": "..."
}}

Rules:
- No explanations
- No markdown
- Only valid JSON
""")

def run_audience_agent(profile: dict) -> dict:
    chain = prompt | llm
    response = chain.invoke(profile).content

    import json

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("⚠️ JSON parsing failed. Raw output:")
        print(response)
        raise