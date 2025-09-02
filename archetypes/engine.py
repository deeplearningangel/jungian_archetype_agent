
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

ARCHETYPES = [
    "Innocent","Everyperson","Hero","Caregiver","Explorer","Outlaw",
    "Lover","Creator","Jester","Sage","Magician","Ruler"
]

QUESTIONS = [
    {"id":"q1","text":"I naturally trust life and look for the good in people.","archetype":"Innocent","reverse":False},
    {"id":"q2","text":"I feel most myself when things are simple, pure, and harmonious.","archetype":"Innocent","reverse":False},
    {"id":"q3","text":"I value belonging and being relatable more than being exceptional.","archetype":"Everyperson","reverse":False},
    {"id":"q4","text":"I’m happiest when the group feels safe, included, and equal.","archetype":"Everyperson","reverse":False},
    {"id":"q5","text":"I’m driven to prove myself through achievement and courage.","archetype":"Hero","reverse":False},
    {"id":"q6","text":"I like hard challenges—they bring out my best self.","archetype":"Hero","reverse":False},
    {"id":"q7","text":"Protecting and caring for others is central to who I am.","archetype":"Caregiver","reverse":False},
    {"id":"q8","text":"I often take responsibility for others’ wellbeing.","archetype":"Caregiver","reverse":False},
    {"id":"q9","text":"Freedom and self-discovery matter more to me than stability.","archetype":"Explorer","reverse":False},
    {"id":"q10","text":"I get restless without novelty, travel, or new horizons.","archetype":"Explorer","reverse":False},
    {"id":"q11","text":"When systems are unjust, I’m willing to break rules to change them.","archetype":"Outlaw","reverse":False},
    {"id":"q12","text":"I’m allergic to control, conformity, and hypocrisy.","archetype":"Outlaw","reverse":False},
    {"id":"q13","text":"Sensuality, intimacy, and beauty are core to my life force.","archetype":"Lover","reverse":False},
    {"id":"q14","text":"I create connection through tenderness, presence, and desire.","archetype":"Lover","reverse":False},
    {"id":"q15","text":"I feel compelled to make things (art, systems, content, products).","archetype":"Creator","reverse":False},
    {"id":"q16","text":"Originality and aesthetics matter to me more than efficiency.","archetype":"Creator","reverse":False},
    {"id":"q17","text":"I use humor, play, and mischief to shift people’s energy.","archetype":"Jester","reverse":False},
    {"id":"q18","text":"Life is too short to be serious all the time.","archetype":"Jester","reverse":False},
    {"id":"q19","text":"I’m driven by truth, understanding, and making sense of reality.","archetype":"Sage","reverse":False},
    {"id":"q20","text":"I naturally analyze, research, and think in systems.","archetype":"Sage","reverse":False},
    {"id":"q21","text":"I catalyze transformation—my presence changes the room.","archetype":"Magician","reverse":False},
    {"id":"q22","text":"I work with symbols, meaning, and energy to create results.","archetype":"Magician","reverse":False},
    {"id":"q23","text":"I like to organize people and resources toward a vision.","archetype":"Ruler","reverse":False},
    {"id":"q24","text":"I value sovereignty, standards, and setting the tone.","archetype":"Ruler","reverse":False},
]

KEYWORD_BOOSTS = {
    "Innocent": ["pure","hope","faith","grace","goodness","optimism"],
    "Everyperson": ["community","together","belonging","relatable","down to earth","humble"],
    "Hero": ["win","compete","challenge","discipline","courage","athlete"],
    "Caregiver": ["nurture","protect","heal","support","mother","service"],
    "Explorer": ["freedom","adventure","travel","wander","novelty","wild"],
    "Outlaw": ["rebel","revolution","break rules","disrupt","fight","justice"],
    "Lover": ["sensual","intimate","beauty","desire","erotic","pleasure"],
    "Creator": ["create","art","design","build","aesthetic","compose"],
    "Jester": ["funny","play","humor","mischief","joy","banter"],
    "Sage": ["truth","analysis","research","wisdom","philosophy","inquiry"],
    "Magician": ["transform","alchemy","energy","ritual","symbol","manifest"],
    "Ruler": ["lead","sovereign","organize","standard","authority","govern"],
}

