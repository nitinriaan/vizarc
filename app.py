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
from vizarc.logo_data import LOGO_LIGHT_URI, LOGO_DARK_URI

load_dotenv()

icon_path = Path(__file__).resolve().parent / "assets" / "icons" / "vizarc-blue-64.png"

st.set_page_config(
    page_title="VizArc - Architecture Studio",
    page_icon=str(icon_path) if icon_path.exists() else "📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling (Mermaid Live Editor aesthetic)
st.markdown("""
<style>
    /* Ultra-clean container fitting 16:9 screen */
    .block-container {
        padding-top: 0.6rem !important;
        padding-bottom: 0.8rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        max-width: 100% !important;
    }
    header[data-testid="stHeader"] {
        display: none;
    }
    /* Buttons */
    button[kind="primary"] {
        background-color: #2563EB !important;
        border-color: #2563EB !important;
        font-weight: 600 !important;
    }
</style>
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
    st.session_state.orientation = "horizontal"

current_ir = st.session_state.get("current_ir")
selected_orientation = st.session_state.get("orientation", "horizontal")

html_code = compile_to_html(current_ir) if current_ir else ""
svg_code = render_svg_diagram(current_ir, orientation=selected_orientation) if current_ir else ""

# Two-Pane Split Layout (Compact left control pane ~19%, massive right canvas ~81%)
col_editor, col_preview = st.columns([1, 4.2], gap="medium")

# ==========================================
# LEFT SIDE PANE: System Specification, Actions & Downloads
# ==========================================
with col_editor:
    # VizArc Brand Logo (Responsive Light/Dark GitHub-grade SVG/PNG)
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
      <a href="https://github.com/nitinriaan/vizarc" target="_blank" title="VizArc on GitHub" style="text-decoration: none; display: block;">
        <img src="{LOGO_LIGHT_URI}" class="vizarc-ui-logo-light" alt="VizArc Logo" style="width: 100%; max-width: 200px; display: block;" />
        <img src="{LOGO_DARK_URI}" class="vizarc-ui-logo-dark" alt="VizArc Logo" style="width: 100%; max-width: 200px; display: none;" />
      </a>
    </div>
    <style>
      @media (prefers-color-scheme: dark) {{
        .vizarc-ui-logo-light {{ display: none !important; }}
        .vizarc-ui-logo-dark {{ display: block !important; }}
      }}
      .stApp[data-theme="dark"] .vizarc-ui-logo-light,
      [data-testid="stAppViewContainer"].dark .vizarc-ui-logo-light {{
        display: none !important;
      }}
      .stApp[data-theme="dark"] .vizarc-ui-logo-dark,
      [data-testid="stAppViewContainer"].dark .vizarc-ui-logo-dark {{
        display: block !important;
      }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("#### 📝 Specification")

    spec_input = st.text_area(
        label="System Specification",
        value=st.session_state.get("spec_text", ""),
        height=230,
        placeholder="Describe your system architecture, components, and data flow...",
        label_visibility="collapsed"
    )

    col_btn_gen, col_btn_load = st.columns([3, 2], gap="small")
    with col_btn_gen:
        generate_clicked = st.button("🚀 Generate", type="primary", use_container_width=True)
    with col_btn_load:
        load_preset_clicked = st.button("⚡ Load", use_container_width=True)

    # Downloads in Left Pane
    if current_ir:
        st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
        col_dl_svg, col_dl_html = st.columns(2, gap="small")
        with col_dl_svg:
            st.download_button(
                label="📥 SVG",
                data=svg_code,
                file_name=f"{current_ir.get('title', 'architecture').lower().replace(' ', '_')}.svg",
                mime="image/svg+xml",
                use_container_width=True
            )
        with col_dl_html:
            st.download_button(
                label="📥 HTML",
                data=html_code,
                file_name=f"{current_ir.get('title', 'architecture').lower().replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True
            )

    # Settings Expander (Presets & Orientation only, NO API Key in UI)
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    with st.expander("⚙️ Presets & Layout", expanded=False):
        st.markdown("##### 📐 13 Preset Architectures")
        preset_names = [f"{t['name']} ({t['id']})" for t in TEMPLATES]
        
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
        st.markdown("##### Layout Direction:")
        layout_choice = st.radio(
            "Layout Direction:",
            options=["Horizontal (LR)", "Vertical (TB)"],
            index=0 if selected_orientation == "horizontal" else 1,
            label_visibility="collapsed"
        )
        new_orientation = "horizontal" if "Horizontal" in layout_choice else "vertical"
        if new_orientation != selected_orientation:
            st.session_state.orientation = new_orientation
            st.rerun()

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
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            try:
                api_key = st.secrets.get("GEMINI_API_KEY")
            except Exception:
                pass
        engine = VizArcEngine(api_key=api_key)
        ir = engine.generate_ir(prompt=spec_input)
        st.session_state.current_ir = ir
        st.session_state.spec_text = spec_input
        st.rerun()

# ==========================================
# RIGHT SIDE PANE: Pure Full-Bleed Canvas (No Header, Nothing)
# ==========================================
with col_preview:
    if current_ir:
        # Pure Edge-to-Edge Interactive Canvas & Explainer (16:9 Viewport Fit)
        components.html(html_code, height=820, scrolling=False)

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
