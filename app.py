import streamlit as st
from typing import Dict
import json
import matplotlib.pyplot as plt
import seaborn as sns
import time
from datetime import datetime
import pandas as pd

# Import from enhanced Jungian engine
from engine import (
    JUNGIAN_QUESTIONS as QUESTIONS, 
    JUNGIAN_ARCHETYPES as ARCHETYPES, 
    score_responses, 
    narrative_for, 
    configure_gemini, 
    generate_deeper_insight, 
    generate_daily_reflection,
    analyze_jungian_profile,
    generate_jungian_insight
)

def create_jungian_analysis_prompt(jungian_result, responses, free_text=""):
    """Create Jung-focused analysis prompt"""
    
    # Find high and low responses for shadow work
    high_responses = [q for q, score in responses.items() if score >= 6]
    low_responses = [q for q, score in responses.items() if score <= 2]
    
    high_patterns = []
    low_patterns = []
    
    for q in QUESTIONS:
        if q["id"] in high_responses:
            high_patterns.append(f"{q['category']}: {q['text']}")
        if q["id"] in low_responses:
            low_patterns.append(f"{q['category']}: {q['text']}")
    
    prompt = f"""You are Carl Jung providing a comprehensive depth-psychological analysis. This person has completed an assessment based on your theoretical framework.

**JUNGIAN PSYCHOLOGICAL PROFILE:**

**Individuation Stage:** {jungian_result.individuation_stage}

**Core Dimensions:**
- Shadow Integration: {jungian_result.shadow_integration:.1f}/7
- Anima/Animus Balance: {jungian_result.anima_animus_balance:.1f}/7  
- Persona Authenticity: {jungian_result.persona_authenticity:.1f}/7

**Consciousness Dynamics:**
- Ego Consciousness: {jungian_result.consciousness_level.get('ego_consciousness', 4):.1f}/7
- Personal Unconscious: {jungian_result.consciousness_level.get('personal_unconscious', 4):.1f}/7
- Collective Unconscious: {jungian_result.consciousness_level.get('collective_unconscious', 4):.1f}/7

**Psychological Type Profile:**
- Introversion: {jungian_result.psychological_type.get('introversion', 4):.1f}/7
- Extraversion: {jungian_result.psychological_type.get('extraversion', 4):.1f}/7
- Thinking: {jungian_result.psychological_type.get('thinking', 4):.1f}/7
- Feeling: {jungian_result.psychological_type.get('feeling', 4):.1f}/7
- Sensation: {jungian_result.psychological_type.get('sensation', 4):.1f}/7
- Intuition: {jungian_result.psychological_type.get('intuition', 4):.1f}/7

**Strong Resonances (Conscious Identification):**
{chr(10).join(high_patterns[:5]) if high_patterns else "None identified"}

**Weak Resonances (Potential Shadow Material):**
{chr(10).join(low_patterns[:5]) if low_patterns else "None identified"}

**Personal Reflection:** "{free_text}"

**PROVIDE DEPTH-PSYCHOLOGICAL ANALYSIS:**

1. **Individuation Assessment**: Where they are in becoming psychologically whole

2. **Shadow Work**: What rejected aspects need conscious integration

3. **Anima/Animus Development**: How to balance inner masculine/feminine

4. **Transcendent Function**: Bridging conscious-unconscious divide

5. **Compensation Patterns**: What the unconscious is trying to balance

6. **Next Developmental Phase**: Specific inner work for continued individuation

Use authentic Jungian concepts: enantiodromia, projection, complexes, synchronicity, etc. Write with psychological sophistication and compassionate insight.

**Length**: 3 substantial paragraphs."""

    return prompt

st.set_page_config(page_title="Jungian Depth Psychology Assessment", page_icon="🧠", layout="wide")

st.title("🧠 Jungian Depth Psychology Assessment")
st.caption("Comprehensive psychological analysis based on Carl Jung's theoretical framework")

# Initialize Gemini
@st.cache_resource
def init_gemini():
    """Initialize Gemini model with detailed error reporting"""
    try:
        import google.generativeai as genai
        
        api_key = "AIzaSyBH9cy72TNkNJmJunr8gNn6_9BpLqIZ9Kk"
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        test_response = model.generate_content(
            "Hello", 
            generation_config={"max_output_tokens": 5}
        )
        
        if test_response.text:
            return model
        else:
            st.error("Gemini model created but not responding")
            return None
            
    except ImportError:
        st.error("google-generativeai package not installed")
        return None
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {e}")
        return None

gemini_model = init_gemini()

