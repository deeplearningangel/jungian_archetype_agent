import google.generativeai as genai
from typing import Dict, List, NamedTuple
import json

# Configure Gemini API
def configure_gemini():
    """Configure Gemini API with your key"""
    api_key = "AIzaSyBH9cy72TNkNJmJunr8gNn6_9BpLqIZ9Kk"  # Your API key
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# Jung's Classical Archetypes (from Collective Unconscious writings)
JUNGIAN_ARCHETYPES = [
    "The Self", "The Shadow", "The Anima", "The Animus", "The Persona",
    "The Great Mother", "The Wise Old Man", "The Trickster", "The Hero",
    "The Child", "The Syzygy", "The Tree of Life"
]

# Comprehensive Jungian Assessment Questions
# Based on Jung's theoretical constructs from his major works
JUNGIAN_QUESTIONS = [
    # === CONSCIOUS VS UNCONSCIOUS DYNAMICS ===
    {"id": "conscious_1", "category": "consciousness", "construct": "ego_consciousness",
     "text": "I am fully aware of why I make the decisions I do"},
    
    {"id": "conscious_2", "category": "consciousness", "construct": "ego_consciousness", 
     "text": "I can easily explain my motivations to others"},
    
    {"id": "unconscious_1", "category": "consciousness", "construct": "personal_unconscious",
     "text": "I often surprise myself with thoughts or reactions that seem to come from nowhere"},
    
    {"id": "unconscious_2", "category": "consciousness", "construct": "personal_unconscious",
     "text": "My dreams reveal things about myself I don't consciously know"},
    
    {"id": "unconscious_3", "category": "consciousness", "construct": "collective_unconscious",
     "text": "I feel connected to universal human experiences beyond my personal life"},
    
    {"id": "unconscious_4", "category": "consciousness", "construct": "collective_unconscious",
     "text": "Certain symbols, myths, or images deeply move me for reasons I can't explain"},
    
    # === SHADOW WORK (Jung's concept of rejected aspects) ===
    {"id": "shadow_1", "category": "shadow", "construct": "shadow_integration",
     "text": "I am aware of qualities in myself that I don't like to acknowledge"},
    
    {"id": "shadow_2", "category": "shadow", "construct": "shadow_projection",
     "text": "I strongly dislike certain traits in other people"},
    
    {"id": "shadow_3", "category": "shadow", "construct": "shadow_integration",
     "text": "I've had to confront parts of myself that contradicted my self-image"},
    
    {"id": "shadow_4", "category": "shadow", "construct": "shadow_recognition",
     "text": "What I criticize most in others might exist within me too"},
    
    {"id": "shadow_5", "category": "shadow", "construct": "shadow_acceptance",
     "text": "I can admit my flaws without being overwhelmed by shame"},
    
    # === ANIMA/ANIMUS (Contrasexual archetype) ===
    {"id": "anima_1", "category": "anima_animus", "construct": "anima_connection",
     "text": "I feel comfortable expressing my emotional, receptive side"},
    
    {"id": "anima_2", "category": "anima_animus", "construct": "anima_integration",
     "text": "I value intuition and feeling as much as logic and action"},
    
    {"id": "animus_1", "category": "anima_animus", "construct": "animus_connection",
     "text": "I can be assertive and goal-directed when needed"},
    
    {"id": "animus_2", "category": "anima_animus", "construct": "animus_integration",
     "text": "I appreciate both rational thinking and creative expression"},
    
    {"id": "contrasexual_1", "category": "anima_animus", "construct": "contrasexual_balance",
     "text": "I embody both traditionally masculine and feminine qualities"},
    
    {"id": "contrasexual_2", "category": "anima_animus", "construct": "contrasexual_projection",
     "text": "I'm attracted to people who embody qualities I lack in myself"},
    
    # === PERSONA (Social mask vs authentic self) ===
    {"id": "persona_1", "category": "persona", "construct": "persona_awareness",
     "text": "I present differently in various social situations"},
    
    {"id": "persona_2", "category": "persona", "construct": "persona_rigidity",
     "text": "I feel pressure to maintain a certain image of myself"},
    
    {"id": "persona_3", "category": "persona", "construct": "persona_authenticity",
     "text": "Sometimes I feel like I'm playing a role rather than being myself"},
    
    {"id": "persona_4", "category": "persona", "construct": "persona_integration",
     "text": "I can drop my social masks and be genuine when appropriate"},
    
    # === INDIVIDUATION PROCESS (Jung's central concept) ===
    {"id": "individuation_1", "category": "individuation", "construct": "self_realization",
     "text": "I feel called to become my truest, most authentic self"},
    
    {"id": "individuation_2", "category": "individuation", "construct": "wholeness_seeking",
     "text": "I'm working to integrate all aspects of my personality, even contradictory ones"},
    
    {"id": "individuation_3", "category": "individuation", "construct": "transcendent_function",
     "text": "I can hold tension between opposing forces within myself"},
    
    {"id": "individuation_4", "category": "individuation", "construct": "self_archetype",
     "text": "I sense a deeper organizing principle or 'Self' beyond my ego"},
    
    # === PSYCHOLOGICAL TYPES (Jung's typology) ===
    {"id": "type_intro_1", "category": "psychological_types", "construct": "introversion",
     "text": "I gain energy from solitude and inner reflection"},
    
    {"id": "type_extra_1", "category": "psychological_types", "construct": "extraversion",
     "text": "I gain energy from social interaction and external activities"},
    
    {"id": "type_thinking_1", "category": "psychological_types", "construct": "thinking_function",
     "text": "I prefer to make decisions based on logical analysis"},
    
    {"id": "type_feeling_1", "category": "psychological_types", "construct": "feeling_function",
     "text": "I prefer to make decisions based on values and impact on people"},
    
    {"id": "type_sensing_1", "category": "psychological_types", "construct": "sensation_function",
     "text": "I trust concrete, practical information over abstract theories"},
    
    {"id": "type_intuitive_1", "category": "psychological_types", "construct": "intuition_function",
     "text": "I'm drawn to possibilities, patterns, and hidden meanings"},
    
    # === COMPLEXES (Jung's theory of autonomous psychological clusters) ===
    {"id": "complex_1", "category": "complexes", "construct": "autonomous_complexes",
     "text": "Sometimes I react in ways that seem beyond my conscious control"},
    
    {"id": "complex_2", "category": "complexes", "construct": "emotional_complexes",
     "text": "Certain topics or situations trigger intense, disproportionate emotions"},
    
    {"id": "complex_3", "category": "complexes", "construct": "complex_integration",
     "text": "I've noticed patterns in my reactions that point to unresolved issues"},
    
    # === ACTIVE IMAGINATION & SYMBOLIC LIFE ===
    {"id": "symbolic_1", "category": "symbolic_life", "construct": "symbolic_thinking",
     "text": "I find deep meaning in symbols, myths, and metaphors"},
    
    {"id": "symbolic_2", "category": "symbolic_life", "construct": "active_imagination",
     "text": "I engage with my imagination as a source of psychological insight"},
    
    {"id": "symbolic_3", "category": "symbolic_life", "construct": "numinous_experience",
     "text": "I've had experiences that felt spiritually or psychologically transformative"},
    
    # === COMPENSATION & BALANCE ===
    {"id": "compensation_1", "category": "compensation", "construct": "psychic_compensation",
     "text": "My unconscious seems to compensate for my conscious attitudes"},
    
    {"id": "compensation_2", "category": "compensation", "construct": "psychological_balance",
     "text": "I notice that overdeveloping one aspect of myself creates problems elsewhere"},
    
    # === COLLECTIVE UNCONSCIOUS MANIFESTATIONS ===
    {"id": "collective_1", "category": "collective_unconscious", "construct": "archetypal_patterns",
     "text": "I recognize universal patterns in human behavior and stories"},
    
    {"id": "collective_2", "category": "collective_unconscious", "construct": "mythic_resonance",
     "text": "Ancient myths and fairy tales feel personally meaningful to me"},
    
    {"id": "collective_3", "category": "collective_unconscious", "construct": "instinctual_wisdom",
     "text": "I trust that there's an innate wisdom in human nature beyond conscious thought"},
    
    # === TELEOLOGICAL PERSPECTIVE (Purpose and meaning) ===
    {"id": "teleological_1", "category": "teleological", "construct": "life_purpose",
     "text": "I believe my psychological development serves a greater purpose"},
    
    {"id": "teleological_2", "category": "teleological", "construct": "meaningful_suffering",
     "text": "Even difficult experiences contribute to my psychological growth"},
    
    {"id": "teleological_3", "category": "teleological", "construct": "future_oriented",
     "text": "I'm more interested in who I'm becoming than who I've been"}
]

