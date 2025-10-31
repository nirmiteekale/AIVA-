import os
import json
import time
import uuid
from pathlib import Path
from dotenv import load_dotenv
from export_docx import markdown_to_docx
from notion_integration import send_markdown_as_page
from auth import signup_email_password, signin_email_password

import streamlit as st

# OpenAI SDK (>=1.0)
try:
    from openai import OpenAI
except Exception as e:
    OpenAI = None

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

st.set_page_config(page_title="AIVA — AI PM Assistant", page_icon="🧠", layout="wide")
st.title("AIVA — AI Virtual Product Strategist")


# --- Firebase Optional Save ---
from firebase_config import init_firebase, firebase_enabled, firebase_db
f_ok, _db = init_firebase()
if f_ok:
    st.sidebar.success("Firebase connected")
else:
    st.sidebar.info("Firebase not configured (optional)")

def save_to_cloud(doc_name, markdown):
    if not firebase_enabled or firebase_db is None:
        return False, "Firebase not configured"
    try:
        import datetime
        doc = {
            "name": doc_name,
            "content": markdown,
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "title": title,
            "description": desc,
            "flags": {"prd": want_prd, "kpis": want_kpis, "competitors": want_comp}
        }
        firebase_db.collection("aiva_prds").add(doc)
        return True, "Saved to Firestore"
    except Exception as e:
        return False, str(e)



if not OPENAI_API_KEY:
    st.warning("Add your OpenAI API key in a .env file (OPENAI_API_KEY=...) to generate AI outputs.")
else:
    client = OpenAI(api_key=OPENAI_API_KEY)

# Sidebar
with st.sidebar:
    st.header("Settings")
    model = st.text_input("Model (e.g., gpt-4o-mini, gpt-4.1, etc.)", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    st.caption("Tip: Use a lightweight model for fast drafts.")
    st.markdown("---")
    st.subheader("Export")
    st.caption("DOCX/Notion export available below")
    export_name = st.text_input("Export file name", value="aiva_prd.md")
    save_btn = st.button("💾 Save Current Output")

# Inputs
st.subheader("1) Idea Intake")
title = st.text_input("Idea Title", placeholder="e.g., AIVA — AI assistant that turns ideas into PRDs")
desc = st.text_area("Describe your idea", placeholder="Who is it for? What problem does it solve? When is it used?")

col1, col2, col3 = st.columns(3)
with col1:
    want_prd = st.checkbox("Generate PRD", value=True)
with col2:
    want_kpis = st.checkbox("Suggest KPIs", value=True)
with col3:
    want_comp = st.checkbox("Quick Competitor Scan", value=False)

# Prompts
def load_prompt(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception:
        return ""

system_prompt = Path("../prompts/system_prompt.txt").read_text(encoding="utf-8")
prd_prompt = Path("../prompts/prd_generator_prompt.txt").read_text(encoding="utf-8")

def ask_openai(messages):
    try:
        resp = client.chat.completions.create(model=model, messages=messages, temperature=0.3)
        return resp.choices[0].message.content
    except Exception as e:
        return f"""**AI Error:** {e}

- Check API key / model name
- Try again later
"""

st.subheader("2) Generate")
run = st.button("🚀 Generate Output")

output_sections = []

if run and not title.strip():
    st.error("Please provide an Idea Title to start.")
elif run and OPENAI_API_KEY:
    with st.spinner("Thinking..."):
        base_context = f"Title: {title}\n\nDescription: {desc}\n"
        # PRD
        if want_prd:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prd_prompt + "\n\n" + base_context}
            ]
            prd_md = ask_openai(messages)
            output_sections.append(("PRD", prd_md))

        # KPIs
        if want_kpis:
            messages = [
                {"role": "system", "content": "You are a PM Metrics mentor. Be concrete and concise."},
                {"role": "user", "content": f"Suggest 3-5 measurable KPIs for this product idea.\n\n{base_context}"}
            ]
            kpis_md = ask_openai(messages)
            output_sections.append(("KPIs", kpis_md))

        # Competitors
        if want_comp:
            messages = [
                {"role": "system", "content": "You are a product strategist. Think in SWOT bullets."},
                {"role": "user", "content": f"Give 3 likely competitors or analogous tools for this idea and a brief SWOT bullet for each.\n\n{base_context}"}
            ]
            comp_md = ask_openai(messages)
            output_sections.append(("Competitor Scan", comp_md))

# Render
if output_sections:
    st.subheader("3) Results")
    full_md = []
    for name, md in output_sections:
        st.markdown(f"### {name}")
        st.markdown(md)
        full_md.append(f"# {name}\n\n{md}\n")

    final_markdown = "\n\n---\n\n".join(full_md)


    cloud_col1, cloud_col2 = st.columns(2)
    with cloud_col1:
        if st.button("☁️ Save to Cloud (Firestore)"):
            ok, msg = save_to_cloud(export_name, final_markdown)
            if ok: st.success(msg)
            else: st.warning(msg)
    with cloud_col2:
        st.caption("Cloud save uses optional Firebase config")


    if save_btn or st.button("💾 Save as Markdown Now"):
        Path("./outputs").mkdir(exist_ok=True)
        out_path = Path("./outputs") / export_name
        out_path.write_text(final_markdown, encoding="utf-8")
        st.success(f"Saved to {out_path}")

    # Export to DOCX
    if st.button("📝 Export to DOCX"):
        docx_path = Path("./outputs") / (export_name.replace(".md","") + ".docx")
        markdown_to_docx(final_markdown, str(docx_path))
        st.success(f"Saved DOCX to {docx_path}")

    # Send to Notion
    if st.button("🔗 Send to Notion (optional)"):
        ok, msg = send_markdown_as_page(title or "AIVA PRD", final_markdown)
        if ok:
            st.success(f"Notion page created: {msg}")
        else:
            st.warning(msg)


    with st.expander("Preview Raw Markdown"):
        st.code(final_markdown, language="markdown")

st.markdown("---")
st.caption("AIVA MVP — Streamlit + OpenAI | Save outputs in ./app/outputs")


with st.sidebar:
    st.markdown("## Auth (optional)")
    auth_tab = st.radio("Choose", ["Sign In", "Sign Up"], horizontal=True)
    auth_email = st.text_input("Email", key="auth_email")
    auth_pass = st.text_input("Password", type="password", key="auth_pass")
    if st.button("Submit", key="auth_submit"):
        try:
            if auth_tab == "Sign Up":
                status, data = signup_email_password(auth_email, auth_pass)
            else:
                status, data = signin_email_password(auth_email, auth_pass)
            if 200 <= status < 300:
                st.session_state["idToken"] = data.get("idToken")
                st.session_state["userEmail"] = data.get("email")
                st.success(f"{auth_tab} success as {data.get('email')}")
            else:
                st.warning(f"Auth error: {data}")
        except Exception as e:
            st.info(f"Auth not configured: {e}")
    if st.session_state.get("userEmail"):
        st.caption(f"Logged in as {st.session_state['userEmail']}")