# System status
with st.expander("🔍 System Status"):
    if gemini_model:
        st.success("✅ Jungian AI Analyst: Online")
        try:
            test = gemini_model.generate_content("Jung", generation_config={"max_output_tokens": 5})
            st.info(f"Connection test: {test.text if test.text else 'No response'}")
        except Exception as e:
            st.error(f"❌ Connection test failed: {e}")
    else:
        st.error("❌ Jungian AI Analyst: Offline")

with st.expander("About This Assessment"):
    st.markdown("""
This assessment is based on **Carl Jung's comprehensive depth psychology**, including:

- **Individuation Process** - Journey toward psychological wholeness
- **Shadow Integration** - Working with rejected aspects of personality  
- **Anima/Animus** - Balancing inner masculine/feminine principles
- **Persona vs Self** - Authentic being beyond social masks
- **Psychological Types** - Jung's original typology system
- **Consciousness Levels** - Ego, personal unconscious, collective unconscious
- **Active Imagination** - Engagement with symbolic and unconscious content

This is **not a clinical assessment** but a tool for psychological self-reflection and growth based on Jungian principles.
""")

# Personal reflection
st.header("1) Psychological Self-Reflection")
free_text = st.text_area(
    "Describe your current psychological landscape. What patterns, conflicts, or developments are you noticing in yourself?", 
    height=140, 
    placeholder="I'm experiencing tension between my public persona and private self. Dreams have been vivid lately, showing me aspects of myself I don't usually acknowledge. I feel called toward something deeper but don't know what..."
)

# Enhanced question interface
st.header("2) Jungian Depth Psychology Questions")

with st.form("jungian_assessment"):
    st.write(f"**{len(QUESTIONS)} questions covering Jung's key psychological concepts**")
    st.write("Rate each statement: 1 = Strongly Disagree → 7 = Strongly Agree")
    
    responses: Dict[str, int] = {}
    
    # Group questions by category for better organization
    categories = {}
    for q in QUESTIONS:
        cat = q["category"].replace("_", " ").title()
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(q)
    
    # Display questions by category
    for category_name, questions in categories.items():
        st.subheader(f"📂 {category_name}")
        
        for q in questions:
            responses[q["id"]] = st.slider(
                q["text"], 
                1, 7, 4, 
                key=q["id"],
                help=f"Category: {category_name} | Construct: {q['construct']}"
            )
        
        st.markdown("---")
    
    submitted = st.form_submit_button("🔮 Analyze My Psychological Profile", use_container_width=True)