class JungianResult(NamedTuple):
    """Results of comprehensive Jungian analysis"""
    consciousness_level: Dict[str, float]
    shadow_integration: float
    anima_animus_balance: float
    persona_authenticity: float
    individuation_stage: str
    psychological_type: Dict[str, float]
    dominant_complexes: List[str]
    archetypal_resonances: Dict[str, float]
    detailed_analysis: Dict[str, any]

def analyze_jungian_profile(responses: Dict[str, int], free_text: str = "") -> JungianResult:
    """
    Comprehensive Jungian analysis based on responses
    """
    
    # Initialize scoring categories
    consciousness_scores = {
        "ego_consciousness": [],
        "personal_unconscious": [],
        "collective_unconscious": []
    }
    
    shadow_scores = []
    anima_animus_scores = []
    persona_scores = []
    individuation_scores = []
    
    type_scores = {
        "introversion": [],
        "extraversion": [],
        "thinking": [],
        "feeling": [],
        "sensation": [],
        "intuition": []
    }
    
    complex_indicators = []
    symbolic_scores = []
    
    # Process responses by category
    for question in JUNGIAN_QUESTIONS:
        qid = question["id"]
        response = responses.get(qid, 4)
        category = question["category"]
        construct = question["construct"]
        
        # Consciousness analysis
        if category == "consciousness":
            if construct in consciousness_scores:
                consciousness_scores[construct].append(response)
        
        # Shadow integration
        elif category == "shadow":
            shadow_scores.append(response)
        
        # Anima/Animus balance
        elif category == "anima_animus":
            anima_animus_scores.append(response)
        
        # Persona authenticity
        elif category == "persona":
            # Reverse score some items (higher authenticity = lower persona identification)
            if construct in ["persona_rigidity", "persona_pressure"]:
                persona_scores.append(8 - response)
            else:
                persona_scores.append(response)
        
        # Individuation process
        elif category == "individuation":
            individuation_scores.append(response)
        
        # Psychological types
        elif category == "psychological_types":
            if construct == "introversion":
                type_scores["introversion"].append(response)
            elif construct == "extraversion":
                type_scores["extraversion"].append(response)
            elif construct == "thinking_function":
                type_scores["thinking"].append(response)
            elif construct == "feeling_function":
                type_scores["feeling"].append(response)
            elif construct == "sensation_function":
                type_scores["sensation"].append(response)
            elif construct == "intuition_function":
                type_scores["intuition"].append(response)
        
        # Complex indicators
        elif category == "complexes":
            complex_indicators.append(response)
        
        # Symbolic life
        elif category in ["symbolic_life", "collective_unconscious", "teleological"]:
            symbolic_scores.append(response)
    
    # Calculate consciousness levels
    consciousness_level = {}
    for construct, scores in consciousness_scores.items():
        if scores:
            consciousness_level[construct] = sum(scores) / len(scores)
        else:
            consciousness_level[construct] = 4.0
    
    # Calculate other dimensions
    shadow_integration = sum(shadow_scores) / len(shadow_scores) if shadow_scores else 4.0
    anima_animus_balance = sum(anima_animus_scores) / len(anima_animus_scores) if anima_animus_scores else 4.0
    persona_authenticity = sum(persona_scores) / len(persona_scores) if persona_scores else 4.0
    
    # Determine individuation stage
    individuation_avg = sum(individuation_scores) / len(individuation_scores) if individuation_scores else 4.0
    if individuation_avg >= 6.0:
        individuation_stage = "Advanced Individuation"
    elif individuation_avg >= 4.5:
        individuation_stage = "Active Individuation"
    else:
        individuation_stage = "Early Individuation"
    
    # Calculate psychological type
    psychological_type = {}
    for type_name, scores in type_scores.items():
        if scores:
            psychological_type[type_name] = sum(scores) / len(scores)
        else:
            psychological_type[type_name] = 4.0
    
    # Identify dominant complexes (placeholder - would need more sophisticated analysis)
    complex_strength = sum(complex_indicators) / len(complex_indicators) if complex_indicators else 4.0
    if complex_strength >= 5.5:
        dominant_complexes = ["Active Complexes Present"]
    elif complex_strength >= 4.0:
        dominant_complexes = ["Moderate Complex Activity"]
    else:
        dominant_complexes = ["Low Complex Activity"]
    
    # Calculate archetypal resonances (simplified)
    symbolic_strength = sum(symbolic_scores) / len(symbolic_scores) if symbolic_scores else 4.0
    archetypal_resonances = {
        "The Self": individuation_avg,
        "The Shadow": shadow_integration,
        "The Anima/Animus": anima_animus_balance,
        "The Persona": persona_authenticity,
        "Collective Archetypal Connection": symbolic_strength
    }
    
    # Detailed analysis
    detailed_analysis = {
        "consciousness_balance": consciousness_level,
        "integration_scores": {
            "shadow": shadow_integration,
            "anima_animus": anima_animus_balance,
            "persona": persona_authenticity
        },
        "type_profile": psychological_type,
        "individuation_level": individuation_avg,
        "complex_activity": complex_strength,
        "symbolic_engagement": symbolic_strength
    }
    
    return JungianResult(
        consciousness_level=consciousness_level,
        shadow_integration=shadow_integration,
        anima_animus_balance=anima_animus_balance,
        persona_authenticity=persona_authenticity,
        individuation_stage=individuation_stage,
        psychological_type=psychological_type,
        dominant_complexes=dominant_complexes,
        archetypal_resonances=archetypal_resonances,
        detailed_analysis=detailed_analysis
    )

