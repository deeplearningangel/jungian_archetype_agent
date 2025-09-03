import google.generativeai as genai
from typing import Dict, List, NamedTuple
import json

# Configure Gemini API
def configure_gemini():
    """Configure Gemini API with your key"""
    api_key = "AIzaSyBH9cy72TNkNJmJunr8gNn6_9BpLqIZ9Kk"  # Your API key
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# Archetype definitions
ARCHETYPES = [
    "The Innocent", "The Explorer", "The Sage", "The Hero", 
    "The Outlaw", "The Magician", "The Regular Guy", "The Lover",
    "The Jester", "The Caregiver", "The Creator", "The Ruler"
]

# Questions for archetype assessment
QUESTIONS = [
    {"id": "q1", "text": "I prefer simple, honest solutions over complex strategies"},
    {"id": "q2", "text": "I'm driven to explore new places, ideas, and experiences"},
    {"id": "q3", "text": "I value knowledge, wisdom, and understanding above all"},
    {"id": "q4", "text": "I feel called to overcome challenges and prove my worth"},
    {"id": "q5", "text": "I question authority and challenge the status quo"},
    {"id": "q6", "text": "I believe in transformation and making the impossible possible"},
    {"id": "q7", "text": "I just want to fit in and belong with others"},
    {"id": "q8", "text": "I'm passionate about love, beauty, and intimate connections"},
    {"id": "q9", "text": "I use humor and playfulness to navigate life"},
    {"id": "q10", "text": "I feel responsible for taking care of others"},
    {"id": "q11", "text": "I'm driven to create something new and original"},
    {"id": "q12", "text": "I naturally take charge and lead others"},
    {"id": "q13", "text": "I trust that things will work out for the best"},
    {"id": "q14", "text": "I need freedom and independence above security"},
    {"id": "q15", "text": "I enjoy learning and sharing knowledge with others"},
    {"id": "q16", "text": "I push myself to be stronger and more capable"},
    {"id": "q17", "text": "I'm willing to break rules if they're unjust"},
    {"id": "q18", "text": "I see potential and possibilities others might miss"},
    {"id": "q19", "text": "I value community and shared experiences"},
    {"id": "q20", "text": "I seek deep, meaningful relationships"},
    {"id": "q21", "text": "I find joy in making others laugh and feel good"},
    {"id": "q22", "text": "I prioritize others' needs over my own"},
    {"id": "q23", "text": "I have a vision and work to make it real"},
    {"id": "q24", "text": "I take responsibility for outcomes and results"}
]

class ArchetypeResult(NamedTuple):
    top3: List[tuple]
    scores: Dict[str, float]
    explanation: str

def score_responses(responses: Dict[str, int], free_text: str = "") -> ArchetypeResult:
    """Score responses and determine top archetypes"""
    # Simple scoring algorithm - maps questions to archetypes
    archetype_mapping = {
        "The Innocent": ["q1", "q13"],
        "The Explorer": ["q2", "q14"], 
        "The Sage": ["q3", "q15"],
        "The Hero": ["q4", "q16"],
        "The Outlaw": ["q5", "q17"],
        "The Magician": ["q6", "q18"],
        "The Regular Guy": ["q7", "q19"],
        "The Lover": ["q8", "q20"],
        "The Jester": ["q9", "q21"],
        "The Caregiver": ["q10", "q22"],
        "The Creator": ["q11", "q23"],
        "The Ruler": ["q12", "q24"]
    }
    
    scores = {}
    for archetype, question_ids in archetype_mapping.items():
        # Calculate average score for this archetype's questions
        archetype_scores = [responses.get(qid, 4) for qid in question_ids]
        avg_score = sum(archetype_scores) / len(archetype_scores)
        # Convert to 0-100 scale
        scores[archetype] = ((avg_score - 1) / 6) * 100
    
    # Get top 3
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top3 = sorted_scores[:3]
    
    explanation = f"Scores calculated by averaging responses to 2 questions per archetype, converted to 0-100 scale."
    
    return ArchetypeResult(top3=top3, scores=scores, explanation=explanation)

