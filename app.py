"""
VizArc Live Architecture Studio (Streamlit)
Mermaid-style two-pane layout:
- Left pane: System Specification & ⚙️ Settings (API Key, 13 Presets, Layout Orientation)
- Right pane: Interactive Canvas with top-corner SVG download, and on-demand format export.
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
from vizarc.adapters import render_ir
from vizarc.adapters.svg_adapter import render_svg_diagram
from vizarc.compiler import compile_to_html

load_dotenv()

st.set_page_config(
    page_title="VizArc - Architecture Studio",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling (Mermaid Live Editor aesthetic)
st.markdown("""
<style>
    /* Remove unnecessary default Streamlit top margins */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    header[data-testid="stHeader"] {
        display: none;
    }
    .studio-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 12px;
        margin-bottom: 14px;
        border-bottom: 1px solid #E2E8F0;
    }
    .brand-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0F172A;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: -0.02em;
    }
    .badge-pill {
        font-size: 0.72rem;
        font-weight: 700;
        color: #2563EB;
        background: #EFF6FF;
        border: 1px solid #DBEAFE;
        padding: 3px 8px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .sub-brand {
        font-size: 0.85rem;
        color: #64748B;
    }
    /* Buttons */
    button[kind="primary"] {
        background-color: #2563EB !important;
        border-color: #2563EB !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Navbar
st.markdown("""
<div class="studio-header">
  <div class="brand-title">
    <span>📐 VizArc</span>
    <span class="badge-pill">Live Architecture Studio</span>
  </div>
  <div class="sub-brand">
    Interactive Canvas • Structurizr Themes • Standalone SVG Vector
  </div>
</div>
""", unsafe_allow_html=True)

# Find default template (E-Commerce Platform)
default_tpl_idx = 0
for i, t in enumerate(TEMPLATES):
    if t["id"] == "ecommerce-platform":
        default_tpl_idx = i
        break

# Initialize session state with default preset on first load
if "current_ir" not in st.session_state:
    initial_tpl = TEMPLATES[default_tpl_idx]
    st.session_state.current_ir = initial_tpl["ir"]
    st.session_state.spec_text = initial_tpl["text"]
    st.session_state.preset_id = initial_tpl["id"]

# Two-Pane Split Layout (Like Mermaid Live Editor)
col_editor, col_preview = st.columns([1, 2.7], gap="large")

# ==========================================
# LEFT SIDE PANE: System Specification & ⚙️ Settings
# ==========================================
with col_editor:
    st.markdown("#### 📝 System Specification")

    spec_input = st.text_area(
        label="System Specification",
        value=st.session_state.get("spec_text", ""),
        height=240,
        placeholder="Describe your system architecture, components, and data flow...",
        label_visibility="collapsed"
    )

    col_btn_gen, col_btn_load = st.columns([3, 2], gap="small")
    
    with col_btn_gen:
        generate_clicked = st.button("🚀 Generate Canvas", type="primary", use_container_width=True)
    with col_btn_load:
        load_preset_clicked = st.button("⚡ Load Preset", use_container_width=True)

    # Settings Gear Expander (in the same left pane)
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    with st.expander("⚙️ Settings & Configuration", expanded=False):
        st.markdown("##### ⚙️ Configuration")
        user_api_key = st.text_input(
            "Google Gemini API Key",
            value=os.getenv("GEMINI_API_KEY", ""),
            type="password",
            help="Your Gemini API key is loaded automatically from .env or .streamlit/secrets.toml."
        )

        st.markdown("---")
        st.markdown("##### 📐 13 Preset Architectures")
        preset_names = [f"{t['name']} ({t['id']})" for t in TEMPLATES]
        
        # Calculate selected index
        current_id = st.session_state.get("preset_id", "ecommerce-platform")
        cur_idx = 0
        for i, t in enumerate(TEMPLATES):
            if t["id"] == current_id:
                cur_idx = i
                break

        chosen_preset_name = st.selectbox(
            "Load architecture preset:",
            preset_names,
            index=cur_idx
        )
        selected_tpl_id = chosen_preset_name.split("(")[-1].replace(")", "").strip()

        st.markdown("---")
        st.markdown("##### SVG / Diagram Layout:")
        layout_choice = st.radio(
            "SVG / Diagram Layout:",
            options=["Horizontal (LR)", "Vertical (TB)"],
            index=0,
            label_visibility="collapsed"
        )
        selected_orientation = "horizontal" if "Horizontal" in layout_choice else "vertical"

# Action Logic
if load_preset_clicked:
    tpl = get_template(selected_tpl_id)
    if tpl:
        st.session_state.current_ir = tpl["ir"]
        st.session_state.spec_text = tpl["text"]
        st.session_state.preset_id = tpl["id"]
        st.rerun()

if generate_clicked:
    with st.spinner("Analyzing architecture and generating interactive canvas..."):
        engine = VizArcEngine(api_key=user_api_key or None)
        ir = engine.generate_ir(prompt=spec_input)
        st.session_state.current_ir = ir
        st.session_state.spec_text = spec_input

# ==========================================
# RIGHT SIDE PANE: Interactive Canvas (Majority of page)
# ==========================================
with col_preview:
    current_ir = st.session_state.get("current_ir")
    
    if current_ir:
        # Default: compile interactive HTML & SVG only
        html_code = compile_to_html(current_ir)
        svg_code = render_svg_diagram(current_ir, orientation=selected_orientation)

        # Top Bar: Diagram Title on left, Download SVG & HTML in top-right corner
        col_title, col_svg_dl, col_html_dl = st.columns([4, 1.2, 1.2], gap="small")
        
        with col_title:
            st.markdown(
                f"<div style='font-size:1.15rem; font-weight:700; color:#0F172A; padding-top:4px;'>"
                f"{current_ir.get('title', 'Architecture Diagram')} "
                f"<span style='font-size:0.75rem; color:#64748B; font-weight:normal;'>({len(current_ir.get('nodes', []))} nodes, {len(current_ir.get('edges', []))} links)</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        with col_svg_dl:
            st.download_button(
                label="📥 Download SVG",
                data=svg_code,
                file_name=f"{current_ir.get('title', 'architecture').lower().replace(' ', '_')}.svg",
                mime="image/svg+xml",
                use_container_width=True
            )

        with col_html_dl:
            st.download_button(
                label="📥 Download HTML",
                data=html_code,
                file_name=f"{current_ir.get('title', 'architecture').lower().replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True
            )

        # Primary Display: Interactive Canvas & One-Page Explainer (Archify Spec)
        components.html(html_code, height=680, scrolling=False)

        # On-Demand Styles Expander: Only generate other formats when user asks for them!
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        with st.expander("🛠️ Export to Other Formats (D2, Structurizr C4, Mermaid, PlantUML, Graphviz DOT, Excalidraw, ASCII...)", expanded=False):
            st.caption("Deterministic on-demand compilation: VizArc compiles these from the Canonical IR with zero extra LLM calls.")

            target_style = st.selectbox(
                "Select format to compile:",
                [
                    "Choose a format...",
                    "⚡ D2 Lang",
                    "🏛️ Structurizr C4 DSL",
                    "🧜‍♂️ Mermaid.js",
                    "📐 PlantUML Component",
                    "🕸️ Graphviz (DOT)",
                    "🎨 Excalidraw",
                    "📟 ASCII / Unicode Box Art",
                    "📦 Canonical Architecture Model (JSON IR)"
                ]
            )

            if target_style != "Choose a format...":
                style_map = {
                    "⚡ D2 Lang": ("d2", "bash", "https://play.d2lang.com"),
                    "🏛️ Structurizr C4 DSL": ("structurizr", "c", "https://playground.structurizr.com"),
                    "🧜‍♂️ Mermaid.js": ("mermaid", "mermaid", "https://mermaid.live"),
                    "📐 PlantUML Component": ("plantuml", "text", "https://www.planttext.com"),
                    "🕸️ Graphviz (DOT)": ("graphviz", "dot", None),
                    "🎨 Excalidraw": ("excalidraw", "text", "https://excalidraw.com"),
                    "📟 ASCII / Unicode Box Art": ("ascii", "text", None),
                    "📦 Canonical Architecture Model (JSON IR)": ("ir", "json", None)
                }

                fmt_key, lang, playground_url = style_map[target_style]

                if fmt_key == "ir":
                    compiled_output = json.dumps(current_ir, indent=2)
                else:
                    compiled_output = render_ir(current_ir, target_format=fmt_key)

                col_info, col_copy = st.columns([4, 1])
                with col_info:
                    if playground_url:
                        st.markdown(f"💡 **Tip:** Preview online at [{playground_url}]({playground_url})")
                with col_copy:
                    st.download_button(
                        label=f"💾 Save .{fmt_key}",
                        data=compiled_output,
                        file_name=f"architecture.{fmt_key}",
                        mime="text/plain",
                        use_container_width=True
                    )

                st.code(compiled_output, language=lang)
    else:
        st.info("👈 Enter a system description or load a preset, then click 'Generate Canvas'.")
