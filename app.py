"""
VizArc Web Playground (Streamlit)
Universal Architecture Compiler: One Model -> All 8 Renderers.
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
    page_title="VizArc - Universal Architecture Compiler",
    page_icon="📐",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.02rem; color: #64748B; margin-bottom: 1.5rem; }
    .badge { background-color: #E2E8F0; color: #334155; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📐 VizArc</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Universal Software Architecture Compiler: One Canonical Model &rarr; '
    '<span class="badge">Interactive HTML</span> <span class="badge">D2</span> <span class="badge">Structurizr C4</span> '
    '<span class="badge">Mermaid</span> <span class="badge">PlantUML</span> <span class="badge">Graphviz DOT</span> '
    '<span class="badge">Excalidraw</span> <span class="badge">ASCII</span></div>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    user_api_key = st.text_input(
        "Google Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Get a free key from Google AI Studio (aistudio.google.com). Leave empty to use offline demo mode."
    )
    st.markdown("---")
    st.markdown("### 💡 Preset Architectures")
    preset = st.selectbox(
        "Load example system:",
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
        "[⭐ Star on GitHub](https://github.com/nitinriaan/vizarc) • [Universal Architecture Compiler](https://github.com/nitinriaan/vizarc)"
    )

# Sample Presets Map
PRESETS = {
    "E-Commerce Microservices": "Design a scalable e-commerce platform: Next.js web client, iOS/Android mobile apps, API Gateway (Envoy), Auth service (Go), Order service (FastAPI), Payment service with Stripe, Kafka event broker, Redis session cache, and PostgreSQL database.",
    "OAuth2 Auth & Token Refresh": "Client authentication architecture: Next.js SPA logging in with OAuth2 authorization code flow, API gateway validating JWT tokens, Auth0 identity provider, and Redis token revocation list.",
    "Real-time WebSocket Chat with Redis": "System architecture for real-time chat: Multiple Node.js WebSocket gateway servers, connected via Redis Pub/Sub backplane, persisting messages to Cassandra cluster.",
    "SaaS Billing & Database Schema": "SaaS billing architecture: React admin dashboard, Stripe Webhook worker queue, Stripe API, and PostgreSQL database storing Organizations, Memberships, and Invoices."
}

col_input, col_output = st.columns([1, 2], gap="medium")

with col_input:
    st.subheader("1. System Specification")

    default_text = PRESETS.get(preset, "Microservice architecture with an API Gateway routing to an Auth service and Order service, using PostgreSQL and Redis cache.")

    prompt_input = st.text_area(
        "Describe your system, paste code or database schema:",
        value=default_text,
        height=220
    )

    compile_btn = st.button("🚀 Compile to All 8 Formats", type="primary", use_container_width=True)

with col_output:
    st.subheader("2. Multi-Renderer Previews")

    if compile_btn or ("all_renders" in st.session_state and st.session_state.all_renders):
        if compile_btn:
            with st.spinner("VizArc analyzing architecture and compiling to all 8 formats in one pass..."):
                engine = VizArcEngine(api_key=user_api_key or None)
                st.session_state.all_renders = engine.generate_all(prompt=prompt_input)

        renders = st.session_state.get("all_renders", {})

        # 8 Format Tabs
        (
            tab_html,
            tab_d2,
            tab_c4,
            tab_mermaid,
            tab_plantuml,
            tab_graphviz,
            tab_excalidraw,
            tab_ascii,
            tab_json
        ) = st.tabs([
            "✨ Interactive Canvas",
            "⚡ D2 Lang",
            "🏛️ Structurizr C4",
            "🧜‍♂️ Mermaid.js",
            "📐 PlantUML",
            "🕸️ Graphviz (DOT)",
            "🎨 Excalidraw",
            "📟 ASCII",
            "📦 Canonical IR"
        ])

        with tab_html:
            st.download_button(
                label="📥 Download Standalone HTML Explainer",
                data=renders.get("html", ""),
                file_name="architecture_explainer.html",
                mime="text/html"
            )
            components.html(renders.get("html", ""), height=580, scrolling=False)

        with tab_d2:
            st.info("💡 Declarative D2 syntax. Test online at https://play.d2lang.com")
            st.code(renders.get("d2", ""), language="bash")

        with tab_c4:
            st.info("💡 Industry-standard Structurizr C4 DSL. Render with Structurizr CLI or Lite.")
            st.code(renders.get("structurizr", ""), language="c")

        with tab_mermaid:
            st.info("💡 Standard Mermaid syntax. Ready to copy into GitHub READMEs or Notion.")
            st.code(renders.get("mermaid", ""), language="mermaid")

        with tab_plantuml:
            st.info("💡 PlantUML component diagram. Test at https://www.planttext.com")
            st.code(renders.get("plantuml", ""), language="text")

        with tab_graphviz:
            st.info("💡 Graphviz DOT language. Compile with `dot -Tpng arch.dot -o arch.png`")
            st.code(renders.get("graphviz", ""), language="dot")

        with tab_excalidraw:
            st.info("💡 Paste this into Excalidraw (More Tools > Mermaid to Excalidraw) for an editable hand-drawn canvas.")
            st.code(renders.get("excalidraw", ""), language="text")

        with tab_ascii:
            st.info("💡 Pure Unicode box diagram for terminal outputs and PR descriptions.")
            st.code(renders.get("ascii", ""), language="text")

        with tab_json:
            st.info("💡 The underlying Canonical Architecture Model (JSON IR) that fuels all 8 renderers.")
            st.code(renders.get("ir", "{}"), language="json")