if submitted:
    # Comprehensive analysis
    with st.spinner("Conducting comprehensive Jungian analysis..."):
        # Get both simple compatibility results and full Jungian analysis
        simple_result = score_responses(responses, free_text)
        jungian_result = analyze_jungian_profile(responses, free_text)
    
    # Create two-column layout for detailed results
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("---")
        st.subheader("🎭 Individuation Profile")
        
        # Key Jungian dimensions
        dimensions = {
            "Shadow Integration": jungian_result.shadow_integration,
            "Anima/Animus Balance": jungian_result.anima_animus_balance,
            "Persona Authenticity": jungian_result.persona_authenticity,
            "Ego Consciousness": jungian_result.consciousness_level.get('ego_consciousness', 4),
            "Unconscious Connection": jungian_result.consciousness_level.get('personal_unconscious', 4),
            "Collective Resonance": jungian_result.consciousness_level.get('collective_unconscious', 4)
        }
        
        for dimension, score in dimensions.items():
            percentage = (score / 7) * 100
            st.metric(
                dimension, 
                f"{score:.1f}/7",
                delta=f"{percentage:.0f}%"
            )
            
            # Show narrative
            narrative = narrative_for(dimension)
            with st.expander(f"About {dimension}"):
                st.markdown(f"*{narrative.get('tagline', '')}*")
                st.markdown(f"**Gifts:** {narrative.get('gifts', '')}")
                st.markdown(f"**Growth:** {narrative.get('growth', '')}")
    
    with col2:
        st.markdown("---")
        st.subheader("🧭 Psychological Type Profile")
        
        # Type analysis
        type_profile = jungian_result.psychological_type
        
        # Attitude (Intro/Extra)
        intro_score = type_profile.get('introversion', 4)
        extra_score = type_profile.get('extraversion', 4)
        
        if intro_score > extra_score:
            dominant_attitude = f"Introversion ({intro_score:.1f}/7)"
        else:
            dominant_attitude = f"Extraversion ({extra_score:.1f}/7)"
        
        st.metric("Dominant Attitude", dominant_attitude)
        
        # Functions
        functions = {
            "Thinking": type_profile.get('thinking', 4),
            "Feeling": type_profile.get('feeling', 4),
            "Sensation": type_profile.get('sensation', 4),
            "Intuition": type_profile.get('intuition', 4)
        }
        
        sorted_functions = sorted(functions.items(), key=lambda x: x[1], reverse=True)
        
        st.write("**Function Hierarchy:**")
        for i, (func, score) in enumerate(sorted_functions, 1):
            st.write(f"{i}. {func}: {score:.1f}/7")
        
        st.info(f"**Individuation Stage:** {jungian_result.individuation_stage}")

    # MANDATORY JUNGIAN AI ANALYSIS
    st.markdown("---")
    st.subheader("🧠 Jung's Depth-Psychological Analysis")
    
    if gemini_model:
        st.info("🕯️ Channeling Jung's analytical wisdom...")
        
        # Create comprehensive prompt
        analysis_prompt = create_jungian_analysis_prompt(jungian_result, responses, free_text)
        
        with st.spinner("Jung is analyzing your psychological profile..."):
            try:
                time.sleep(1)
                
                # Direct API call for Jung's analysis
                jung_response = gemini_model.generate_content(
                    analysis_prompt,
                    generation_config={
                        "temperature": 0.8,
                        "max_output_tokens": 1200,
                    }
                )
                
                if jung_response and jung_response.text:
                    st.success("✅ Jung's Analysis Complete")
                    st.markdown("### 🌟 Carl Jung's Assessment of Your Psyche")
                    st.markdown(jung_response.text)
                    
                    # Generate integration practice
                    st.markdown("---")
                    st.subheader("🎯 Integration Practice")
                    
                    practice_prompt = f"""As Carl Jung, recommend ONE specific active imagination or inner work practice for someone at the "{jungian_result.individuation_stage}" stage with shadow integration level {jungian_result.shadow_integration:.1f}/7. Make it practical for daily psychological development. 2-3 sentences."""
                    
                    with st.spinner("Jung is prescribing your integration practice..."):
                        practice_response = gemini_model.generate_content(
                            practice_prompt,
                            generation_config={
                                "temperature": 0.7,
                                "max_output_tokens": 200,
                            }
                        )
                        
                        if practice_response and practice_response.text:
                            st.info(f"**Jung's Prescription:**\n\n{practice_response.text}")
                
                else:
                    st.error("❌ Jung's analysis unavailable")
                    
            except Exception as e:
                st.error(f"🚨 Jung's Analysis Failed: {str(e)}")
                
                with st.expander("🔍 Debug Information"):
                    st.code(f"""
Error: {type(e).__name__}: {str(e)}
Model Status: {gemini_model is not None}
Prompt Length: {len(analysis_prompt)}
Individuation Stage: {jungian_result.individuation_stage}
Shadow Integration: {jungian_result.shadow_integration}
                    """)
    else:
        st.error("🤖 Jungian Analyst offline")

    # Comprehensive visualization
    st.markdown("---")
    st.subheader("📊 Comprehensive Psychological Profile")
    
    # Create visualization of all dimensions
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Core Jungian Dimensions
    core_dims = {
        "Shadow\nIntegration": jungian_result.shadow_integration,
        "Anima/Animus\nBalance": jungian_result.anima_animus_balance,
        "Persona\nAuthenticity": jungian_result.persona_authenticity,
        "Individuation\nLevel": jungian_result.detailed_analysis['individuation_level']
    }
    
    bars1 = ax1.bar(core_dims.keys(), [v * 14.28 for v in core_dims.values()], 
                   color=['#e74c3c', '#f39c12', '#9b59b6', '#2ecc71'], alpha=0.8)
    ax1.set_title("Core Jungian Dimensions", fontweight='bold', fontsize=14)
    ax1.set_ylabel("Development Level (%)")
    ax1.set_ylim(0, 100)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add values on bars
    for bar, val in zip(bars1, core_dims.values()):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}/7', ha='center', va='bottom', fontweight='bold')
    
    # 2. Consciousness Levels
    consciousness = {
        "Ego\nConsciousness": jungian_result.consciousness_level.get('ego_consciousness', 4),
        "Personal\nUnconscious": jungian_result.consciousness_level.get('personal_unconscious', 4),
        "Collective\nUnconscious": jungian_result.consciousness_level.get('collective_unconscious', 4)
    }
    
    bars2 = ax2.bar(consciousness.keys(), [v * 14.28 for v in consciousness.values()], 
                   color=['#3498db', '#34495e', '#8e44ad'], alpha=0.8)
    ax2.set_title("Consciousness Dynamics", fontweight='bold', fontsize=14)
    ax2.set_ylabel("Connection Level (%)")
    ax2.set_ylim(0, 100)
    ax2.tick_params(axis='x', rotation=45)
    
    for bar, val in zip(bars2, consciousness.values()):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}/7', ha='center', va='bottom', fontweight='bold')
    
    # 3. Psychological Types - Attitudes
    attitudes = {
        "Introversion": jungian_result.psychological_type.get('introversion', 4),
        "Extraversion": jungian_result.psychological_type.get('extraversion', 4)
    }
    
    bars3 = ax3.bar(attitudes.keys(), [v * 14.28 for v in attitudes.values()], 
                   color=['#16a085', '#e67e22'], alpha=0.8)
    ax3.set_title("Psychological Attitudes", fontweight='bold', fontsize=14)
    ax3.set_ylabel("Preference Level (%)")
    ax3.set_ylim(0, 100)
    
    for bar, val in zip(bars3, attitudes.values()):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}/7', ha='center', va='bottom', fontweight='bold')
    
    # 4. Psychological Functions
    functions = {
        "Thinking": jungian_result.psychological_type.get('thinking', 4),
        "Feeling": jungian_result.psychological_type.get('feeling', 4),
        "Sensation": jungian_result.psychological_type.get('sensation', 4),
        "Intuition": jungian_result.psychological_type.get('intuition', 4)
    }
    
    bars4 = ax4.bar(functions.keys(), [v * 14.28 for v in functions.values()], 
                   color=['#c0392b', '#27ae60', '#f39c12', '#9b59b6'], alpha=0.8)
    ax4.set_title("Psychological Functions", fontweight='bold', fontsize=14)
    ax4.set_ylabel("Function Strength (%)")
    ax4.set_ylim(0, 100)
    ax4.tick_params(axis='x', rotation=45)
    
    for bar, val in zip(bars4, functions.values()):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f}/7', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)
    
    # Detailed results
    with st.expander("📋 Complete Jungian Analysis Data"):
        st.write("**Individuation Assessment:**")
        st.json(jungian_result.detailed_analysis)
        
        st.write("**Question Response Pattern:**")
        response_df = pd.DataFrame([
            {"Question": q["text"][:50] + "...", 
             "Category": q["category"], 
             "Response": responses.get(q["id"], 4)}
            for q in QUESTIONS
        ])
        st.dataframe(response_df)
    
    # Enhanced download
    comprehensive_report = {
        "timestamp": datetime.now().isoformat(),
        "individuation_stage": jungian_result.individuation_stage,
        "core_dimensions": {
            "shadow_integration": jungian_result.shadow_integration,
            "anima_animus_balance": jungian_result.anima_animus_balance,
            "persona_authenticity": jungian_result.persona_authenticity
        },
        "consciousness_levels": jungian_result.consciousness_level,
        "psychological_type": jungian_result.psychological_type,
        "archetypal_resonances": jungian_result.archetypal_resonances,
        "detailed_analysis": jungian_result.detailed_analysis,
        "personal_reflection": free_text,
        "responses": responses,
        "disclaimer": "Comprehensive Jungian depth-psychological analysis for personal growth and self-understanding. Not for clinical diagnosis."
    }
    
    st.download_button(
        "📥 Download Complete Jungian Profile",
        data=json.dumps(comprehensive_report, indent=2),
        file_name=f"jungian_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        use_container_width=True
    )

# Enhanced sidebar
with st.sidebar:
    st.header("🧠 Jungian Depth Psychology")
    
    st.markdown("""
    **This assessment explores:**
    
    🌑 **Shadow Integration**  
    Working with rejected aspects
    
    ⚖️ **Anima/Animus**  
    Inner masculine/feminine balance
    
    🎭 **Persona vs Self**  
    Social mask vs authentic being
    
    🧭 **Individuation**  
    Journey toward wholeness
    
    🔍 **Consciousness Levels**  
    Ego, personal & collective unconscious
    
    🎨 **Active Imagination**  
    Symbolic engagement
    
    **Based on Jung's complete works including:**
    - Psychological Types
    - The Red Book  
    - Memories, Dreams, Reflections
    - The Archetypes & Collective Unconscious
    """)
    
    if gemini_model:
        st.success("🧠 Jung's AI: Active")
    else:
        st.error("🧠 Jung's AI: Inactive")
    
    st.markdown("---")
    st.caption("*For psychological exploration, not clinical use*")

st.markdown("---")
st.caption("© Jungian Depth Psychology Assessment — Based on Carl Jung's theoretical framework")
st.caption("🧠 Powered by comprehensive depth psychology • For individuation and self-understanding")