def narrative_for(archetype: str) -> Dict[str, str]:
    """Return narrative elements for each archetype"""
    narratives = {
        "The Innocent": {
            "tagline": "The optimistic believer in goodness",
            "gifts": "Trust, faith, optimism, and ability to see the good in everything",
            "shadows": "Naivety, denial, and avoiding difficult truths",
            "growth": "Learning to balance optimism with wisdom and discernment"
        },
        "The Explorer": {
            "tagline": "The adventurous seeker of new horizons",
            "gifts": "Independence, curiosity, and pioneering spirit",
            "shadows": "Restlessness, inability to commit, and fear of being trapped",
            "growth": "Finding adventure while building meaningful connections"
        },
        "The Sage": {
            "tagline": "The wise seeker of truth and understanding",
            "gifts": "Wisdom, intelligence, and deep understanding",
            "shadows": "Overthinking, isolation, and ivory tower syndrome",
            "growth": "Applying wisdom practically and connecting with others"
        },
        "The Hero": {
            "tagline": "The courageous warrior for what's right",
            "gifts": "Courage, determination, and willingness to fight for causes",
            "shadows": "Ego, need for recognition, and burnout from constant battles",
            "growth": "Learning when to fight and when to rest, developing humility"
        },
        "The Outlaw": {
            "tagline": "The revolutionary challenger of the status quo",
            "gifts": "Independent thinking, courage to challenge systems, authenticity",
            "shadows": "Destructive rebellion, cynicism, and pushing people away",
            "growth": "Channeling rebellion constructively and building alliances"
        },
        "The Magician": {
            "tagline": "The visionary transformer of reality",
            "gifts": "Vision, creativity, and ability to manifest dreams",
            "shadows": "Manipulation, disconnection from reality, and power abuse",
            "growth": "Using power ethically and staying grounded in reality"
        },
        "The Regular Guy": {
            "tagline": "The down-to-earth connector",
            "gifts": "Empathy, common sense, and ability to relate to everyone",
            "shadows": "Fear of standing out, cynicism, and victim mentality",
            "growth": "Developing confidence while maintaining authenticity"
        },
        "The Lover": {
            "tagline": "The passionate seeker of connection and beauty",
            "gifts": "Passion, commitment, and appreciation of beauty",
            "shadows": "Jealousy, obsession, and losing identity in relationships",
            "growth": "Learning to love self while maintaining healthy boundaries"
        },
        "The Jester": {
            "tagline": "The playful bringer of joy and wisdom",
            "gifts": "Humor, playfulness, and ability to lighten any situation",
            "shadows": "Avoiding serious issues, being inappropriate, and hiding pain",
            "growth": "Balancing humor with depth and addressing underlying issues"
        },
        "The Caregiver": {
            "tagline": "The nurturing protector of others",
            "gifts": "Compassion, generosity, and natural nurturing abilities",
            "shadows": "Enabling others, martyrdom, and neglecting own needs",
            "growth": "Learning healthy boundaries and self-care practices"
        },
        "The Creator": {
            "tagline": "The innovative maker of new realities",
            "gifts": "Creativity, imagination, and artistic expression",
            "shadows": "Perfectionism, moodiness, and fear of criticism",
            "growth": "Accepting imperfection and sharing work with others"
        },
        "The Ruler": {
            "tagline": "The responsible leader and organizer",
            "gifts": "Leadership, responsibility, and ability to create order",
            "shadows": "Control issues, tyranny, and fear of chaos",
            "growth": "Leading with compassion and trusting others"
        }
    }
    
    return narratives.get(archetype, {
        "tagline": "Unknown archetype",
        "gifts": "To be discovered",
        "shadows": "To be explored", 
        "growth": "To be developed"
    })

def generate_deeper_insight(top_archetypes: List[tuple], free_text: str = "", model=None) -> str:
    """Generate deeper psychological insight using Gemini AI"""
    if model is None:
        model = configure_gemini()
    
    # Create a detailed prompt for Gemini
    archetype_summary = ", ".join([f"{name} ({score:.1f})" for name, score in top_archetypes])
    
    prompt = f"""You are a wise Jungian psychologist and archetype expert. A person has taken an archetype assessment with these results:

Top Archetypes: {archetype_summary}

Personal reflection: "{free_text}"

Please provide a thoughtful, personalized analysis that includes:

1. **Current Life Phase**: What psychological/spiritual development phase are they likely in?

2. **Integration Opportunity**: How can they balance their dominant archetypes with their less expressed ones?

3. **Shadow Work**: What shadow aspects might they need to acknowledge based on their profile?

4. **Growth Direction**: What specific steps would support their individuation process?

5. **Archetypal Tension**: What creative tension exists between their top archetypes that could fuel growth?

Keep the tone warm, insightful, and empowering. Focus on growth and integration rather than problems. Make it feel personally relevant and actionable.

Length: 3-4 paragraphs maximum."""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                max_output_tokens=600,
            )
        )
        return response.text if response.text else "Unable to generate insight at this time."
    
    except Exception as e:
        return f"AI insight temporarily unavailable. Error: {str(e)}"

def generate_daily_reflection(archetype_name: str, model=None) -> str:
    """Generate a daily reflection question based on the primary archetype"""
    if model is None:
        model = configure_gemini()
    
    prompt = f"""As a Jungian psychologist, create a thoughtful daily reflection question for someone whose primary archetype is {archetype_name}. 

The question should:
- Be personally meaningful and introspective
- Connect to their archetype's growth edge
- Be practical for daily self-reflection
- Encourage integration of their archetype's gifts while addressing potential shadows

Provide just the question, nothing else. Make it thought-provoking but not overwhelming."""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=100,
            )
        )
        return response.text.strip() if response.text else f"How can I embody the best qualities of {archetype_name} today?"
    
    except Exception as e:
        return f"How can I embody the best qualities of {archetype_name} today?"