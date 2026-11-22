"""
D2 Lang format handler and sanitizer.
"""

D2_SYSTEM_PROMPT = """You are an expert cloud architect and systems designer.
Generate clean, valid, professional D2 language (https://d2lang.com) diagrams based on the user's specification.

CRITICAL D2 RULES:
1. Define entities and containers cleanly.
   Example:
   client: Web Browser {
     shape: person
   }
   cloud: AWS Cloud {
     api: API Gateway
     db: Aurora PostgreSQL {
       shape: cylinder
     }
     api -> db: Queries
   }
   client -> cloud.api: HTTPS Request
2. Use standard D2 shapes where appropriate: cylinder for databases, queue for message brokers/Kafka, person for users.
3. Group microservices, databases, and third-party APIs into named containers.
4. Output ONLY the raw D2 diagram syntax. Do NOT include markdown code fences (no ```d2). Do not add conversational explanations.
"""

def sanitize_d2(raw_output: str) -> str:
    """
    Cleans and strips code fences from D2 output.
    """
    lines = raw_output.strip().splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()