def generate_jungian_insight(result: JungianResult, responses: Dict[str, int], free_text: str = "", model=None) -> str:
    """Generate comprehensive Jungian analysis using Gemini AI"""
    if model is None:
        model = configure_gemini()
    
    # Create sophisticated prompt
    prompt = f"""You are Carl Jung himself, providing a comprehensive psychological analysis. A person has completed an in-depth assessment based on your theoretical framework.

**PSYCHOLOGICAL PROFILE:**

**Consciousness Dynamics:**
- Ego Consciousness: {result.consciousness_level.get('ego_consciousness', 0):.1f}/7
- Personal Unconscious Awareness: {result.consciousness_level.get('personal_unconscious', 0):.1f}/7  
- Collective Unconscious Connection: {result.consciousness_level.get('collective_unconscious', 0):.1f}/7

**Integration Levels:**
- Shadow Integration: {result.shadow_integration:.1f}/7
- Anima/Animus Balance: {result.anima_animus_balance:.1f}/7
- Persona Authenticity: {result.persona_authenticity:.1f}/7

**Individuation Stage:** {result.individuation_stage}

**Psychological Type Tendencies:**
- Introversion: {result.psychological_type.get('introversion', 0):.1f}/7
- Extraversion: {result.psychological_type.get('extraversion', 0):.1f}/7
- Thinking: {result.psychological_type.get('thinking', 0):.1f}/7
- Feeling: {result.psychological_type.get('feeling', 0):.1f}/7
- Sensation: {result.psychological_type.get('sensation', 0):.1f}/7
- Intuition: {result.psychological_type.get('intuition', 0):.1f}/7

**Personal Reflection:** "{free_text}"

**PROVIDE JUNGIAN ANALYSIS:**

1. **Current Individuation Assessment**: Where they stand in the process of becoming whole

2. **Shadow Work Needs**: What rejected aspects require integration

3. **Anima/Animus Development**: How to balance masculine/feminine principles  

4. **Persona vs Self**: Relationship between social mask and authentic nature

5. **Psychological Type Implications**: How their dominant functions serve individuation

6. **Unconscious Compensation**: What the unconscious might be trying to tell them

7. **Next Individuation Steps**: Specific inner work for continued development

**TONE**: Write as Jung himself - wise, depth-psychological, using actual Jungian terminology naturally. Reference concepts like transcendent function, enantiodromia, synchronicity when relevant.

**LENGTH**: 5-6 substantial paragraphs."""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.8,
                "max_output_tokens": 1000,
            }
        )
        return response.text if response.text else "Analysis temporarily unavailable."
    
    except Exception as e:
        return f"Jung's analysis unavailable: {str(e)}"

