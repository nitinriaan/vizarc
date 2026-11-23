"""
VizArc Web Playground (Streamlit)
Universal Architecture Compiler: One Model -> All 9 Renderers (HTML, SVG, D2, Mermaid, C4, etc.).
"""

import os
import sys
import json
from pathlib import Path

# Ensure src/ is on sys.path for local execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from vizarc.engine import VizArcEngine
from vizarc.templates import TEMPLATES, get_template
from vizarc.adapters import render_ir, render_all_formats
from vizarc.adapters.svg_adapter import render_svg_diagram

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
    .badge { background-color: #E2E8F0; color: #334155; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; margin-right: 4px; }
    .badge-hl { background-color: #DBEAFE; color: #1D4ED8; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📐 VizArc</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Universal Software Architecture Compiler: One Canonical Model &rarr; '
    '<span class="badge-hl">Interactive HTML</span> <span class="badge-hl">Pure SVG Vector</span> '
    '<span class="badge">D2</span> <span class="badge">Structurizr C4</span> '
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
    st.markdown("### 📐 13 Preset Architectures")
    preset_names = ["Custom Prompt"] + [f"{t['name']} ({t['id']})" for t in TEMPLATES]
    chosen_preset = st.selectbox("Load architecture preset:", preset_names)

    orientation_choice = st.radio(
        "SVG / Diagram Layout:",
        options=["Horizontal (LR)", "Vertical (TB)"],
        index=0,
        horizontal=True
    )
    selected_orient = "horizontal" if "Horizontal" in orientation_choice else "vertical"

    st.markdown("---")
    st.markdown(
        "**Features:**\n"
        "- ☁️ 188+ Cloud Service Icons (AWS, GCP, Azure, K8s)\n"
        "- ⚡ 100% Offline Mode & 13 Presets\n"
        "- 🎨 Path Tracing, Minimap & Keyboard Shortcuts\n"
        "- 🤖 GitHub Actions PR Comment Automation\n\n"
        "[⭐ Star on GitHub](https://github.com/nitinriaan/vizarc)"
    )

# Selected Template check
selected_tpl = None
if chosen_preset != "Custom Prompt":
    tpl_id = chosen_preset.split("(")[-1].replace(")", "").strip()
    selected_tpl = get_template(tpl_id)

col_input, col_output = st.columns([1, 2], gap="medium")

with col_input:
    st.subheader("1. System Specification")

    if selected_tpl:
        default_text = selected_tpl.get("text", "")
        st.caption(f"**Loaded Preset:** {selected_tpl['name']} — {selected_tpl['description']}")
    else:
        default_text = "Microservice architecture with an API Gateway routing to an Auth service and Order service, using PostgreSQL and Redis cache."

    prompt_input = st.text_area(
        "Describe your system or architecture requirements:",
        value=default_text,
        height=200
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        compile_btn = st.button("🚀 Compile to All 9 Formats", type="primary", use_container_width=True)
    with col_btn2:
        use_preset_ir = st.button("⚡ Render Preset IR (Offline)", use_container_width=True, disabled=not selected_tpl)

with col_output:
    st.subheader("2. Multi-Renderer Previews")

    should_run = compile_btn or use_preset_ir
    if should_run:
        with st.spinner("Compiling Canonical Architecture Model into all formats..."):
            if use_preset_ir and selected_tpl:
                ir = selected_tpl["ir"]
                renders = render_all_formats(ir)
                renders["svg"] = render_svg_diagram(ir, orientation=selected_orient)
                renders["ir"] = json.dumps(ir, indent=2)
                st.session_state.all_renders = renders
            else:
                engine = VizArcEngine(api_key=user_api_key or None)
                ir = engine.generate_ir(prompt=prompt_input)
                renders = render_all_formats(ir)
                renders["svg"] = render_svg_diagram(ir, orientation=selected_orient)
                renders["ir"] = json.dumps(ir, indent=2)
                st.session_state.all_renders = renders

    renders = st.session_state.get("all_renders", None)

    if renders:
        # 9 Format Tabs + IR
        (
            tab_html,
            tab_svg,
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
            "🖼️ Pure SVG Vector",
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

        with tab_svg:
            svg_content = renders.get("svg", "")
            st.download_button(
                label="📥 Download Standalone SVG Vector",
                data=svg_content,
                file_name="architecture.svg",
                mime="image/svg+xml"
            )
            st.markdown(f'<div style="background:#0B0F19; border-radius:8px; padding:12px; overflow:auto;">{svg_content}</div>', unsafe_allow_html=True)

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
            st.info("💡 The underlying Canonical Architecture Model (JSON IR) that fuels all 9 renderers.")
            st.code(renders.get("ir", "{}"), language="json")
    else:
        st.info("👈 Enter a system description or select one of the 13 preset templates, then click Compile.")
