"""
ASCII / Unicode architecture diagram generator.
"""

ASCII_SYSTEM_PROMPT = """You are a software architect creating clean ASCII/Unicode architecture diagrams.
Generate structured, clean box-and-arrow diagrams using Unicode box-drawing characters (┌─┐, │, └─┘, ▲, ▼, ◄, ►).

RULES:
1. Ensure boxes are neatly aligned with even padding and straight lines.
2. Clearly label services, databases, queues, and protocols (e.g. [REST], [gRPC], [SQL]).
3. Use arrows (──►, ◄──►, ▲, ▼) to show direction of communication.
4. Output ONLY the ASCII diagram inside a clean layout. Do NOT include markdown code fences (no ```).
"""

def sanitize_ascii(raw_output: str) -> str:
    """
    Cleans code fences from ASCII diagram output.
    """
    lines = raw_output.strip().splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()