NARRATIVES = {
    "Innocent":{"tagline":"Trust, simplicity, and the holy 'yes' to life.","gifts":"Optimism, faith, moral clarity, restorative presence.","shadows":"Naïveté, avoidance of conflict, spiritual bypassing.","growth":"Build boundaries. Let your goodness have a spine."},
    "Everyperson":{"tagline":"Belonging, empathy, and honest ordinariness.","gifts":"Relatability, loyalty, community glue.","shadows":"People-pleasing, fear of standing out.","growth":"Practice brave authenticity—even when it sets you apart."},
    "Hero":{"tagline":"Courage, mastery, and devotion to the hard path.","gifts":"Discipline, grit, execution under pressure.","shadows":"Workaholism, zero-sum thinking, contempt for rest.","growth":"Let tenderness and recovery amplify your power."},
    "Caregiver":{"tagline":"Protection, generosity, and sacred stewardship.","gifts":"Compassion, reliability, safe harbor for others.","shadows":"Martyrdom, burnout, enabling.","growth":"Care for yourself as fiercely as you care for others."},
    "Explorer":{"tagline":"Freedom, discovery, and the road beyond the map.","gifts":"Independence, novelty, adaptive intelligence.","shadows":"Restlessness, commitment phobia.","growth":"Choose a north star to keep wandering meaningful."},
    "Outlaw":{"tagline":"Truth with teeth. Reform through disruption.","gifts":"Courage to defy, bullshit detector, catalytic force.","shadows":"Reactivity, scorched-earth, isolation.","growth":"Aim your fire: design before you detonate."},
    "Lover":{"tagline":"Presence, beauty, and the art of devotion.","gifts":"Magnetism, intimacy, aesthetic intelligence.","shadows":"Enmeshment, vanity, addiction to validation.","growth":"Choose deep nourishment over shallow attention."},
    "Creator":{"tagline":"Originality, elegance, and making the invisible visible.","gifts":"Imagination, craft, taste, invention.","shadows":"Perfectionism, procrastination via tinkering.","growth":"Ship the work. Let the world iterate with you."},
    "Jester":{"tagline":"Holy mischief and joy as medicine.","gifts":"Levity, spontaneity, social alchemy.","shadows":"Deflection through humor, irresponsibility.","growth":"Use play to reveal truth, not run from it."},
    "Sage":{"tagline":"Seeing what is. Serving truth over comfort.","gifts":"Clarity, insight, rigorous thinking.","shadows":"Analysis paralysis, detachment from feeling.","growth":"Let wisdom touch the body—practice applied knowing."},
    "Magician":{"tagline":"Transformation, pattern-weaving, and timing.","gifts":"Synchronicity, meaning-making, energetic precision.","shadows":"Manipulation, grandiosity, spiritual theatrics.","growth":"Anchor your power in service and integrity."},
    "Ruler":{"tagline":"Sovereignty, standards, and elegant order.","gifts":"Leadership, structure, resourcing, protection.","shadows":"Control, rigidity, elitism.","growth":"Rule by designing trust, not demanding it."},
}

from dataclasses import dataclass

@dataclass
class Result:
    scores: dict   # 0..100
    top3: list
    explanation: str

def normalize_scores(raw: dict) -> dict:
    vals = list(raw.values())
    vmin, vmax = min(vals), max(vals)
    if vmax == vmin:
        return {k: 50.0 for k in raw}
    out = {}
    for k, v in raw.items():
        lin = (v - vmin) / (vmax - vmin)
        sig = 1/(1+math.exp(-6*(lin-0.5)))
        out[k] = round(sig*100, 2)
    return out

def keyword_adjustments(free_text: str) -> dict:
    ft = (free_text or "").lower()
    bumps = {a:0.0 for a in ARCHETYPES}
    for arch, words in KEYWORD_BOOSTS.items():
        for w in words:
            if w in ft:
                bumps[arch] += 1.0
    return bumps

def score_responses(responses: dict, free_text: str="") -> Result:
    raw = {a: 0.0 for a in ARCHETYPES}
    counts = {a: 0 for a in ARCHETYPES}
    for q in QUESTIONS:
        val = int(responses.get(q["id"], 4))
        if q["reverse"]:
            val = 8 - val
        raw[q["archetype"]] += val
        counts[q["archetype"]] += 1
    for a in ARCHETYPES:
        if counts[a] > 0:
            raw[a] = raw[a] / counts[a]
    bumps = keyword_adjustments(free_text)
    for a, b in bumps.items():
        raw[a] += b * 0.15
    norm = normalize_scores(raw)
    top3 = sorted(norm.items(), key=lambda kv: kv[1], reverse=True)[:3]
    expl = "Scores reflect your questionnaire averages with small text-based nudges for archetypal keywords."
    return Result(scores=norm, top3=top3, explanation=expl)

def narrative_for(archetype: str) -> dict:
    return NARRATIVES.get(archetype, {"tagline":"", "gifts":"", "shadows":"", "growth":""})
