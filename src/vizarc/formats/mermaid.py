"""
Mermaid format handler and self-healing syntax sanitizer.
"""

import re

MERMAID_SYSTEM_PROMPT = """You are an expert software architect and systems engineer.
Generate clean, valid, professional Mermaid.js diagrams based on the user's specification.

CRITICAL SYNTAX RULES:
1. Always start with a valid Mermaid declaration: 'flowchart TD', 'flowchart LR', 'sequenceDiagram', 'erDiagram', or 'stateDiagram-v2'.
2. For flowcharts, ALWAYS quote node labels that contain special characters, spaces, or parentheses:
   Correct: id["Service Name (Port 8080)"]
   Incorrect: id[Service Name (Port 8080)]
3. Use simple alphanumeric IDs for nodes: e.g., web_client, api_gw, auth_svc, db_main.
4. Use subgraphs to group logical components (e.g., 'subgraph Frontend', 'subgraph Backend Services', 'subgraph Data Layer').
5. Output ONLY the raw Mermaid diagram syntax. Do NOT include markdown code fences (no ```mermaid). Do not add explanations.
"""

def sanitize_mermaid(raw_output: str) -> str:
    """
    Cleans and repairs common Mermaid syntax issues produced by LLMs.
    """
    lines = raw_output.strip().splitlines()
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()
        # Remove markdown fences if present
        if stripped.startswith("```"):
            continue
        cleaned_lines.append(line)

    code = "\n".join(cleaned_lines).strip()

    # Ensure code starts with a valid header
    valid_headers = (
        "flowchart", "graph", "sequenceDiagram", "erDiagram", 
        "classDiagram", "stateDiagram", "stateDiagram-v2", 
        "gantt", "pie", "mindmap"
    )
    first_token = code.split()[0] if code.split() else ""
    if not any(code.strip().startswith(h) for h in valid_headers):
        # Default to flowchart TD if header was omitted
        code = f"flowchart TD\n{code}"

    # Self-healing: Quote unquoted node labels with parentheses e.g. node[Label (Info)] -> node["Label (Info)"]
    # Pattern looks for: ID [ content with () but not starting with " ]
    def quote_label(match):
        node_id = match.group(1)
        bracket_type = match.group(2)  # [ or ( or {
        content = match.group(3)
        closing_bracket = "]" if bracket_type == "[" else (")" if bracket_type == "(" else "}")
        
        # If already quoted, leave as is
        if content.startswith('"') and content.endswith('"'):
            return f"{node_id}{bracket_type}{content}{closing_bracket}"
        # Escape any internal double quotes and wrap in quotes
        safe_content = content.replace('"', "'")
        return f'{node_id}{bracket_type}"{safe_content}"{closing_bracket}'

    code = re.sub(r'(\b\w+)(\[|\(|\{)([^"\[\]\(\)\{\}\n]*\([^"\[\]\n]*\)[^"\[\]\n]*)(\]|\)|\})', quote_label, code)

    return code.strip()
