
import streamlit as st
from typing import Dict
import json
import matplotlib.pyplot as plt

from archetypes.engine import QUESTIONS, ARCHETYPES, score_responses, narrative_for

st.set_page_config(page_title="Jungian Archetype Agent", page_icon="🜍", layout="centered")

st.title("🜍 Jungian Archetype Agent")
st.caption("Reflective tool for self-inquiry. Not a clinical assessment.")

with st.expander("What is this?"):
    st.markdown("""
This app offers a **Jungian-archetype inspired** reflection. You’ll answer 24 statements (1–7). 
We compute scores for 12 archetypes and show your top 3 with insights: **gifts**, **shadows**, and **growth** edges.
**Note:** Archetypes are symbolic lenses, not diagnoses.
""")

st.header("1) About you (optional)")
free_text = st.text_area("Describe yourself in a few sentences. What drives you right now?", height=120, placeholder="I care about freedom, beauty, and building something original...")

st.header("2) Statements (1 = Strongly Disagree, 7 = Strongly Agree)")
with st.form("quiz"):
    responses: Dict[str, int] = {}
    for q in QUESTIONS:
        responses[q["id"]] = st.slider(q["text"], 1, 7, 4, key=q["id"])
    submitted = st.form_submit_button("Get my archetypes")

if submitted:
    result = score_responses(responses, free_text)

    st.subheader("Your Top Archetypes")
    for i, (name, score) in enumerate(result.top3, start=1):
        st.markdown(f"**{i}. {name} — {score:.1f}**")
        n = narrative_for(name)
        with st.container(border=True):
            st.markdown(f"_{n.get('tagline','')}_")
            st.markdown(f"**Gifts:** {n.get('gifts','')}")
            st.markdown(f"**Shadows:** {n.get('shadows','')}")
            st.markdown(f"**Growth:** {n.get('growth','')}")

    st.subheader("All Scores")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    xs = list(result.scores.keys())
    ys = [result.scores[k] for k in xs]
    ax.bar(xs, ys)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score (0-100)")
    ax.set_xticklabels(xs, rotation=45, ha="right")
    ax.set_title("Archetype Profile")
    st.pyplot(fig, clear_figure=True)

    with st.expander("How your result is calculated"):
        st.write(result.explanation)
        st.json(result.scores)

    report = {
        "top3": result.top3,
        "scores": result.scores,
        "summary": [
            {
                "archetype": name,
                "tagline": narrative_for(name).get("tagline",""),
                "gifts": narrative_for(name).get("gifts",""),
                "shadows": narrative_for(name).get("shadows",""),
                "growth": narrative_for(name).get("growth",""),
            } for name, _ in result.top3
        ],
        "notes": free_text,
        "disclaimer": "Symbolic, reflective tool. Not a diagnosis or medical advice."
    }
    st.download_button("Download JSON Report", data=json.dumps(report, indent=2), file_name="archetype_report.json", mime="application/json")

st.markdown("---")
st.caption("© Archetype Agent — for reflection & coaching, not therapy. If you're in crisis, seek professional care.")