# Backward compatibility functions for existing app
QUESTIONS = JUNGIAN_QUESTIONS  # For compatibility
ARCHETYPES = JUNGIAN_ARCHETYPES

def score_responses(responses: Dict[str, int], free_text: str = ""):
    """Compatibility wrapper for existing app"""
    jungian_result = analyze_jungian_profile(responses, free_text)
    
    # Convert to old format for app compatibility
    class CompatResult:
        def __init__(self, jung_result):
            self.top3 = [
                (f"Individuation Level: {jung_result.individuation_stage}", jung_result.detailed_analysis['individuation_level'] * 14.28),
                (f"Shadow Integration: {jung_result.shadow_integration:.1f}/7", jung_result.shadow_integration * 14.28),
                (f"Anima/Animus Balance: {jung_result.anima_animus_balance:.1f}/7", jung_result.anima_animus_balance * 14.28)
            ]
            
            self.scores = {
                "Shadow Work": jung_result.shadow_integration * 14.28,
                "Anima/Animus": jung_result.anima_animus_balance * 14.28,
                "Persona Authenticity": jung_result.persona_authenticity * 14.28,
                "Consciousness": jung_result.consciousness_level.get('ego_consciousness', 4) * 14.28,
                "Unconscious Connection": jung_result.consciousness_level.get('personal_unconscious', 4) * 14.28,
                "Collective Resonance": jung_result.consciousness_level.get('collective_unconscious', 4) * 14.28,
                "Introversion": jung_result.psychological_type.get('introversion', 4) * 14.28,
                "Extraversion": jung_result.psychological_type.get('extraversion', 4) * 14.28,
                "Thinking": jung_result.psychological_type.get('thinking', 4) * 14.28,
                "Feeling": jung_result.psychological_type.get('feeling', 4) * 14.28,
                "Sensation": jung_result.psychological_type.get('sensation', 4) * 14.28,
                "Intuition": jung_result.psychological_type.get('intuition', 4) * 14.28
            }
            
            self.explanation = f"Comprehensive Jungian analysis based on {len(JUNGIAN_QUESTIONS)} questions covering consciousness, shadow, anima/animus, persona, individuation, psychological types, and archetypal resonances."
            self.jungian_result = jung_result
    
    return CompatResult(jungian_result)

