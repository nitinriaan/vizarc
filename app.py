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
    page_title="VizArc - Interactive Architecture Explainer",
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
    '<div class="sub-title">Turn any idea, plan, or codebase into a beautiful <b>interactive architecture explainer</b>. '
    '<span class="badge">Interactive HTML</span> <span class="badge">Link Tracing</span> <span class="badge">Mermaid</span> <span class="badge">D2</span></div>',
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
            "SaaS Billing & Database Schema"
        ]
    )
    st.markdown("---")
    st.markdown(
        "[⭐ Star on GitHub](https://github.com/nitinriaan/vizarc) • [Built with Gemini Flash](https://aistudio.google.com)"
    )

# Sample Presets Map
PRESETS = {
    "E-Commerce Microservices": {
        "text": "Design a scalable e-commerce architecture with a Next.js web client, mobile app, API Gateway, Auth service, Order service with FastAPI, Payment service with Stripe integration, and PostgreSQL databases. Add Kafka for order processing and Redis for session cache.",
        "format": "html",
        "archetype": "architecture"
    },
    "OAuth2 Auth & Token Refresh": {
        "text": "Client login architecture with Auth0/OAuth server, issuing access and refresh tokens, API gateway token validation, and Redis token revocation store.",
        "format": "html",
        "archetype": "architecture"
    },
    "Real-time WebSocket Chat with Redis": {
        "text": "System architecture for real-time multiplayer chat. Multiple Node.js WebSocket gateway servers, connected via Redis Pub/Sub backplane, persisting message history to Cassandra/PostgreSQL.",
        "format": "html",
        "archetype": "architecture"
    },
    "SaaS Billing & Database Schema": {
        "text": "SaaS billing system with Next.js dashboard, Stripe Webhook listener, Billing worker queue, and PostgreSQL database with Organizations, Memberships, and Invoices.",
        "format": "html",
        "archetype": "architecture"
    }
}

# Layout Columns
col_input, col_output = st.columns([1, 2], gap="medium")

with col_input:
    st.subheader("1. System Specification")

    default_text = "Microservice architecture with an API Gateway routing to an Auth service and Order service, using PostgreSQL and Redis cache."
    default_format = "html"
    default_archetype = "architecture"

    if preset in PRESETS:
        default_text = PRESETS[preset]["text"]
        default_format = PRESETS[preset]["format"]
        default_archetype = PRESETS[preset]["archetype"]

    prompt_input = st.text_area(
        "Describe your system, paste code/schema, or enter requirements:",
        value=default_text,
        height=180
    )

    format_options = ["html", "mermaid", "d2", "ascii", "excalidraw"]
    format_idx = format_options.index(default_format) if default_format in format_options else 0
    target_format = st.selectbox(
        "Target Format:",
        format_options,
        index=format_idx,
        format_func=lambda x: {
            "html": "✨ Interactive One-Page Explainer (.html with Link Tracing)",
            "mermaid": "Mermaid.js (GitHub Markdown standard)",
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

    generate_btn = st.button("🚀 Generate Architecture Explainer", type="primary", use_container_width=True)

with col_output:
    st.subheader("2. Interactive Explainer & Output")

    if generate_btn or ("diagram_result" in st.session_state and st.session_state.diagram_result):
        if generate_btn:
            with st.spinner("VizArc compiling interactive architecture explainer..."):
                engine = VizArcEngine(api_key=user_api_key or None)
                st.session_state.diagram_result = engine.generate(
                    prompt=prompt_input,
                    diagram_format=target_format,
                    archetype=target_archetype
                )
                st.session_state.current_format = target_format

        result = st.session_state.get("diagram_result", "")
        current_fmt = st.session_state.get("current_format", target_format)

        if current_fmt == "html":
            st.download_button(
                label="📥 Download Standalone HTML Explainer",
                data=result,
                file_name="architecture_explainer.html",
                mime="text/html"
            )
            # Render interactive canvas inside iframe
            components.html(result, height=580, scrolling=False)
        elif current_fmt in ("mermaid", "excalidraw"):
            tab_preview, tab_code = st.tabs(["👁️ Live Preview", "💻 Raw Code"])
            with tab_preview:
                mermaid_html = f"""
                <div style="display:flex; justify-content:center; padding: 20px; background:#FAFAFA; border-radius:8px;">
                  <pre class="mermaid">{result}</pre>
                </div>
                <script type="module">
                  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                  mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
                </script>
                """
                components.html(mermaid_html, height=450, scrolling=True)
            with tab_code:
                st.code(result, language="mermaid")
        elif current_fmt == "ascii":
            st.code(result, language="text")
        elif current_fmt == "d2":
            st.code(result, language="bash")
