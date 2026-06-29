import os


AUDIENCE_AGENT_MODEL = os.getenv("AUDIENCE_AGENT_MODEL", "openai:gpt-4o-mini")
IDEA_AGENT_MODEL = os.getenv("IDEA_AGENT_MODEL", "openai:gpt-4o-mini")
CONTENT_AGENT_MODEL = os.getenv("CONTENT_AGENT_MODEL", "openai:gpt-4o-mini")
AUTOMATION_AGENT_MODEL = os.getenv("AUTOMATION_AGENT_MODEL", "openai:gpt-4o-mini")