def narrative_for(archetype_or_dimension: str) -> Dict[str, str]:
    """Enhanced narratives based on Jungian theory"""
    narratives = {
        "Shadow Work": {
            "tagline": "Integration of rejected aspects of the personality",
            "gifts": "Self-awareness, psychological wholeness, reduced projection onto others",
            "shadows": "Denial, repression, scapegoating, unconscious destructive behaviors",
            "growth": "Conscious acknowledgment and integration of disowned qualities"
        },
        "Anima/Animus": {
            "tagline": "Balance of inner masculine and feminine principles",
            "gifts": "Psychological completeness, creativity, authentic relationships",
            "shadows": "Gender rigidity, projection in relationships, one-sided development",
            "growth": "Conscious development of contrasexual qualities within oneself"
        },
        "Persona Authenticity": {
            "tagline": "Balance between social adaptation and authentic self-expression",
            "gifts": "Social effectiveness while maintaining personal integrity",
            "shadows": "Over-identification with roles, loss of authentic self, rigid social masks",
            "growth": "Flexible persona use while staying connected to genuine self"
        },
        "Consciousness": {
            "tagline": "Ego awareness and conscious psychological functioning",
            "gifts": "Self-direction, rational decision-making, personal responsibility",
            "shadows": "Ego inflation, disconnection from unconscious wisdom",
            "growth": "Balanced ego development with openness to unconscious guidance"
        },
        "Unconscious Connection": {
            "tagline": "Relationship with personal unconscious contents",
            "gifts": "Access to repressed memories, creative potential, self-understanding",
            "shadows": "Unconscious compulsions, unprocessed trauma, psychological symptoms",
            "growth": "Active engagement with unconscious through dreams, imagination, therapy"
        },
        "Collective Resonance": {
            "tagline": "Connection to universal human patterns and wisdom",
            "gifts": "Archetypal insight, mythic understanding, transpersonal perspective",
            "shadows": "Inflation, loss of individual identity, archetypal possession",
            "growth": "Conscious relationship with archetypal energies while maintaining ego boundaries"
        }
    }
    
    # Add psychological type narratives
    type_narratives = {
        "Introversion": {
            "tagline": "Energy oriented toward inner world of ideas and reflection",
            "gifts": "Depth, reflection, inner wisdom, independent thinking",
            "shadows": "Social withdrawal, overthinking, isolation from external world",
            "growth": "Developing comfort with external engagement while honoring introvert needs"
        },
        "Extraversion": {
            "tagline": "Energy oriented toward outer world of people and activities",
            "gifts": "Social connection, action-orientation, adaptability, enthusiasm",
            "shadows": "Superficiality, external dependence, avoidance of inner work",
            "growth": "Developing inner reflection while maintaining external engagement"
        },
        "Thinking": {
            "tagline": "Decision-making based on logical analysis and objective criteria",
            "gifts": "Rationality, objectivity, analytical problem-solving, fairness",
            "shadows": "Emotional disconnection, over-intellectualization, lack of empathy",
            "growth": "Integrating feeling values with logical analysis"
        },
        "Feeling": {
            "tagline": "Decision-making based on values and impact on people",
            "gifts": "Empathy, values-based action, human understanding, harmony",
            "shadows": "Over-emotionality, subjective bias, conflict avoidance",
            "growth": "Developing objective analysis while honoring human values"
        },
        "Sensation": {
            "tagline": "Focus on concrete, practical, present-moment information",
            "gifts": "Practicality, realism, attention to detail, grounded perspective",
            "shadows": "Resistance to change, narrow focus, missing the big picture",
            "growth": "Opening to possibilities while maintaining practical grounding"
        },
        "Intuition": {
            "tagline": "Focus on possibilities, patterns, and future potential",
            "gifts": "Vision, innovation, pattern recognition, creative insight",
            "shadows": "Impracticality, unrealistic expectations, neglect of details",
            "growth": "Grounding insights in practical reality while maintaining visionary perspective"
        }
    }
    
    narratives.update(type_narratives)
    
    return narratives.get(archetype_or_dimension, {
        "tagline": "Aspect of psychological development",
        "gifts": "To be discovered through deeper exploration",
        "shadows": "To be acknowledged and integrated", 
        "growth": "To be cultivated through conscious inner work"
    })

