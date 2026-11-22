"""
VizArc Web Playground (Streamlit)
Deployable for $0 on Hugging Face Spaces or Streamlit Community Cloud.
"""

import os
import sys
from pathlib import Path

# Ensure src/ is on sys.path for local execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from vizarc.engine import VizArcEngine

load_dotenv()

st.set_page_config(
    page_title="VizArc - AI Architecture & Diagram Engine",
    page_icon="📐",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.05rem; color: #64748B; margin-bottom: 1.5rem; }
    .badge { background-color: #E2E8F0; color: #334155; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📐 VizArc</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">AI-Powered Software Architecture & Diagram Engine for Developers & AI Agents '
    '<span class="badge">Mermaid</span> <span class="badge">D2</span> <span class="badge">ASCII</span> <span class="badge">Excalidraw</span></div>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    user_api_key = st.text_input(
        "Google Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Get a free key from Google AI Studio (aistudio.google.com). Leave empty to use fallback demo mode."
    )
    st.markdown("---")
    st.markdown("### 💡 Preset Templates")
    preset = st.selectbox(
        "Choose an example to load:",
        [
            "Custom",
            "E-Commerce Microservices",
            "OAuth2 Auth & Token Refresh",
            "Real-time WebSocket Chat with Redis",
            "SaaS Database Schema (ERD)"
        ]
    )
    st.markdown("---")
    st.markdown(
        "[⭐ Star on GitHub](https://github.com) • [Built with Gemini Flash](https://aistudio.google.com)"
    )

# Sample Presets Map
PRESETS = {
    "E-Commerce Microservices": {
        "text": "Design a scalable e-commerce architecture with a Next.js web client, API Gateway, Auth service, Product Catalog with Elasticsearch, Payment service with Stripe integration, and PostgreSQL databases. Add Kafka for order processing.",
        "format": "mermaid",
        "archetype": "architecture"
    },
    "OAuth2 Auth & Token Refresh": {
        "text": "Create a detailed sequence diagram showing a client logging in with username and password, receiving access and refresh tokens from Auth0/OAuth server, and handling a 401 Unauthorized token refresh sequence.",
        "format": "mermaid",
        "archetype": "sequence"
    },
    "Real-time WebSocket Chat with Redis": {
        "text": "System architecture for real-time multiplayer chat. Multiple Node.js WebSocket gateway servers, connected via Redis Pub/Sub backplane, persisting message history to Cassandra/PostgreSQL.",
        "format": "d2",
        "archetype": "architecture"
    },
    "SaaS Database Schema (ERD)": {
        "text": "ERD database schema for a SaaS billing platform: Users (id, email, password_hash), Organizations (id, name, plan), Memberships (user_id, org_id, role), Invoices (id, org_id, amount_cents, status).",
        "format": "mermaid",
        "archetype": "erd"
    }
}

# Layout Columns
col_input, col_output = st.columns([1, 1], gap="medium")

with col_input:
    st.subheader("1. System Specification")

    default_text = "Microservice architecture with an API Gateway routing to an Auth service and Order service, using PostgreSQL and Redis cache."
    default_format = "mermaid"
    default_archetype = "architecture"

    if preset in PRESETS:
        default_text = PRESETS[preset]["text"]
        default_format = PRESETS[preset]["format"]
        default_archetype = PRESETS[preset]["archetype"]

    prompt_input = st.text_area(
        "Describe your system, paste SQL schema, or enter requirements:",
        value=default_text,
        height=180
    )

    format_options = ["mermaid", "d2", "ascii", "excalidraw"]
    format_idx = format_options.index(default_format) if default_format in format_options else 0
    target_format = st.selectbox(
        "Target Diagram Format:",
        format_options,
        index=format_idx,
        format_func=lambda x: {
            "mermaid": "Mermaid.js (GitHub & Docs standard)",
            "d2": "D2 Lang (Modern declarative architecture)",
            "ascii": "ASCII / Unicode (Terminal & PR descriptions)",
            "excalidraw": "Excalidraw (Whiteboard importable)"
        }[x]
    )

    archetype_options = ["architecture", "sequence", "flowchart", "erd"]
    archetype_idx = archetype_options.index(default_archetype) if default_archetype in archetype_options else 0
    target_archetype = st.selectbox(
        "Diagram Archetype:",
        archetype_options,
        index=archetype_idx,
        format_func=lambda x: x.capitalize()
    )

    generate_btn = st.button("🚀 Generate Architecture Diagram", type="primary", use_container_width=True)

with col_output:
    st.subheader("2. Generated Diagram & Code")

    if generate_btn or ("diagram_result" in st.session_state and st.session_state.diagram_result):
        if generate_btn:
            with st.spinner("VizArc analyzing and designing system architecture..."):
                engine = VizArcEngine(api_key=user_api_key or None)
                st.session_state.diagram_result = engine.generate(
                    prompt=prompt_input,
                    diagram_format=target_format,
                    archetype=target_archetype
                )
                st.session_state.current_format = target_format

        result = st.session_state.get("diagram_result", "")
        current_fmt = st.session_state.get("current_format", target_format)

        # Tabbed Output: Live Preview vs Raw Code
        tab_preview, tab_code = st.tabs(["👁️ Live Visual Preview", "💻 Raw Code & Markdown"])

        with tab_preview:
            if current_fmt in ("mermaid", "excalidraw"):
                # Render via Mermaid CDN inside HTML component
                mermaid_html = f"""
                <div id="diagram-container" style="display:flex; justify-content:center; padding: 20px; background:#FAFAFA; border-radius:8px; border:1px solid #E2E8F0;">
                  <pre class="mermaid" style="font-family:inherit;">
{result}
                  </pre>
                </div>
                <script type="module">
                  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                  mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
                </script>
                """
                components.html(mermaid_html, height=450, scrolling=True)
            elif current_fmt == "ascii":
                st.code(result, language="text")
            elif current_fmt == "d2":
                st.info("💡 D2 diagrams can be compiled with `d2 file.d2` or pasted into https://play.d2lang.com")
                st.code(result, language="bash")

        with tab_code:
            st.code(result, language="mermaid" if current_fmt == "mermaid" else "text")
            
            # Helper for GitHub README markdown copy
            st.markdown("##### GitHub README Snippet")
            gh_snippet = f"```{current_fmt}\n{result}\n```"
            st.code(gh_snippet, language="markdown")