# Enhanced AI functions that use the comprehensive Jungian framework
def generate_deeper_insight(top_results, free_text: str = "", model=None) -> str:
    """Generate insight using comprehensive Jungian analysis"""
    if model is None:
        model = configure_gemini()
    
    # This is called with the simplified results, but we can make it more Jungian
    prompt = f"""As Carl Jung, provide insight for someone with these psychological characteristics:

**Profile Summary:** {', '.join([f'{name}: {score:.1f}%' for name, score in top_results])}

**Personal Reflection:** "{free_text}"

Provide a depth-psychological analysis focusing on:
1. Their current individuation stage and psychological development
2. Shadow work opportunities for greater wholeness  
3. Integration practices for balanced psychological functioning
4. Connection to archetypal patterns and collective unconscious

Write as Jung himself would - with psychological depth, compassion, and practical wisdom for inner development. 3-4 paragraphs."""

    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.8, "max_output_tokens": 600}
        )
        return response.text if response.text else "Jungian insight temporarily unavailable."
    except Exception as e:
        return f"Jung's wisdom unavailable: {str(e)}"

def generate_daily_reflection(primary_aspect: str, model=None) -> str:
    """Generate daily reflection based on Jungian principles"""
    if model is None:
        model = configure_gemini()
    
    prompt = f"""As Carl Jung, create a daily reflection question for someone working on {primary_aspect}. 

The question should:
- Support psychological development and individuation
- Encourage shadow integration or conscious development
- Be practically applicable to daily life
- Reflect depth-psychological understanding

Provide just the reflective question, written in Jung's thoughtful, psychologically sophisticated style."""

    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.7, "max_output_tokens": 100}
        )
        return response.text.strip() if response.text else f"How can I more consciously engage with {primary_aspect} in my daily life?"
    except Exception as e:
        return f"How can I more consciously develop {primary_aspect} today?"